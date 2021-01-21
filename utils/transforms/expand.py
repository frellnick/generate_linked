"""
Expand

Frame expansion methods.
    1.  Copy-Permute
    2.  Not implemented
"""
import pandas as pd 
import numpy as np

from settings import get_config, g

config = get_config()



def _sample_source_frame(frame:pd.DataFrame, frame_size:int)->pd.DataFrame:
    print(f'Oversampling frame of size {len(frame)} to {frame_size}')
    return frame.sample(n=frame_size, replace=True)\
        .reset_index(drop=True)


def _permute_column(s:pd.Series):
    return np.random.permutation(s)


def _make_jobs(frame: pd.DataFrame, cols_to_permute:list):
    return [frame[col] for col in cols_to_permute]


def _run_permutations_multiprocess(frame:pd.DataFrame, cols_to_permute:list)->dict:
    jobs = _make_jobs(frame, cols_to_permute)
    uf = g.mpool.map(_permute_column, jobs)
    data = {}
    for i, col in enumerate(cols_to_permute):
        data[col] = uf[i]
    return data


def _run_permutations_singlethread(frame, cols_to_permute:list)->dict:
    data = {}
    for col in cols_to_permute:
        data[col] = _permute_column(frame[col])
    return data


def _add_unpermuted_p_to_data(p:pd.DataFrame, data:dict):
    for col in p.columns:
        if col not in data:
            data[col] = p[col]
    return data


def expand_frame(frame:pd.DataFrame, frame_size:int)->pd.DataFrame:
    p = _sample_source_frame(frame, frame_size)
    cols_to_permute = np.random.choice(p.columns, size=np.random.randint(1, len(p.columns)), replace=False)
    print(f'Permuting {cols_to_permute} columns: {len(cols_to_permute)}')

    if config.MULTIPROCESSING:
        data = _run_permutations_multiprocess(p, cols_to_permute)
    else:
        data = _run_permutations_singlethread(p, cols_to_permute)

    data = _add_unpermuted_p_to_data(p, data)
    df = pd.DataFrame.from_dict(data)
    return df