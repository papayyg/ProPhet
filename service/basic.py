from random import randint


async def random_l(matches):
    a, b = sorted(map(int, matches))
    return randint(a, b)
