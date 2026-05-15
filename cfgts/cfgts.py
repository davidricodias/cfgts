from __future__ import annotations

import copy
import re
from collections import defaultdict
from logging import getLevelNamesMapping, getLogger, root
from threading import Lock

import numpy as np
import pandas as pd
import polars as pl
from dowhy import CausalModel
from numba import prange
from optuna import Study, Trial, create_study
from polars import DataFrame
from sklearn.base import RegressorMixin
from sklearn.utils.validation import NotFittedError, check_is_fitted

from cfgts.logger import activate_logger, log, set_logger_level

__author__ = "José David Rico Días"
__copyright__ = "Copyright (c) 2025 José David Rico Días"
__license__ = "CC BY-NC-ND"


class CFGTS:
    __slots__ = (
        "__run_lock",
        "_all_trials",
        "_causal_model",
        "_counterfactual_study",
        "_counterfactuals",
        "_coverage_set",
        "_coverage_study",
        "_forward_set",
        "_input_cols",
        "_joint_density_model",
        "_marginal_density_model",
        "_num_coverage_trials",
        "_target_cols",
        "counterfactual_value",
        "instance",
        "kwargs",
        "model",
        "n_walk_steps",
        "range_max",
        "range_min",
        "timeout",
        "whitelist",
    )

    def __init__(
        self,
        model: RegressorMixin,
        instance: DataFrame,
        counterfactual_value: DataFrame,
        whitelist: list[str] | None = None,
        timeout: int = 60,
        range_min: int = -(10**1),
        range_max: int = 10**1,
        n_walk_steps: int = 4,
        **kwargs: str,
    ):
        """The CFGTS (CounterFactual Generation for Time Series) class is designed to
        generate counterfactuals for time series data using a fitted multi-output
        autoregressive model.

        The model is autoregressive: given D variables observed over T lags, it
        predicts all D variables at the current timestep.  Input features are
        lagged columns (e.g. X_t-1, X_t-2, Y_t-1, Y_t-2) and targets are
        lag-0 columns (e.g. X_t, Y_t).  The model maps R^(D*T) -> R^D.

        Args:
            model (RegressorMixin): A fitted sklearn multi-output regression
                model whose .predict() returns shape (n_samples, D).
            instance (DataFrame): The initial instance with D*T input columns
                (lagged features, e.g. X_t-1, X_t-2, Y_t-1, Y_t-2).
            counterfactual_value (DataFrame): The target values for all D
                output variables (e.g. X_t, Y_t).
            whitelist (list[str] | None, optional): The variables that the counterfactual engine can use to generate the counterfactuals. If None then all variables are used. Defaults to None.
            timeout (int, optional): The maximum time in seconds to run the counterfactual generation process. Defaults to 60.
            range_min (int, optional): The minimum value for the features when generating counterfactuals. Defaults to -(10**1).
            range_max (int, optional): The maximum value for the features when generating counterfactuals. Defaults to 10**1.
            n_walk_steps (int, optional): Number of forward time steps to walk from each counterfactual and coverage point for generating additional data points for causal validation. Defaults to 4.
            kwargs (str): Additional keyword arguments for configuration. Supported keys include:
                - "verbose": Sets the logging level conformant to the logging library levels. For example CFGTS(..., verbose="DEBUG"). Defaults to "NOTSET".
        """
        self.model: RegressorMixin = model
        self.instance: DataFrame = instance
        self.counterfactual_value: DataFrame = counterfactual_value
        self.whitelist: list[str] | None = whitelist
        self.timeout: int = timeout
        self.range_min: int = range_min
        self.range_max: int = range_max
        self.n_walk_steps: int = n_walk_steps
        self.kwargs: dict[str, str] = kwargs

        self._counterfactuals: DataFrame | None = None
        self._all_trials: DataFrame | None = None
        self._counterfactual_study: Study | None = None
        self._coverage_study: Study | None = None
        self._forward_set: DataFrame | None = None
        self._causal_model: CausalModel | None = None
        self._num_coverage_trials: int = (
            300  # Number of samples in the matrix generated for coverage optimization objective
        )
        self._input_cols: list[str] = list(self.instance.columns)
        self._target_cols: list[str] = list(self.counterfactual_value.columns)

        self.__run_lock = Lock()

        self.__assert_preconditions()

        # Get configuration from kwargs
        self.__setup_logging()

    @property
    def counterfactuals(self: CFGTS) -> DataFrame | None:
        assert self._counterfactuals is not None, (
            "Counterfactuals have not been generated yet. Please run the `run()` method first."
        )
        return self._counterfactuals

    @property
    def study(self: CFGTS) -> Study | None:
        assert self._counterfactual_study is not None, (
            "Study has not been created yet. Please run the `run()` method first."
        )
        return self._counterfactual_study

    def __setup_logging(self: CFGTS) -> None:
        logging_level: str = "NOTSET"
        if "verbose" in self.kwargs.keys():
            verbose_level = (
                self.kwargs.get("verbose") if self.kwargs.get("verbose") is not None else "NOTSET"
            )
            if verbose_level in getLevelNamesMapping().keys() and verbose_level != "NOTSET":
                activate_logger()
                logging_level = verbose_level

        set_logger_level(logging_level)
        # Setup logging for optuna
        for name in root.manager.loggerDict:
            if name.startswith("optuna"):
                optuna_logger = getLogger(name)
                optuna_logger.setLevel(logging_level)

    def __assert_preconditions(self: CFGTS) -> None:
        try:
            check_is_fitted(self.model)
        except NotFittedError as exc:
            log.error("Could not instantiate CFGTS as the model has not been fitted yet")
            raise AssertionError(
                "Could not instantiate CFGTS as the model has not been fitted yet"
            ) from exc

        if (
            "verbose" in self.kwargs.keys()
            and self.kwargs.get("verbose") not in getLevelNamesMapping().keys()
        ):
            msg: str = f"Invalid logging level: {self.kwargs.get('verbose')}. Please use a valid logging level from the logging library."
            log.error(msg)
            raise AssertionError(msg)

    def run(self: CFGTS) -> DataFrame:
        """Runs the CFGTS algorithm to generate counterfactuals.

        Returns:
            DataFrame: The generated counterfactuals.
        """
        with self.__run_lock:
            with log.timeit("Generating counterfactuals"):
                self.__generate_counterfactuals()
                self.__generate_coverage_set()
                self.__generate_forward_set()
                # Use all the counterfactuals found as a seed to generate the causal model
                self.__test_counterfactuals_validity()

            return DataFrame()

    def __test_counterfactuals_validity(self: CFGTS) -> None:
        """Test counterfactual validity using a unified causal DAG.

        For the autoregressive multi-output model R^(D*T) -> R^D:
        1) Builds a single DAG with D*T input + D output vertices.
        2) Estimates causal effects per (input, target) pair via DoWhy backdoor.
        3) Scores each counterfactual as the mean causal consistency across D targets.
        4) Validates whitelisted features (if provided).
        """
        if self._counterfactuals is None or self._coverage_set is None:
            msg = "Counterfactuals or coverage set not generated. Please run `run()` first."
            log.error(msg)
            raise AssertionError(msg)

        input_cols = self._input_cols
        target_cols = self._target_cols

        dfs_to_concat = [self._counterfactuals, self._coverage_set]
        if self._forward_set is not None and not self._forward_set.is_empty():
            dfs_to_concat.append(self._forward_set)
        causal_df: pd.DataFrame = pl.concat(dfs_to_concat).to_pandas()

        # Build unified DAG in GML format:
        #   Vertices: all input columns + all target columns
        #   Edges: (a) every input -> every target; (b) time-lag among inputs
        graph_nodes: list[str] = []
        graph_edges: list[str] = []
        edges_set: set[tuple[str, str]] = set()

        for col in input_cols:
            graph_nodes.append(f'node [id "{col}" label "{col}"]')
        for col in target_cols:
            graph_nodes.append(f'node [id "{col}" label "{col}"]')

        # (a) Every input -> every target
        for inp in input_cols:
            for tgt in target_cols:
                graph_edges.append(f'edge [source "{inp}" target "{tgt}"]')
                edges_set.add((inp, tgt))

        # (b) Time-lag edges among input features
        pattern = re.compile(r"^(?P<base>.+)_t(?:-(?P<lag>\d+))?$")
        lag_to_features: dict[int, list[str]] = {}
        for col in input_cols:
            match = pattern.match(col)
            if not match:
                continue
            lag = int(match.group("lag") or 0)
            lag_to_features.setdefault(lag, []).append(col)

        all_lags_sorted = sorted(lag_to_features.keys())
        for higher_idx in range(1, len(all_lags_sorted)):
            higher_lag = all_lags_sorted[higher_idx]
            for lower_idx in range(0, higher_idx):
                lower_lag = all_lags_sorted[lower_idx]
                for source in lag_to_features[higher_lag]:
                    for target_feat in lag_to_features[lower_lag]:
                        if (source, target_feat) not in edges_set:
                            graph_edges.append(f'edge [source "{source}" target "{target_feat}"]')
                            edges_set.add((source, target_feat))

        gml_body = "\n".join(graph_nodes + graph_edges)
        gml_graph: str = f"graph [\ndirected 1\n{gml_body}\n]"

        instance_df = self.instance.to_pandas()
        counterfactuals_df = self._counterfactuals.to_pandas()

        # Whitelist validation
        if self.whitelist is not None:
            changed_cols: list[str] = []
            instance_vals = instance_df.iloc[0]
            for col in input_cols:
                if not np.allclose(
                    counterfactuals_df[col].to_numpy(),
                    np.full(counterfactuals_df.shape[0], instance_vals[col]),
                    rtol=0.0,
                    atol=1e-8,
                ):
                    changed_cols.append(col)

            invalid_cols = [col for col in changed_cols if col not in self.whitelist]
            if invalid_cols:
                log.warning(
                    "Counterfactuals modify non-whitelisted features: %s",
                    ", ".join(invalid_cols),
                )

        # Estimate causal effect per (input, target) pair
        causal_effects: dict[str, dict[str, float]] = {tgt: {} for tgt in target_cols}

        for tgt in target_cols:
            for inp in input_cols:
                try:
                    feature_model = CausalModel(
                        data=causal_df,
                        treatment=inp,
                        outcome=tgt,
                        graph=gml_graph,
                    )
                    estimand = feature_model.identify_effect()
                    estimate = feature_model.estimate_effect(
                        estimand,
                        method_name="backdoor.linear_regression",
                    )
                    causal_effects[tgt][inp] = float(estimate.value)
                except Exception as exc:  # pragma: no cover
                    log.warning(
                        "Could not estimate causal effect for '%s' -> '%s': %s",
                        inp,
                        tgt,
                        exc,
                    )

        if all(not effects for effects in causal_effects.values()):
            log.warning("No causal effects could be estimated; scoring skipped.")
            self._counterfactuals = self._counterfactuals.with_columns(
                pl.lit(float("nan")).alias("score")
            )
            return

        # Score each counterfactual: mean causal consistency across D targets
        y_hat: np.ndarray = np.asarray(self.model.predict(self.instance), dtype=float)[
            0
        ]  # shape (D,)

        scores: list[float] = []
        instance_vals = instance_df[input_cols].iloc[0].to_numpy(dtype=float)

        for _, row in counterfactuals_df.iterrows():
            cf_vals = row[input_cols].to_numpy(dtype=float)
            delta_x = cf_vals - instance_vals

            target_scores: list[float] = []
            for tgt_idx, tgt in enumerate(target_cols):
                effects = causal_effects[tgt]
                if not effects:
                    continue

                expected_delta = sum(
                    effects[inp] * delta_x[i] for i, inp in enumerate(input_cols) if inp in effects
                )
                actual_y = float(row[tgt])
                actual_delta = actual_y - float(y_hat[tgt_idx])

                target_score = 1.0 - abs(expected_delta - actual_delta) / (
                    abs(expected_delta) + abs(actual_delta) + 1e-10
                )
                target_scores.append(target_score)

            scores.append(float(np.mean(target_scores)) if target_scores else float("nan"))

        self._counterfactuals = self._counterfactuals.with_columns(pl.Series("score", scores))

        avg_score = float(np.mean(scores))
        log.info(
            "Counterfactual causal scores: avg=%.4f, min=%.4f, max=%.4f (%d counterfactuals)",
            avg_score,
            float(np.min(scores)),
            float(np.max(scores)),
            len(scores),
        )

    def __generate_counterfactuals(self: CFGTS) -> None:
        self._counterfactual_study = create_study(directions=["minimize", "minimize"])
        optimization_objective: CFGTS.CounterfactualObjective = self.CounterfactualObjective(
            self.model,
            self.counterfactual_value,
            self.instance,
            range_min=self.range_min,
            range_max=self.range_max,
        )
        self._counterfactual_study.optimize(
            optimization_objective,
            timeout=self.timeout,
            n_jobs=1,
        )

        # Store all trials
        all_trials = defaultdict(list)
        for _trial in self._counterfactual_study.trials:
            for k, v in _trial.params.items():
                all_trials[k].append(v)
        self._all_trials = DataFrame(all_trials, schema=self._input_cols)

        # Store best trials
        counterfactuals = defaultdict(list)
        for _trial in self._counterfactual_study.best_trials:
            for k, v in _trial.params.items():
                counterfactuals[k].append(v)
        self._counterfactuals = DataFrame(counterfactuals, schema=self._input_cols)
        predictions = np.asarray(self.model.predict(self._counterfactuals), dtype=float)
        for idx, col_name in enumerate(self._target_cols):
            self._counterfactuals = self._counterfactuals.with_columns(
                pl.Series(col_name, predictions[:, idx])
            )

    def __generate_coverage_set(self: CFGTS) -> None:
        r"""Calculate coverage set between $\hat{y}$ and $\hat{y}'$ for all D targets."""

        y_star = self.counterfactual_value.to_numpy()[0].astype(np.float64)  # shape (D,)
        y_hat = np.asarray(self.model.predict(self.instance), dtype=np.float64)[0]  # shape (D,)

        # Per-target coverage intervals: diameter 3 * |y_hat_i - y*_i| each
        y_intervals = np.abs(y_hat - y_star)
        y_lower_bounds = np.minimum(y_hat, y_star) - y_intervals
        y_upper_bounds = np.maximum(y_hat, y_star) + y_intervals

        self._coverage_study = create_study(direction="minimize")
        optimization_objective: CFGTS.CoverageObjective = self.CoverageObjective(
            self.model,
            self.instance,
            y_lower_bounds,
            y_upper_bounds,
            self.range_min,
            self.range_max,
            self._num_coverage_trials,
        )

        self._coverage_study.optimize(
            optimization_objective,
            timeout=self.timeout,
            n_jobs=1,
        )

        # Store best trial
        coverage_result = defaultdict(list)
        for trial, value in self._coverage_study.best_trial.params.items():
            feature = trial.split("_", 1)[1]
            coverage_result[feature].append(value)

        self._coverage_set = DataFrame(coverage_result, schema=self._input_cols)
        predictions = np.asarray(self.model.predict(self._coverage_set), dtype=float)
        for idx, col_name in enumerate(self._target_cols):
            self._coverage_set = self._coverage_set.with_columns(
                pl.Series(col_name, predictions[:, idx])
            )

    def __parse_lag_structure(
        self: CFGTS,
    ) -> tuple[list[tuple[str, str, int]], dict[str, str], int]:
        """Parse lag structure from input and target column names.

        Returns:
            tuple: (col_info, base_to_target, max_lag) where
                col_info is a list of (column_name, base_variable, lag) per input column,
                base_to_target maps base variable name to target column (e.g. "X" -> "X_t"),
                max_lag is the maximum lag T found.
        """
        pattern = re.compile(r"^(?P<base>.+)_t(?:-(?P<lag>\d+))?$")
        col_info: list[tuple[str, str, int]] = []
        for col in self._input_cols:
            match = pattern.match(col)
            if match:
                base = match.group("base")
                lag = int(match.group("lag") or 0)
                col_info.append((col, base, lag))

        base_to_target: dict[str, str] = {}
        for tgt in self._target_cols:
            match = pattern.match(tgt)
            if match:
                base_to_target[match.group("base")] = tgt

        max_lag = max(lag for _, _, lag in col_info) if col_info else 0
        return col_info, base_to_target, max_lag

    def __generate_forward_set(self: CFGTS) -> None:
        """Generate additional data points by walking the model forward from counterfactuals and coverage set."""
        if self._counterfactuals is None or self._coverage_set is None:
            return

        source_df = pl.concat([self._counterfactuals, self._coverage_set])
        parts: list[DataFrame] = []

        for row_idx in range(source_df.shape[0]):
            row_input = source_df[row_idx, : len(self._input_cols)].to_numpy()[0]
            walked = self.__walk_forward_from(row_input, self.n_walk_steps)
            if not walked.is_empty():
                parts.append(walked)

        self._forward_set = pl.concat(parts) if parts else None

        if self._forward_set is not None:
            log.info(
                "Forward walking generated %d data points from %d source rows",
                self._forward_set.shape[0],
                source_df.shape[0],
            )

    def __walk_forward_from(self: CFGTS, start_input: np.ndarray, n_steps: int) -> DataFrame:
        """Walk the model forward n_steps times from a given input vector recurrently."""
        col_info, base_to_target, max_lag = self.__parse_lag_structure()

        col_index: dict[tuple[str, int], int] = {}
        for idx, (_, base, lag) in enumerate(col_info):
            col_index[(base, lag)] = idx

        current_input = start_input.copy()
        rows: list[np.ndarray] = []

        for _ in range(n_steps):
            pred = np.asarray(
                self.model.predict(
                    DataFrame(current_input.reshape(1, -1), schema=self._input_cols)
                ),
                dtype=float,
            )[0]

            rows.append(np.concatenate([current_input, pred]))

            # Shift window forward: lag L ← lag L-1, lag 1 ← predicted target
            new_input = current_input.copy()
            for base, tgt_col in base_to_target.items():
                tgt_idx = self._target_cols.index(tgt_col)
                for lag in range(max_lag, 1, -1):
                    if (base, lag) in col_index and (base, lag - 1) in col_index:
                        new_input[col_index[(base, lag)]] = current_input[
                            col_index[(base, lag - 1)]
                        ]
                if (base, 1) in col_index:
                    new_input[col_index[(base, 1)]] = pred[tgt_idx]
            current_input = new_input

        if not rows:
            return DataFrame(schema=self._input_cols + self._target_cols)

        return DataFrame(np.stack(rows), schema=self._input_cols + self._target_cols)

    class CoverageObjective:
        def __init__(
            self,
            model: RegressorMixin,
            instance: DataFrame,
            y_lower_bounds: np.ndarray,
            y_upper_bounds: np.ndarray,
            range_min: int,
            range_max: int,
            num_coverage_trials: int,
        ) -> None:
            self.model = model
            self.instance = copy.deepcopy(instance).to_numpy()
            self.variables = copy.deepcopy(instance.columns)
            self.y_lower_bounds = y_lower_bounds
            self.y_upper_bounds = y_upper_bounds
            self.range_min = range_min
            self.range_max = range_max
            self.num_coverage_trials = num_coverage_trials

        def __call__(self, trial: Trial) -> float:
            x_space: np.ndarray = np.empty(shape=(self.num_coverage_trials, self.instance.shape[1]))

            for instance_num in range(self.num_coverage_trials):
                for i in range(self.instance.shape[1]):
                    x_space[instance_num][i] = trial.suggest_float(
                        f"{instance_num}_{self.variables[i]}", self.range_min, self.range_max
                    )

            y_space = np.asarray(
                self.model.predict(DataFrame(x_space, schema=self.variables)), dtype=float
            )  # shape (num_coverage_trials, D)

            # Mean star discrepancy across D target dimensions
            n_targets = y_space.shape[1]
            total_disc = 0.0
            for d in range(n_targets):
                total_disc += self.__out_sampled_star_discrepancy(
                    y_space[:, d],
                    bounds=(self.y_lower_bounds[d], self.y_upper_bounds[d]),
                )
            return total_disc / n_targets

        @staticmethod
        def __out_sampled_star_discrepancy(
            sample: np.ndarray, bounds: tuple[int | float, int | float] = (0, 1)
        ) -> np.float64:
            """Compute star discrepancy for sets that can have elements outside the defined bounds

            Args:
                sample (np.ndarray): sample to compute the discrepancy from
                bounds (tuple[int | float, int | float], optional): Interval bounds for the disc. Defaults to (0, 1).

            Returns:
                np.float64: Discrepancy
            """
            a, b = bounds

            # Filter: keep only points in [a, b]
            sample_filtered = sample[(sample >= a) & (sample <= b)]

            n = len(sample_filtered)

            if n == 0:
                return 10e10

            # Normalize to [0, 1]
            sample_normalized = (sample_filtered - a) / (b - a)

            d = 1

            # Term 1: disc1
            abs_diff = np.abs(sample_normalized - 0.5)
            disc1 = np.sum(1 + 0.5 * abs_diff - 0.5 * abs_diff**2)

            # Term 2: disc2 - using broadcasting
            i_vals = sample_normalized[:, np.newaxis]  # Shape: (n, 1)
            j_vals = sample_normalized[np.newaxis, :]  # Shape: (1, n)

            term = (
                1
                + 0.5 * np.abs(i_vals - 0.5)
                + 0.5 * np.abs(j_vals - 0.5)
                - 0.5 * np.abs(i_vals - j_vals)
            )
            disc2 = np.sum(term)

            result = (13.0 / 12.0) ** d - 2.0 / n * disc1 + 1.0 / (n**2) * disc2

            return result

        def scale_array(arr: np.ndarray, a: int | float, b: int | float) -> np.ndarray:
            arr = np.asarray(arr)
            min_val, max_val = arr.min(), arr.max()
            if min_val == max_val:
                # already uniform, map to midpoint
                return np.full_like(arr, (a + b) / 2)
            return (arr - min_val) / (max_val - min_val) * (b - a) + a + 1e-8

    class CounterfactualObjective:
        def __init__(
            self,
            model: RegressorMixin,
            objective_value: DataFrame,
            instance: DataFrame,
            range_min: int = -(10**1),
            range_max: int = 10**1,
        ) -> None:
            self.model = model
            self.objective_value = copy.deepcopy(objective_value).to_numpy()
            self.instance = copy.deepcopy(instance).to_numpy()
            self.variables = copy.deepcopy(instance.columns)
            self.suggested_instance = np.ndarray(shape=(instance.shape[0], instance.shape[1]))
            self.range_min = range_min
            self.range_max = range_max

        def __call__(self, trial: Trial) -> tuple[float, float]:
            suggestion = np.ndarray(shape=(self.instance.shape[0], self.instance.shape[1]))
            for i in range(len(self.suggested_instance)):
                for j in range(len(self.suggested_instance[i])):
                    suggestion[i][j] = trial.suggest_float(
                        f"{self.variables[j]}", self.range_min, self.range_max
                    )
            features_diff = distance_between_observations(self.instance, suggestion)
            y_hat_prima = self.model.predict(DataFrame(suggestion, schema=self.variables))
            # Sum of per-target relative errors: Σᵢ |y*ᵢ − ŷᵢ| / |y*ᵢ|
            objective_diff = float(
                np.sum(np.abs(self.objective_value - y_hat_prima) / np.abs(self.objective_value))
            )
            return objective_diff, features_diff


# @njit(fastmath=True)
def distance(A: np.ndarray, B: np.ndarray) -> np.float64:
    return np.sqrt(np.sum((A - B) ** 2))  # Euclidean distance


# @njit(fastmath=True)
def distance_between_observations(A: np.ndarray, B: np.ndarray) -> np.float64:
    num_rows = A.shape[0]
    total_distance = 0.0
    for i in prange(num_rows):  # Parallel iteration
        total_distance += distance(A[i], B[i])
    total_distance /= A.shape[0]
    return total_distance
