# settings.py

from assets.mappings import colmap
import inspect
import os
import json
from utils import g


class Config():
    def __init__(self, debug=True):
        super().__init__()

        self.MAPPINGS = colmap

        self.SOURCE_DIR = _mpath('data/source_samples')

        self.SAVE_POOL = True

        self.ID_FILE_PATH = _mpath('data/idpool/id_pool.csv')

        self.ID_FILE_SAVE_PATH = _mpath('data/idpool/id_pool_modified.csv')
    
        self.LINKED_DIR = _mpath('data/linked_tables')
        
        self.REPORT_DIR = _mpath('data/reports')

        self.UNIQUE_COLUMNS = True

        self.UNIQUE_FIELD_OPTIONS = [
            'ssn', 
            'ssid', 
            # 'birth_date',
            'student_id',
            # 'first_name', 
            # 'last_name',
        ]

        # Set total size of identity pool to be created or sampled
        self.ID_POOL_SIZE = 20000

        # Set proportion of identities in identity pool to be used in linkage
        self.ID_POOL_MAX_UTILIZATION = 0.95

        # Dataset Size
        self.DATASET_SIZE = 10000

        # Link Assignment ('random_assignment' (1:1) or 'random_with_repeats')
        self.ASSIGNMENT_TYPE = 'random_assignment'

        # Control native multiprocessing. Must be False if not ran from __main__ 
        self.MULTIPROCESSING = True

        self.NUM_WORKERS = 4


    def _collect_attrs(self) -> list:
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        return _to_dict([a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))])

    def export(self, path=None):
        def _format(raw):
            return raw
        if path is None:
            return json.dumps(_format(self._collect_attrs()))
        
        with open(path, 'w+') as file:
            json.dump(_format(self._collect_attrs()), file, sort_keys=True, indent=4)



## Utility Functions


def _to_dict(keyvals:list) -> dict:
    d = {}
    for kv in keyvals:
        d[kv[0]] = kv[1]
    return d

def _mpath(path):
    cp = path.split('/')
    return os.path.join(os.getcwd(), *cp)


## Factory function 

def get_config(debug=True) -> Config:
    if not hasattr(g, 'config'):
        g.config = Config(debug=debug)
    return g.config