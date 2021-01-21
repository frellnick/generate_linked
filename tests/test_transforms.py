# test_transforms.py


from utils.transforms import stage_partial
import pytest



@pytest.fixture
def test_fn():
    def add(n1, n2):
        return n1 + n2
    return add


def test_stage_partial(test_fn):
    pfn = stage_partial(test_fn, 2)
    sum = pfn(2)
    assert sum == 4