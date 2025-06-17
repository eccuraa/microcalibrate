import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class Calibration:
    def __init__(
        self,
        loss_matrix: pd.DataFrame,
        weights: np.ndarray,
        targets: np.ndarray,
        epochs: Optional[int] = 32,
        noise_level: Optional[float] = 10.0,
        learning_rate: Optional[float] = 1e-3,
        dropout_rate: Optional[float] = 0.1,
        subsample_every: Optional[int] = 50,
    ):
        """Initialize the Calibration class.

        Args:
            loss_matrix (pd.DataFrame): DataFrame containing the loss matrix.
            weights (np.ndarray): Array of original weights.
            targets (np.ndarray): Array of target values.
            epochs (int): Optional number of epochs for calibration. Defaults to 32.
            noise_level (float): Optional level of noise to add to weights. Defaults to 10.0.
            learning_rate (float): Optional learning rate for the optimizer. Defaults to 1e-3.
            dropout_rate (float): Optional probability of dropping weights during training. Defaults to 0.1.
            subsample_every (int): Optional frequency of subsampling during training. Defaults to 50.
        """

        self.loss_matrix = loss_matrix
        self.weights = weights
        self.targets = targets
        self.epochs = epochs
        self.noise_level = noise_level
        self.learning_rate = learning_rate
        self.dropout_rate = dropout_rate
        self.subsample_every = subsample_every

    def calibrate(self) -> None:
        """Calibrate the weights based on the loss matrix and targets."""

        from .reweight import reweight

        new_weights, subsample = reweight(
            original_weights=self.weights,
            loss_matrix=self.loss_matrix,
            targets_array=self.targets,
            epochs=self.epochs,
            noise_level=self.noise_level,
            learning_rate=self.learning_rate,
            dropout_rate=self.dropout_rate,
            subsample_every=self.subsample_every,
        )

        self.loss_matrix = self.loss_matrix.loc[subsample]
        self.weights = new_weights
