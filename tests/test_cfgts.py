"""cfgts tests

Plese remember to follow the basic four steps:
1. Arrange
2. Act
3. Assert
4. Cleanup
"""

import pytest
from polars import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.utils.validation import NotFittedError

from cfgts import CFGTS
from cfgts.logger import activate_logger, set_logger_level

activate_logger()
set_logger_level("DEBUG")


def test_given_model_is_not_fitted_when_cfgts_is_instantiated_then_raises_NotFittedError_and_logs_error(
    caplog,
):
    """
    Given a model is instantiated
    And the model is not fitted
    When CFGTS is instantiated
    Then CFGTS should raise NotFittedError
    And there should be a log the error message containing 'Could not instantiate CFGTS as the model has not been fitted yet'
    """

    model = LinearRegression()
    instance = DataFrame({"X": [1]})
    counterfactual_value = DataFrame({"Y": [4]})

    with pytest.raises(NotFittedError):
        CFGTS(model, instance, counterfactual_value)
    assert ["Could not instantiate CFGTS as the model has not been fitted yet"] == [
        rec.message for rec in caplog.records
    ]


def test_given_model_is_fitted_then_cfgts_init_instantiates_ok():
    """
    Given a model is instantiated
    And the model is fitted
    When CFGTS inits
    Then no error must be thrown
    """

    model = LinearRegression()
    X = DataFrame({"X1": [1, 2, 3]})
    y = DataFrame({"Y": [4, 5, 6]})
    model.fit(X, y)
    instance = DataFrame({"X1": [1]})
    counterfactual_value = DataFrame({"Y": [4]})

    CFGTS(model, instance, counterfactual_value)


def test_given_model_is_fitted_then_cfgts_init_instantiates_ok_and_generate_counterfactual_value_generates_ok():
    """
    Given a model is instantiated
    And the model is fitted
    And CFGTS is instantiated
    When calling __generate_counterfactuals()
    Then there should be counterfactual values
    And the counterfactuals property should return a non-empty DataFrame
    And the study property should return a non-None Study object
    And the counterfactual values should be within range
    """
    model = LinearRegression()
    X = DataFrame({"X1": [1, 2, 3]})
    y = DataFrame({"Y": [4, 5, 6]})
    model.fit(X, y)
    instance = DataFrame({"X1": [1]})
    counterfactual_value = DataFrame({"Y": [5]})

    cfgts = CFGTS(model, instance, counterfactual_value, timeout=10, verbose="DEBUG")
    # Run private method
    cfgts._CFGTS__generate_counterfactuals()  # type: ignore

    assert cfgts.counterfactuals is not None
    assert not cfgts.counterfactuals.is_empty()
    assert cfgts.counterfactuals.mean().rows()[0][0] <= 2
    assert cfgts.counterfactuals.mean().rows()[0][0] >= 1
    assert cfgts.study is not None
