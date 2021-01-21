# test_link.py


import pytest

from settings import get_config, g

from utils.link.replace import get_id_pool
from utils.link.dataset import Dataset


@pytest.fixture
def config():
    c = get_config()
    return c



def test_get_id_pool(config):
    pool = get_id_pool()
    assert type(pool) == Dataset
    assert len(pool) == 0


def test_id_pool_default_compute(config):
    pool = get_id_pool()
    transformed = pool.compute()
    assert len(transformed) == int(config.ID_POOL_MAX_UTILIZATION * config.ID_POOL_SIZE)
