# test_dataset.py


import pytest 
import os
from settings import get_config, g

from utils.link.dataset import Dataset


@pytest.fixture 
def source():
    c = get_config()
    files = os.listdir(c.SOURCE_DIR)
    return os.path.join(c.SOURCE_DIR, files[0])

    
@pytest.fixture 
def transforms():
    def null_transform(data):
        return data

    return [null_transform]


def test_dataset_construction(source, transforms):
    d = Dataset(
        source=source,
        transforms=transforms
    )


def test_dataset_view_raw(source, transforms):
    d = Dataset(
        source=source,
        transforms=transforms
    )
    assert len(d.raw) > 0
