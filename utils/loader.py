# loader.py


import pandas as pd
import os



def load(fpath, **kwargs):
    return pd.read_csv(fpath, low_memory=False, **kwargs)


def get_path_names(dirpath):
    fdirectory = {}
    for fname in os.listdir(dirpath):
        fdirectory[fname] = os.path.join(dirpath, fname)
    return fdirectory