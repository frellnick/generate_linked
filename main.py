#main.py


import argparse
from settings import get_config
from utils.loader import load, get_path_names
from utils.transforms import force_unique

from functools import partial
import os

config = get_config()

def _load_process_id_pool(id_transforms:list = None):
    raw_ids = load(config.ID_FILE_PATH)
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


def modify_idpool(save=True):
    idpool = _load_process_id_pool(_get_transforms())
    if save:
        idpool.to_csv(os.path.join(config.ID_DIR, 'test_idpool_modified.csv'), index=False)
    return idpool


def run(*args, **kwargs):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate Identity Pool and Linked Datasets')

    idpool = _load_process_id_pool()
    print(idpool.head())