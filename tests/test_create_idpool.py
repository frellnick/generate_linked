# test_create_idpool.py


import pytest
import os
from settings import get_config
from run.create_identity_pool import create_id_pool


@pytest.fixture
def testconfig():
    c = get_config(debug=True)
    return c


def test_create_small_pool(testconfig):
    testconfig.ID_POOL_SIZE = 10000
    testconfig.SAVE_POOL = False
    pool = create_id_pool(config=testconfig)
    assert len(pool) == testconfig.ID_POOL_SIZE


def test_create_large_pool(testconfig):
    testconfig.ID_POOL_SIZE = 200000
    testconfig.SAVE_POOL = False
    pool = create_id_pool(config=testconfig)


def test_create_save_small_pool(testconfig):
    testconfig.ID_POOL_SIZE = 100
    pool = create_id_pool(config=testconfig)
    assert len(pool) == testconfig.ID_POOL_SIZE 
    assert os.path.isfile(testconfig.ID_FILE_SAVE_PATH) == True