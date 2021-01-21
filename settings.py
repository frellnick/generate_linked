# settings.py

from assets.mappings import colmap
import os
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
            'birth_date',
            'student_id',
            # 'first_name', 
            # 'last_name',
        ]

        # Set total size of identity pool to be created or sampled
        self.ID_POOL_SIZE = 20000

        # Set proportion of identities in identity pool to be used in linkage
        self.ID_POOL_MAX_UTILIZATION = 1.0

        # Dataset Size
        self.DATASET_SIZE = 1000


        # Control native multiprocessing. Must be False if not ran from __main__ 
        self.MULTIPROCESSING = False

        self.NUM_WORKERS = 4



def _mpath(path):
    cp = path.split('/')
    return os.path.join(os.getcwd(), *cp)


def get_config(debug=True) -> Config:
    if not hasattr(g, 'config'):
        g.config = Config(debug=debug)
        
    return g.config