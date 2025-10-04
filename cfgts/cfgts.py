from __future__ import annotations

import copy
from collections import defaultdict
from logging import getLevelNamesMapping, getLogger, root
from threading import Lock

import numpy as np
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
        "_counterfactuals",
        "_study",
        "counterfactual_value",
        "instance",
        "kwargs",
        "model",
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
        **kwargs: str,
    ):
        """The CFGTS (CounterFactual Generation for Time Series) class is designed to
        generate counterfactuals for time series data using a fitted regression model.

        Args:
            model (RegressorMixin): A fitted sklearn regression model.
            instance (DataFrame): The initial instance for which the counterfactual is generated.
            counterfactual_value (DataFrame): The target counterfactual output.
            whitelist (list[str] | None, optional): The variables that the counterfactual engine can use to generate the counterfactuals. If None then all variables are used. Defaults to None.
            timeout (int, optional): The maximum time in seconds to run the counterfactual generation process. Defaults to 60.
            range_min (int, optional): The minimum value for the features when generating counterfactuals. Defaults to -(10**1).
            range_max (int, optional): The maximum value for the features when generating counterfactuals. Defaults to 10**1.
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
        self.kwargs: dict[str, str] = kwargs

        self._counterfactuals: DataFrame | None = None
        self._all_trials: DataFrame | None = None
        self._study: Study | None = None

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
        assert self._study is not None, (
            "Study has not been created yet. Please run the `run()` method first."
        )
        return self._study

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
            raise exc

        if (
            "verbose" in self.kwargs.keys()
            and self.kwargs.get("verbose") not in getLevelNamesMapping().keys()
        ):
            msg: str = f"Invalid logging level: {self.kwargs.get('verbose')}. Please use a valid logging level from the logging library."
            log.error(msg)
            raise ValueError(msg)

    def run(self: CFGTS) -> DataFrame:
        """Runs the CFGTS algorithm to generate counterfactuals.

        Returns:
            DataFrame: The generated counterfactuals.
        """
        with self.__run_lock:
            with log.timeit("Generating counterfactuals"):
                self.__generate_counterfactuals()
            # Use all the counterfactuals found as a seed to generate the causal model

            return DataFrame()

    def __generate_counterfactuals(self: CFGTS) -> None:
        self._study = create_study(directions=["minimize", "minimize"])
        optimization_objective: CFGTS.Objective = self.Objective(
            self.model,
            self.counterfactual_value,
            self.instance,
            range_min=self.range_min,
            range_max=self.range_max,
        )
        self._study.optimize(
            optimization_objective,
            timeout=self.timeout,
            n_jobs=-1,
        )

        # Store all trials
        all_trials = defaultdict(list)
        for _trial in self._study.trials:
            for k, v in _trial.params.items():
                all_trials[k].append(v)
        self._all_trials = DataFrame(all_trials, schema=self.instance.columns)

        # Store best trials
        counterfactuals = defaultdict(list)
        for _trial in self._study.best_trials:
            for k, v in _trial.params.items():
                counterfactuals[k].append(v)
        self._counterfactuals = DataFrame(counterfactuals, schema=self.instance.columns)

    class Objective:
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
            for i in range(len(self.suggested_instance)):
                for j in range(len(self.suggested_instance[i])):
                    self.suggested_instance[i][j] = trial.suggest_float(
                        f"{self.variables[j]}", self.range_min, self.range_max
                    )
            features_diff = distance_between_observations(self.instance, self.suggested_instance)
            y_hat = self.model.predict(DataFrame(self.suggested_instance, schema=self.variables))
            objective_diff = np.abs(self.objective_value - y_hat) / (
                self.objective_value
            )  # Relative difference
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
