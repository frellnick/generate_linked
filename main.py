#main.py


import argparse


def run(*args, **kwargs):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate Identity Pool and Linked Datasets')

    idpool = _load_process_id_pool()
    print(idpool.head())