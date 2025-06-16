"""
Test the calibration process.
"""

from src.microcalibrate.calibration import Calibration
import numpy as np
import pandas as pd


def test_calibration() -> None:
    """Test the calibration process."""

    # Create a mock dataset with age and income
    data = pd.DataFrame(
        {
            "age": np.random.randint(18, 70, size=100),
            "income": np.random.normal(40000, 50000, size=100),
        }
    )
    weights = np.ones(len(data))
    targets_matrix = pd.DataFrame(
        {
            "income_aged_20_30": (
                (data["age"] >= 20) & (data["age"] <= 30)
            ).astype(float)
            * data["income"],
            "income_aged_40_50": (
                (data["age"] >= 40) & (data["age"] <= 50)
            ).astype(float)
            * data["income"],
        }
    )
    targets = np.array(
        [
            (targets_matrix["income_aged_20_30"] * weights).sum() * 1,
            (targets_matrix["income_aged_40_50"] * weights).sum() * 1,
        ]
    )

    calibrator = Calibration(
        data=data,
        weights=weights,
        targets=targets,
    )

    # Call calibrate method on our data and targets of interest
    # calibrator.calibrate()
    final_weights = targets_matrix.mul(calibrator.weights, axis=0).sum().values

    # Check that the calibration process has improved the weights
    np.testing.assert_allclose(
        final_weights,
        targets,
        rtol=0.01,  # relative tolerance
        err_msg="Calibrated totals do not match target values",
    )
