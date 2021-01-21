# test_replace.py


from utils.link.replace import get_id_pool
from utils.link.dataset import Dataset


def test_id_pool_instantiation():
    idpool = get_id_pool()
    assert idpool is not None
    assert type(idpool) == Dataset