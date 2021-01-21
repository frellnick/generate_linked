"""
Dataset

Base class for lazy load and transformations
"""

from utils.loader import load
import pandas as pd
import functools


class Dataset():
    def __init__(self, source:str, transforms:list):
        self.source = source
        self.transforms = transforms
        self._computed = False
        self._transformed = pd.DataFrame()


    def __repr__(self):
        return f'<Dataset> from source: {self.source}.  Transforms: {self.transforms}'


    def __len__(self):
        if self._computed:
            return len(self.compute())
        else:
            return 0


    @functools.cached_property
    def raw(self):
        return load(self.source)
    

    def compute(self):
        if self._computed:
            return self._transformed
        
        self._computed = True
        df = load(self.source)
        for t in self.transforms:
            df = t(df)
        self._transformed = df.copy()
        return df


    def apply(self, fn, *args, **kwargs):
        if not self._computed:
            self.compute()
        
        return fn(self._transformed, *args, **kwargs)