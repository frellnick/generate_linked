# stagepartial.py

from functools import partial


def stage_partial(fn, *args, **kwargs):
    return partial(fn, *args, **kwargs)