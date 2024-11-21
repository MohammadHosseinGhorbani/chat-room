import random


def gen_random_code():
    return ''.join([str(random.randint(0, 9)) for i in range(5)])
