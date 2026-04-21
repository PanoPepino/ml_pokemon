import pandas as pd

from pathlib import Path


def load_data(path: Path | str) -> pd.DataFrame:
    """Load Pokemon data."""
    path = Path(path)
    df = pd.read_csv(path)
    return df
