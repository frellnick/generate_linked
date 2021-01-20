# test_config.py

from settings import get_config
import pytest 


@pytest.fixture 
def cfg():
    return get_config()


def test_config(cfg):
    assert cfg.MAPPINGS is not None
