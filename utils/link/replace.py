"""
Replace

Instantiate datsets, idpool, and replace identifying information with idpool.
"""

from .dataset import Dataset
from utils.transforms import stage_partial, sample_frame, rename_col
from settings import get_config, g

config = get_config()

def get_id_pool() -> Dataset:
    num_ids = int(config.ID_POOL_MAX_UTILIZATION * config.ID_POOL_SIZE)
    idpool = Dataset(
        source=config.ID_FILE_SAVE_PATH,
        transforms=[
            stage_partial(sample_frame, n=num_ids),
            stage_partial(rename_col, append='_pool'),
        ]
    )
    return idpool