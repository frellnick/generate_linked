# test_global.py

from utils import g


def test_g():
    g.test = True 
    assert hasattr(g, 'test')