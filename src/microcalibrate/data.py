"""
Data utilities for downloading and managing datasets.
"""

import pandas as pd
from pathlib import Path
from huggingface_hub import hf_hub_download
from typing import Union


def get_data_directory() -> Path:
    """
    Get the data directory path.
    Creates the directory if it doesn't exist.
    """
    data_dir = Path.home() / ".microcalibrate" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


class Dataset:
    """
    Dataset class for loading data from HDF5 files.
    """
    
    @staticmethod
    def from_file(file_path: Union[str, Path], time_period: int = 2023) -> pd.DataFrame:
        """
        Load dataset from HDF5 file.
        
        Args:
            file_path: Path to the HDF5 file
            time_period: Time period for the dataset
            
        Returns:
            DataFrame containing the dataset
        """
        return pd.read_hdf(file_path, key="data")


def get_dataset(dataset: str = "cps_2023", time_period: int = 2023) -> pd.DataFrame:
    """
    Get the dataset from the huggingface hub.
    
    Args:
        dataset: Dataset name to download
        time_period: Time period for the dataset
        
    Returns:
        DataFrame containing the dataset
    """
    dataset_path = hf_hub_download(
        repo_id="policyengine/policyengine-us-data",
        filename=f"{dataset}.h5",
        local_dir=get_data_directory() / "input" / "cps",
    )

    return Dataset.from_file(dataset_path, time_period=time_period)