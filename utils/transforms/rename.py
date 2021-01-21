# rename.py

import pandas as pd\

def rename_col(data:pd.DataFrame, schema:dict=None, append:str=None)->pd.DataFrame:
    if schema is not None:
        assert type(schema) == dict
        data.rename(schema, inplace=True, axis=1)
    if append is not None:
        schema = {}
        for col in data.columns:
            schema[col] = col+append
        data.rename(schema, inplace=True, axis=1)
    return data

    