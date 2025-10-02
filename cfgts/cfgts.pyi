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
    counterfactuals: DataFrame | None
    study: Study | None

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
    ) -> None: ...
    def run(self: CFGTS) -> None: ...
