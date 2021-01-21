# Synthetic Linked Dataset Generator
An application to generate linked datasets to simulate real-world and ideal scenarios for multi-source human data.


## Requirements

```yaml
python >= 3.7
Anaconda, Miniconda
```

### Miniconda Environment Setup

```bash
conda create -n synthgen python=3.8
conda activate synthgen
conda install pytest
conda install faker
# conda install modin[dask] ## Requires network firwall rules for DASK scheduler
# conda env create -f environment.yml
# conda activate synthgen
```


## Usage
Configure application in settings.py

**Specify** the following:
1. self.SOURCE_DIR - Example:  _mpath('data/source_samples')

2. self.ID_FILE_PATH - Example:  _mpath('data/idpool/id_pool.csv')

3. self.ID_FILE_SAVE_PATH - Example: _mpath('data/idpool/id_pool_modified.csv')
    
4. self.LINKED_DIR - Example:  _mpath('data/linked_tables')
        
5. self.REPORT_DIR - Example:  _mpath('data/reports')


## Tests
Tests written with pytest.  

Run all with: 
```bash
cd root_dir
pytest -v
```

