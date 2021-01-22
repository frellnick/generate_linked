"""
Replace

Instantiate datsets, idpool, and replace identifying information with idpool.
"""

from .dataset import Dataset

from utils.transforms import stage_partial, sample_frame, rename_col
from settings import get_config, g
from assets.mappings import colmap
from .linkage import Linkage

import os

config = get_config()


def load_id_pool() -> Dataset:
    num_ids = max(
        [
            int(config.ID_POOL_MAX_UTILIZATION * config.ID_POOL_SIZE),
            config.DATASET_SIZE,
        ]
    )
    idpool = Dataset(
        source=config.ID_FILE_SAVE_PATH,
        transforms=[
            stage_partial(sample_frame, n=num_ids),
            stage_partial(rename_col, append='_pool'),
        ]
    )
    return idpool


def _list_files(s=None):
    if s is None:
        s = config.SOURCE_DIR
    return [os.path.join(s, filename) for filename in os.listdir(s)]
    

def load_source_samples():
    t = [
        stage_partial(sample_frame, replace=True),
    ]
    files = [Dataset(s, t) for s in _list_files()]
    return files


def create_linkage():
    l = Linkage(
        files=load_source_samples(),
        idpool=load_id_pool()
    )
    l.process()
    return l