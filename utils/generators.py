#generators.py


import numpy as np
from faker import Faker

fake = Faker()
gen_registry = {}



def ssn(*args, **kwargs):
    return np.random.randint(111111111, 999999999)
gen_registry['ssn'] = ssn
gen_registry['student_id'] = ssn


def ssid(*args, **kwargs):
    v = np.random.randint(111111111, 999999999)
    return ''.join([hex(v), hex(v*2)])
gen_registry['ssid'] = ssid


def name(*args, **kwargs):
    return '-'.join(
        [
            *[*args,
            *np.random.choice(
                fake.name().split()
            )],
        ]
    )
gen_registry['first_name'] = name 
gen_registry['last_name'] = name
gen_registry['middle_name'] = name 


def birth_date(*args, **kwargs):
    dd = str(np.random.randint(1,28))
    mm = str(np.random.randint(1, 12))
    yyyy = str(np.random.randint(1200, 3000))
    return '/'.join([mm, dd, yyyy])
gen_registry['birth_date'] = birth_date


def student_id(*args, **kwargs):
    return np.random.randint(0, 999999999)
gen_registry['student_id'] = student_id


def gender(*args, **kwargs):
    return np.random.choice(['m', 'f', 'n', 'u'])
gen_registry['gender'] = gender