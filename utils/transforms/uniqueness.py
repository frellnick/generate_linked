# draw_unique.py

"""
Draw Unique Data
    Ensure column uniqueness.  Run generators to build unique data.
"""

import pandas as pd
import numpy as np

from utils.generators import gen_registry

from settings import get_config, g

config = get_config()



def draw_unique(data, fieldname=None):
    """
    Iterate over field with generator until all values in set are unique.
    """
    if fieldname is None:
        fieldname = data.columns[0]

    def _test_unique(f:pd.Series):
        return f.nunique() == len(f)
    
    def _get_duplicate_indices(f: pd.Series, fname:str):
        vc = f.value_counts()
        dup = pd.DataFrame({'counts': vc[vc > 1]}).reset_index()
        dup.columns = [fname, 'counts']
        tdf = pd.DataFrame(f)
        tdf = tdf.merge(dup, on=fname, how='left')
        return tdf.query('counts>1').index
    
    def _redraw_duplicates(data:pd.DataFrame, fieldname:str, g):
        dup_ind = _get_duplicate_indices(data[fieldname], fieldname)
        newdf = data.iloc[dup_ind].copy()
        newdf[fieldname] = [g() for _ in range(len(newdf))]
        data.update(newdf)
        print(f'Updated {len(newdf)} records')

    
    field = data[fieldname]
    print("Drawing unique: ", fieldname)
    if not _test_unique(field):
        generator = gen_registry[fieldname]
        _redraw_duplicates(data, fieldname, generator)
        draw_unique(data, fieldname)
    
    return data



def _data_contains_fieldnames(data: pd.DataFrame, fieldnames: list) -> bool:
    for n in fieldnames:
        if n not in data.columns:
            return False
    return True


def _make_jobs(data, fieldnames):
    return [data[fieldname].to_frame(name=fieldname).copy() for fieldname in fieldnames]


def force_unique(data:pd.DataFrame, fieldnames:list):
    
    print('fieldnames: ', fieldnames)
    assert _data_contains_fieldnames(data, fieldnames)

    if config.MULTIPROCESSING:
        print('Starting processes for draw unique.')
        jobs = _make_jobs(data, fieldnames)
        uf = list(g.mpool.map(draw_unique, jobs))
        for frame in uf:
            col = frame.columns[0]
            data[col] = frame[col]
    else:
        print('Running single threaded draw unique.')
        for fieldname in fieldnames:
            print('Drawing unique column: ', fieldname)
            unique_frame = draw_unique(data[fieldname].to_frame(name=fieldname).copy())
            data[fieldname] = unique_frame[fieldname]
    
    return data