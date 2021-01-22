# test_linkage.py

import pytest 
import os
import pandas as pd
from settings import get_config, g

from utils.link.linkage import (
    random_assignment, 
    random_with_repeats_assignment,
    merge_with_pool,
    swap_mapped_and_clean
)
from utils.link.replace import (
    load_id_pool
)

@pytest.fixture 
def source():
    c = get_config()
    files = os.listdir(c.SOURCE_DIR)
    return os.path.join(c.SOURCE_DIR, files[0])



def test_random_assignment(source):
    df = pd.read_csv(source).sample(100)
    linked = random_assignment(df, max_id=len(df))

    assert len(df) == len(linked)
    assert 'id' in linked.columns


def test_random_with_repeats_assignment(source):
    df = pd.read_csv(source).sample(100)
    linked = random_with_repeats_assignment(df, max_id=len(df))

    assert len(df) == len(linked)
    assert 'id' in linked.columns


def test_merge_with_pool(source):
    df = pd.read_csv(source).sample(100)
    idpool = load_id_pool().compute()
    id_list = idpool['id_pool'].unique()
    linked = random_assignment(df, id_list=id_list)
    linked = merge_with_pool(linked=linked, idpool=idpool)


def test_swap_mapped_and_clean(source):
    df = pd.read_csv(source).sample(100)
    idpool = load_id_pool().compute()
    id_list = idpool['id_pool'].unique()
    linked = random_assignment(df, id_list=id_list)
    linked = merge_with_pool(linked=linked, idpool=idpool)
    ssn_pool = linked['ssn_pool']
    linked = swap_mapped_and_clean(linked)
    assert linked['SSN'][0] == ssn_pool[0]