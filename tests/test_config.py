# test_config.py


import pytest 


@pytest.fixture 
def cfg():
    from settings import config 
    return config


def test_config(cfg):
    assert cfg.MAPPINGS is not None