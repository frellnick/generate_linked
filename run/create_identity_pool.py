# create_identity_pool.py

from pandas.core import frame
from settings import get_config, g
from utils.loader import load
from utils.transforms import force_unique, expand_frame

from functools import partial
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
    epool = expand_frame(frame=pool, frame_size=pool_size)
    epool['id'] = np.arange(pool_size)
    return epool


def create_id_pool(config=config) -> pd.DataFrame:
    raw_pool = _load_source_pool()
    if len(raw_pool) < config.ID_POOL_SIZE:
        pool = _expand_pool(raw_pool, config.ID_POOL_SIZE)
    else:
        pool = raw_pool.sample(n=config.ID_POOL_SIZE)
    return _transform_save_pool(
        pool, save=config.SAVE_POOL, 
        save_path=config.ID_FILE_SAVE_PATH)