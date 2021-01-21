# sample.py

from settings import get_config
import pandas as pd

config = get_config()


def sample_frame(data:pd.DataFrame, n:int=None, replace:bool=False) -> pd.DataFrame:
    if n is None:
        n = config.DATASET_SIZE
    
    return data.sample(n=n, replace=replace)