# create_identity_pool.py

import argparse
from settings import get_config
from utils.loader import load, get_path_names
from utils.transforms import force_unique

from functools import partial
import os
import pandas as pd
import numpy as np


config = get_config()

def _load_source_pool():
    return load(config.ID_FILE_PATH)


def _transform_pool(source_pool:pd.DataFrame, id_transforms:list = None):
    p = source_pool.copy()
    if id_transforms is not None:
        for t in id_transforms:
            p = t(p)
    return p


def _get_transforms()->list:
    transforms = []
    if config.UNIQUE_COLUMNS:
        transforms.append(
            partial(force_unique, fieldnames=config.UNIQUE_FIELD_OPTIONS)
            )
    return transforms


def _transform_save_pool(pool:pd.DataFrame, save=False, save_path=None)->pd.DataFrame:
    tpool =_transform_pool(pool, _get_transforms())
    if save:
        tpool.to_csv(save_path, index=False)
    return tpool


def _expand_pool(pool:pd.DataFrame, pool_size:int)->pd.DataFrame:
    def _copy_with_permuation(pool:pd.DataFrame, pool_size:int)->pd.DataFrame:
        print(f'Oversampling pool of size {len(pool)} to {pool_size}')
        p = pool.sample(n=pool_size, replace=True)\
            .reset_index(drop=True)
        for col in np.random.choice(p.columns, size=np.random.randint(1, len(p.columns)), replace=False):
            print(f'Permuting ID Pool Column: ', col)
            p[col] = np.random.permutation(p[col])
        return p 
    return _copy_with_permuation(pool, pool_size)


def create_id_pool(config=config) -> pd.DataFrame:
    raw_pool = _load_source_pool()
    if len(raw_pool) < config.ID_POOL_SIZE:
        pool = _expand_pool(raw_pool, config.ID_POOL_SIZE)
    else:
        pool = raw_pool.sample(n=config.ID_POOL_SIZE)
    return _transform_save_pool(
        pool, save=config.SAVE_POOL, 
        save_path=config.ID_FILE_SAVE_PATH)