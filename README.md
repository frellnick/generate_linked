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
conda install pytest pandas numpy faker
# conda install modin[dask] ## Requires network firwall rules for DASK scheduler
# conda env create -f environment.yml
# conda activate synthgen
```


## Usage
Configure application in settings.py

Run with 
```bash
python main.py
```

## Tests
Tests written with pytest.  

Run all with: 
```bash
cd root_dir
pytest -v
```

