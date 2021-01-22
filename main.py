#main.py


import argparse
import multiprocessing as mp

from run import create_id_pool, link_sources, export_linkage
from settings import g, get_config

import time


config = get_config()

def time_step(fn, fname, *args, **kwargs):
    s = time.time()
    print(f"Starting {fname}")
    out = fn(*args, **kwargs)
    print(f"Completed {fname} in {time.time() - s}.")
    return out



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate Identity Pool and Linked Datasets')

    start = time.time()

    config.MULTIPROCESSING = True
    g.mpool = mp.Pool(config.NUM_WORKERS)
    
    # Create an ID Pool - Will save modified to disk
    idpool = time_step(create_id_pool, 'create_id_pool')

    # Create default linkage
    linkage = time_step(link_sources, 'link_sources')

    # Export linkage with default paramaters
    export_linkage(linkage=linkage)
