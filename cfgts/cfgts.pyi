from optuna import Study
from polars import DataFrame as DataFrame
from sklearn.base import RegressorMixin as RegressorMixin

from cfgts.logger import log as log

class CFGTS:
    model: RegressorMixin
    instance: DataFrame
    counterfactual_value: DataFrame
    whitelist: list[str] | None
    timeout: int
    range_min: int
    range_max: int
    n_walk_steps: int
    counterfactuals: DataFrame | None
    study: Study | None
    _counterfactuals: DataFrame | None
    _coverage_set: DataFrame | None
    _forward_set: DataFrame | None

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
    ) -> None:
        """Autoregressive multi-output counterfactual generator.

        Args:
            model: A fitted sklearn multi-output regressor (predict returns (n, D)).
            instance: D*T input columns (lagged features, e.g. X_t-1, Y_t-2).
            counterfactual_value: Target values for all D outputs (e.g. X_t, Y_t).
            whitelist: Allowed input features to change. None means all.
            timeout: Max seconds per optimization phase.
            range_min: Lower bound for feature suggestions.
            range_max: Upper bound for feature suggestions.
            n_walk_steps: Number of forward steps for temporal data augmentation.
            kwargs: "verbose" key sets logging level.
        """
        ...
    def run(self: CFGTS) -> None: ...
