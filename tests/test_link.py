# test_link.py


import pytest
import os

from settings import get_config, g

from utils.link.replace import (
    load_id_pool, load_source_samples,
    create_linkage
)
from utils.link.dataset import Dataset


@pytest.fixture
def config():
    c = get_config()
    return c



def test_load_id_pool(config):
    pool = load_id_pool()
    assert type(pool) == Dataset
    assert len(pool) == 0


def test_id_pool_default_compute(config):
    pool = load_id_pool()
    transformed = pool.compute()
    assert len(transformed) == int(config.ID_POOL_MAX_UTILIZATION * config.ID_POOL_SIZE)
    colnames = transformed.columns
    assert len(colnames[0].split('_')) > 1


def test_load_source_samples(config):
    files = load_source_samples()
    n = os.listdir(config.SOURCE_DIR)
    assert len(files) == len(n)
    for f in files:
        assert type(f) == Dataset
        f.compute()
        assert len(f) == config.DATASET_SIZE


def test_create_linkage(config):
    l = create_linkage()
    assert l is not None
    