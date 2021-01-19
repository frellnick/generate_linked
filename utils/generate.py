# generate.py

from settings import config
from .loader import load, get_path_names
from .transforms import force_unique

from functools import partial
import os

def prepare_ids(id_transforms:list = None):
    raw_ids = load(config.ID_PATH)
    if id_transforms is not None:
        for t in id_transforms:
            raw_ids = t(raw_ids)
    return raw_ids


def _get_transforms():
    transforms = []
    if config.UNIQUE_COLUMNS:
        transforms.append(
            partial(force_unique, fieldnames=config.UNIQUE_FIELD_OPTIONS)
            )
    return transforms

def generate_from_source():
    fdir = get_path_names(config.SOURCE_DIR)
    idpool = prepare_ids(_get_transforms())
    return idpool


if __name__ == "__main__":
    idpool = generate_from_source()
    idpool.to_csv(os.path.join(config.ID_DIR, 'test_idpool_modified.csv'), index=False)