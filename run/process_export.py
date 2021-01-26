# create_linked.py


from utils.link import create_linkage
from utils.link.linkage import Linkage
import os
import ntpath

from settings import get_config

config = get_config()



def link_sources(*args, **kwargs):
    print('Constructing linkage.')
    linkage = create_linkage()
    print('Processing linkage.')
    linkage.process()
    return linkage
    

def _path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def _generate_path(source_path, base_dir=None):
    if base_dir is None:
        base_dir = config.LINKED_DIR
    fname = _path_leaf(source_path)
    return os.path.join(base_dir, fname)


def _generate_config_report(config, *args, **kwargs):
    pass

def _generate_linkage_report(config, *args, **kwargs):
    pass

def export_linkage(linkage:Linkage, *args, **kwargs):
    # report = generate_report(linkage, *args, **kwargs)  ## TODO: Not implemented yet
    # report.save(*args, **kwargs)

    # Save the linked files
    for f in linkage.files:
        save_path = _generate_path(f.source)
        f.linked.to_csv(save_path, index=False)

    # Copy ID Pool computed for linkage
    save_path = _generate_path(linkage.idpool.source)
    linkage.idpool.compute().to_csv(save_path, index=False)

    # Save Configuration for reference
    config.export(_generate_path('CONFIG.json'))
    



