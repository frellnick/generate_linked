# transforms.py

"""
ID Transforms
    General modifications like insuring validity, uniqueness, error introduction.
"""

import pandas as pd
import numpy as np

from utils.generators import gen_registry



def draw_unique(data, fieldname):
    """
    Iterate over field with generator until all values in set are unique.
    """
    def _test_unique(f:pd.Series):
        return f.nunique() == len(f)
    
    def _get_duplicate_indices(f: pd.Series, fname:str):
        vc = f.value_counts()
        dup = pd.DataFrame({'counts': vc[vc > 1]}).reset_index()
        dup.columns = [fname, 'counts']
        tdf = pd.DataFrame(f)
        tdf = tdf.merge(dup, on=fname, how='left')
        return tdf.query('counts>1').index
    
    def _redraw_duplicates(data, fieldname, g):
        dup_ind = _get_duplicate_indices(data[fieldname], fieldname)
        newdf = data.loc[dup_ind].copy()
        newdf[fieldname] = [g() for _ in range(len(newdf))]
        data.update(newdf)
        print(f'Updated {len(newdf)} records')

        
    field = data[fieldname]
    if _test_unique(field):
        return data
    else:
        generator = gen_registry[fieldname]
        _redraw_duplicates(data, fieldname, generator)
        draw_unique(data, fieldname)


def force_unique(data, fieldnames):
    print('fieldnames: ', fieldnames)
    for fieldname in fieldnames:
        print('Drawing unique column: ', fieldname)
        draw_unique(data, fieldname)
    return data