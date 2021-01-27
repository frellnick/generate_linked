#generators.py


import numpy as np
from faker import Faker
from settings import get_config, g
import json

config = get_config()
fake = Faker()
gen_registry = {}



def _check_default_num(*args) -> int:
    if len(args) > 0:
        assert type(args[0]) == int, f'Must pass an integer number of values to generator. Passed {args[0]}'
        return args[0]
    return 1


def ssn(*args, **kwargs) -> list:
    n = _check_default_num(*args)
    def _collect():
        return np.random.randint(111111111, 999999999)
    return [_collect() for _ in range(n)]
gen_registry['ssn'] = ssn
gen_registry['student_id'] = ssn


def ssid(*args, **kwargs) -> list:
    n = _check_default_num(*args)
    def _collect():
        v = np.random.randint(111111111, 999999999)
        return ''.join([hex(v), hex(v*2)])
    return [_collect() for _ in range(n)]
gen_registry['ssid'] = ssid


def name(*args, **kwargs) -> list:
    n = _check_default_num(*args)
    def _combined():
        return fake.name().replace(' ', '-')

    def _combined_reversed():
        n = fake.name().split(' ')
        n.reverse()
        return '-'.join(n)

    def _single():
        return fake.first_name()
    
    def _single_last():
        return fake.last_name()

    def _single_first_prefix():
        return ' '.join([fake.prefix(), fake.first_name()])

    def _combined_suffix():
        n = fake.name().replace(' ', '-')
        return ' '.join([n, fake.suffix()])

    def _select_from_file(n=1):
        if not hasattr(g, 'names'):
            with open(config.NAMES_FILE, 'r') as file:
                g.names = np.array(json.load(file))

        names = [str(x) for x in np.random.choice(g.names, n, replace=False)]
        return names

    # fns = {
    #     0:_combined,
    #     1:_combined_reversed,
    #     2:_single,
    #     3:_single_last,
    #     4:_single_first_prefix,
    #     5:_combined_suffix,
    #     6:_select_from_file,
    # }
    # i = np.random.randint(0, len(fns))
    # fn = fns[i]
    # return fn()
    return _select_from_file(n)
gen_registry['first_name'] = name 
gen_registry['last_name'] = name
gen_registry['middle_name'] = name 


def birth_date(*args, **kwargs) -> list:
    n = _check_default_num(*args)
    def _collect():
        dd = str(np.random.randint(1,28))
        mm = str(np.random.randint(1, 12))
        yyyy = str(np.random.randint(1200, 3000))
        return '/'.join([mm, dd, yyyy])
    return [_collect() for _ in range(n)]
gen_registry['birth_date'] = birth_date


def student_id(*args, **kwargs) -> list:
    n = _check_default_num(*args)
    def _collect():
        return np.random.randint(0, 999999999)
    return [_collect() for _ in range(n)]
gen_registry['student_id'] = student_id


def gender(*args, **kwargs) -> list:
    n = _check_default_num(*args)
    def _collect():
        return np.random.choice(['m', 'f', 'n', 'u'])
    return [_collect() for _ in range(n)]
gen_registry['gender'] = gender