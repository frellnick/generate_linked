# test_run.py


from run import link_sources



def test_link_sources():
    linkage = link_sources()
    for f in linkage.files:
        assert hasattr(f, 'linked')


def test_export_linkage():
    pass