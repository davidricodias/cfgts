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
from sklearn.multioutput import MultiOutputRegressor

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
    And there should be a log with the error message containing 'Could not instantiate CFGTS as the model has not been fitted yet'
    """

    model = MultiOutputRegressor(LinearRegression())
    instance = DataFrame({"X_t-1": [1]})
    counterfactual_value = DataFrame({"X_t": [4]})

    with pytest.raises(AssertionError):
        CFGTS(model, instance, counterfactual_value)
    assert ["Could not instantiate CFGTS as the model has not been fitted yet"] == [
        rec.message for rec in caplog.records
    ]


def test_given_model_is_fitted_then_cfgts_init_instantiates_ok():
    """
    Given a multi-output model is fitted
    When CFGTS inits
    Then no error must be thrown
    """

    model = MultiOutputRegressor(LinearRegression())
    X = DataFrame({"X_t-1": [1, 2, 3], "Y_t-1": [4, 5, 6]})
    y = DataFrame({"X_t": [2, 3, 4], "Y_t": [5, 6, 7]})
    model.fit(X, y)
    instance = DataFrame({"X_t-1": [1], "Y_t-1": [4]})
    counterfactual_value = DataFrame({"X_t": [3], "Y_t": [6]})

    CFGTS(model, instance, counterfactual_value, timeout=60, verbose="DEBUG")


def test_given_model_is_fitted_then_cfgts_init_instantiates_ok_and_generate_counterfactual_value_generates_ok():
    """
    Given a multi-output model is fitted
    And CFGTS is instantiated
    When calling __generate_counterfactuals()
    Then there should be counterfactual values
    And the counterfactuals property should return a non-empty DataFrame
    And the study property should return a non-None Study object
    """
    model = MultiOutputRegressor(LinearRegression())
    X = DataFrame({"X_t-1": [1, 2, 3], "Y_t-1": [4, 5, 6]})
    y = DataFrame({"X_t": [2, 3, 4], "Y_t": [5, 6, 7]})
    model.fit(X, y)
    instance = DataFrame({"X_t-1": [1], "Y_t-1": [4]})
    counterfactual_value = DataFrame({"X_t": [3], "Y_t": [6]})

    cfgts = CFGTS(model, instance, counterfactual_value, timeout=60, verbose="DEBUG")
    cfgts._CFGTS__generate_counterfactuals()  # type: ignore

    assert cfgts.counterfactuals is not None
    assert not cfgts.counterfactuals.is_empty()
    # Counterfactuals should have both input + target columns
    assert "X_t-1" in cfgts.counterfactuals.columns
    assert "Y_t-1" in cfgts.counterfactuals.columns
    assert "X_t" in cfgts.counterfactuals.columns
    assert "Y_t" in cfgts.counterfactuals.columns
    assert cfgts.study is not None


def test_autoregressive_full_pipeline(caplog):
    """
    Given an autoregressive multi-output model with 2 variables and 2 lags
    When the full CFGTS pipeline runs (counterfactuals + coverage + causal scoring)
    Then counterfactuals are generated with D target columns and a score column
    """
    caplog.clear()
    model = MultiOutputRegressor(LinearRegression())
    # 2 variables (X, Y) with 2 lags
    X = DataFrame(
        {
            "X_t-1": [0, 1, 2, 3, 4],
            "X_t-2": [0, 0, 1, 2, 3],
            "Y_t-1": [0, 3, 4, 5, 6],
            "Y_t-2": [0, 0, 3, 4, 5],
        }
    )
    y = DataFrame(
        {
            "X_t": [1, 2, 3, 4, 5],
            "Y_t": [3, 4, 5, 6, 7],
        }
    )
    model.fit(X, y)
    instance = DataFrame({"X_t-1": [2], "X_t-2": [1], "Y_t-1": [4], "Y_t-2": [3]})
    counterfactual_value = DataFrame({"X_t": [5], "Y_t": [7]})

    cfgts = CFGTS(model, instance, counterfactual_value, timeout=60, verbose="DEBUG")
    cfgts._CFGTS__generate_counterfactuals()  # type: ignore
    cfgts._CFGTS__generate_coverage_set()  # type: ignore
    cfgts._CFGTS__generate_forward_set()  # type: ignore
    cfgts._CFGTS__test_counterfactuals_validity()  # type: ignore

    assert cfgts.counterfactuals is not None
    assert "score" in cfgts.counterfactuals.columns
    assert "X_t" in cfgts.counterfactuals.columns
    assert "Y_t" in cfgts.counterfactuals.columns
    assert any("Counterfactual causal scores" in rec.message for rec in caplog.records)


def test_forward_walking_generates_data_points(caplog):
    """
    Given an autoregressive multi-output model with 2 variables and 2 lags
    When forward walking is performed with n_walk_steps=2
    Then _forward_set should contain rows from walking each counterfactual and coverage row
    And all rows should have correct columns
    """
    caplog.clear()
    model = MultiOutputRegressor(LinearRegression())
    X = DataFrame(
        {
            "X_t-1": [0, 1, 2, 3, 4],
            "X_t-2": [0, 0, 1, 2, 3],
            "Y_t-1": [0, 3, 4, 5, 6],
            "Y_t-2": [0, 0, 3, 4, 5],
        }
    )
    y = DataFrame(
        {
            "X_t": [1, 2, 3, 4, 5],
            "Y_t": [3, 4, 5, 6, 7],
        }
    )
    model.fit(X, y)
    instance = DataFrame({"X_t-1": [2], "X_t-2": [1], "Y_t-1": [4], "Y_t-2": [3]})
    counterfactual_value = DataFrame({"X_t": [5], "Y_t": [7]})

    n_steps = 2
    cfgts = CFGTS(
        model, instance, counterfactual_value, timeout=10, n_walk_steps=n_steps, verbose="DEBUG"
    )
    cfgts._CFGTS__generate_counterfactuals()  # type: ignore
    cfgts._CFGTS__generate_coverage_set()  # type: ignore
    cfgts._CFGTS__generate_forward_set()  # type: ignore

    fb_set = cfgts._forward_set
    assert fb_set is not None
    assert cfgts._counterfactuals is not None
    assert cfgts._coverage_set is not None
    n_source_rows = cfgts._counterfactuals.shape[0] + cfgts._coverage_set.shape[0]
    assert fb_set.shape[0] == n_source_rows * n_steps
    # Check all expected columns are present
    for col in ["X_t-1", "X_t-2", "Y_t-1", "Y_t-2", "X_t", "Y_t"]:
        assert col in fb_set.columns
    assert any("Forward walking generated" in rec.message for rec in caplog.records)


def test_full_pipeline_with_forward_walking(caplog):
    """
    Given an autoregressive model
    When the full pipeline runs with timeout=10 and n_walk_steps=2
    Then counterfactuals should be generated without error
    And counterfactuals should have a score column
    And forward data should be included in causal validation
    """
    caplog.clear()
    model = MultiOutputRegressor(LinearRegression())
    X = DataFrame(
        {
            "X_t-1": [0, 1, 2, 3, 4],
            "X_t-2": [0, 0, 1, 2, 3],
            "Y_t-1": [0, 3, 4, 5, 6],
            "Y_t-2": [0, 0, 3, 4, 5],
        }
    )
    y = DataFrame(
        {
            "X_t": [1, 2, 3, 4, 5],
            "Y_t": [3, 4, 5, 6, 7],
        }
    )
    model.fit(X, y)
    instance = DataFrame({"X_t-1": [2], "X_t-2": [1], "Y_t-1": [4], "Y_t-2": [3]})
    counterfactual_value = DataFrame({"X_t": [5], "Y_t": [7]})

    cfgts = CFGTS(
        model, instance, counterfactual_value, timeout=10, n_walk_steps=2, verbose="DEBUG"
    )
    cfgts.run()

    assert cfgts.counterfactuals is not None
    assert "score" in cfgts.counterfactuals.columns
    assert cfgts._forward_set is not None
