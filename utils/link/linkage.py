"""
Linkage

Collections object and general processing methods
"""


from .dataset import Dataset
import pandas as pd
import numpy as np

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


    def __repr__(self):
        return '<Linkage Object>'


    def _map_replace(self):
        pass

    def _assign_linkage(self, assignment='random'):
        assign = _load_assignment_fn(assignment)
        for f in self.files:
            f.linked = f.apply(assign, max_id=len(self.idpool))





def _load_assignment_fn(assignment):
    assignments = {
        'random': random_assignment,
    }
    return assignments[assignment]



def random_assignment(data: pd.DataFrame, *args, **kwargs):
    assert kwargs['max_id'] > 0, 'Must pass max_id > 0 for random assignment'
    id_assignments = np.random.choice(
        np.arange(kwargs['max_id']), size=len(data), replace=False)
    data['id'] = id_assignments
    return data
