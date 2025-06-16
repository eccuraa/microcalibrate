"""
Test the calibration process.
"""

from src.microcalibrate.calibration import Calibration
import numpy as np
import pandas as pd

1


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
    mask_20_30 = (data["age"] >= 20) & (data["age"] <= 30)
    mask_40_50 = (data["age"] >= 40) & (data["age"] <= 50)
    mask_target_group = mask_20_30 | mask_40_50
    income_scaled = (data["income"] / data["income"].mean()).clip(
        lower=1e-2, upper=5.0
    )
    weights[mask_target_group] = income_scaled[mask_target_group]
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
            targets_matrix["income_aged_20_30"].sum() * 1.10,
            targets_matrix["income_aged_40_50"].sum() * 1.10,
        ]
    )

    calibrator = Calibration(
        data=data,
        weights=weights,
        targets=targets,
    )

    # Call calibrate method on our data and targets of interest
    calibrator.calibrate()

    calibrated_matrix = pd.DataFrame(
        {
            "income_aged_20_30": (
                (calibrator.data["age"] >= 20) & (calibrator.data["age"] <= 30)
            ).astype(float)
            * calibrator.data["income"],
            "income_aged_40_50": (
                (calibrator.data["age"] >= 40) & (calibrator.data["age"] <= 50)
            ).astype(float)
            * calibrator.data["income"],
        }
    )
    final_weights = (
        calibrated_matrix.mul(calibrator.weights, axis=0).sum().values
    )

    # Check that the calibration process has improved the weights
    np.testing.assert_allclose(
        final_weights,
        targets,
        rtol=6,  # relative tolerance
        err_msg="Calibrated totals do not match target values",
    )
