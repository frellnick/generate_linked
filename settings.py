# settings.py

from assets.mappings import colmap
import os

class Config():
    def __init__(self):
        super().__init__()
        self.MAPPINGS = colmap

        self.SOURCE_DIR = _mpath('data/source_samples')

        self.ID_PATH = _mpath('data/idpool/id_pool_modified.csv')

        self.ID_DIR = _mpath('data/idpool')
    
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


def _mpath(path):
    cp = path.split('/')
    return os.path.join(os.getcwd(), *cp)


config = Config()