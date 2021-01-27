"""
Linkage

Collections object and general processing methods
"""


from .dataset import Dataset
import pandas as pd
import numpy as np


from assets.mappings import colmap
from settings import get_config, g
import warnings

config = get_config()


class Linkage():
    """
    Linkage

    params
    ------
    files: list of datasets with sources loaded
    idpool: idpool dataset
    """
    def __init__(self, files:list, idpool:Dataset):
        self.files = files 
        self.idpool = idpool
        self._assigned = False


    def __repr__(self):
        return '<Linkage Object>'

    def _assign_linkage(self, assignment=None):
        if assignment is None:
            assignment = config.ASSIGNMENT_TYPE
        assign = _load_assignment_fn(assignment)
        id_list = self.idpool.compute()['id_pool'].unique()
        for f in self.files:
            f.linked = f.apply(assign, id_list=id_list)
        self._assigned = True

    def _multiprocess_merge_with_pool(self):
        jobs = list(zip(
            [f.linked for f in self.files], 
            [self.idpool.compute() for _ in range(len(self.files))]
        ))
        uf = list(g.mpool.map(merge_with_pool, jobs))
        for i, f in enumerate(self.files):
            f.linked = uf[i]

    def _multiprocess_swap_mapped_and_clean(self):
        jobs = [f.linked for f in self.files]
        uf = list(g.mpool.map(swap_mapped_and_clean, jobs))
        for i, f in enumerate(self.files):
            f.linked = uf[i]

    def _replace_linked_values(self):
        if config.MULTIPROCESSING:
            self._multiprocess_merge_with_pool()
            self._multiprocess_swap_mapped_and_clean()
        else:
            for f in self.files:
                f.linked = merge_with_pool(f.linked, self.idpool.compute())
                f.linked = swap_mapped_and_clean(f.linked)

    def process(self):
        self._assign_linkage()
        self._replace_linked_values()



def _load_assignment_fn(assignment):
    assignments = {
        'random_assignment': random_assignment,
        'random_with_repeats': random_with_repeats_assignment,
    }
    return assignments[assignment]


# A 1:1 assignment row to ID.  Not for repead IDs.
def random_assignment(data: pd.DataFrame, *args, **kwargs):
    if 'max_id' in kwargs:
        id_assignments = np.random.choice(
            np.arange(kwargs['max_id']), size=len(data), replace=False)
    elif 'id_list' in kwargs:
        print(f"Assigning ids from frame of length: {len(kwargs['id_list'])}  to Data of length: {len(data)}")
        id_assignments = np.random.choice(
            kwargs['id_list'], size=len(data), replace=False)
    else:
        raise KeyError("'max_id' or 'id_list' must be provided.")

    data['id'] = id_assignments
    return data


# Random assignment allows for repeats.
def _search_keys(seta, setb):
    return [a for a in seta if a in setb]

def random_with_repeats_assignment(data: pd.DataFrame, *args, **kwargs):
    if 'colmap' not in kwargs:
        warnings.warn('colmap not provided.  Duplicate behavior controlled by default Mappings')
        id_cols = colmap.keys()
    else:
        id_cols = kwargs['colmap']

    mapped_columns = _search_keys(id_cols, data.columns)
    unique_frame = data[mapped_columns].drop_duplicates().copy()
    unique_frame = random_assignment(unique_frame, *args, **kwargs)
    return pd.merge(data, unique_frame, on=mapped_columns)



def merge_with_pool(*args) -> pd.DataFrame:
    if len(args) == 1:
        args = args[0]
    linked = args[0]
    idpool = args[1]
    assert 'id' in linked.columns, "First frame does not have id columns."
    assert 'id_pool' in idpool.columns, "Second frame does not have id_pool column."
    return pd.merge(linked, idpool, left_on='id', right_on='id_pool')


def swap_mapped_and_clean(data: pd.DataFrame) -> pd.DataFrame:
    idset = _search_keys(colmap.keys(), data.columns)

    # Change column names
    schema = {}
    for col in idset:
        schema[colmap[col]] = col

    d = data.drop(idset, axis=1)
    d.rename(schema, axis=1, inplace=True)

    # # Overwrite identifying data - DEPRECATED
    # for col in idset:
    #     data[col] = data[colmap[col]]

    # Drop pool columns
    keep = [c for c in d.columns if 'pool' not in c]
    return d[keep]

