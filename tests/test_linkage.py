# test_linkage.py

import pytest 
import os
import pandas as pd
from settings import get_config, g

from utils.link.linkage import random_assignment


@pytest.fixture 
def source():
    c = get_config()
    files = os.listdir(c.SOURCE_DIR)
    return os.path.join(c.SOURCE_DIR, files[0])



def test_random_assignment(source):
    df = pd.read_csv(source).sample(100)
    linked = random_assignment(df, max_id=len(df))

    assert len(df) == len(linked)
    linked.to_csv('test_linked.csv')

