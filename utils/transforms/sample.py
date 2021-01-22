# sample.py

from settings import get_config
import pandas as pd


config = get_config()


def sample_frame(data:pd.DataFrame, n:int=None, replace:bool=False) -> pd.DataFrame:
    if n is None:
        n = config.DATASET_SIZE

    if not replace:
        assert len(data) > n, F"Trying to sample {n} items from data of length {len(data)} without replacement."
    
    try:
        return data.sample(n=n, replace=replace)
    except Exception as e:
        raise e