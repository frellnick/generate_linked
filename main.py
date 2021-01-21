#main.py


import argparse
import multiprocessing as mp

from run.create_identity_pool import create_id_pool
from settings import g, get_config


config = get_config()

def run(*args, **kwargs):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate Identity Pool and Linked Datasets')

    config.MULTIPROCESSING = True
    g.mpool = mp.Pool(config.NUM_WORKERS)
    
    idpool = create_id_pool()