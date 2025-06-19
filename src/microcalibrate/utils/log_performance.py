from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import torch


def log_performance_over_epochs(
    tracked: Dict[str, List[Any]],
    targets: torch.Tensor,
    target_names: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Calculate the errors and performance metrics for the model for all the logged epochs.

    Args:
        tracked (Dict[str, List[Any]]): Dictionary containing lists of tracked metrics.
        targets (torch.Tensor): Array of target values.
        targets_names (torch.Tensor): Array of target names.

    Returns:
        performance_df: DataFrame containing the calculated errors and performance metrics.
    """
    targets = targets.detach().cpu().numpy()
    k = len(targets)

    df = pd.DataFrame(
        {
            "epoch": tracked["epochs"],
            "loss": tracked["loss"],
            "pct_close": tracked["pct_close"],
        }
    )

    # Expand estimates into a matrix (n_epochs, k_targets)
    estimates = np.stack(tracked["estimates"])
    estimates_df = pd.DataFrame(
        estimates, columns=[f"estimate_{i}" for i in range(k)]
    )

    # Broadcast targets across all rows
    targets_df = pd.DataFrame(
        np.tile(targets, (len(df), 1)),
        columns=(
            target_names
            if target_names is not None
            else [f"target_{i}" for i in range(k)]
        ),
    )

    # Compute errors
    errors_df = estimates_df.values - targets_df.values
    abs_errors_df = np.abs(errors_df)
    rel_abs_errors_df = abs_errors_df / targets_df.values

    # Package into DataFrames with column names
    errors_df = pd.DataFrame(
        errors_df, columns=[f"error_{i}" for i in range(k)]
    )
    abs_errors_df = pd.DataFrame(
        abs_errors_df, columns=[f"abs_error_{i}" for i in range(k)]
    )
    rel_abs_errors_df = pd.DataFrame(
        rel_abs_errors_df, columns=[f"rel_abs_error_{i}" for i in range(k)]
    )

    # Concatenate all
    performance_df = pd.concat(
        [
            df.reset_index(drop=True),
            targets_df,
            estimates_df,
            errors_df,
            abs_errors_df,
            rel_abs_errors_df,
        ],
        axis=1,
    )

    return performance_df
