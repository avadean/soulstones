from numpy.random import random

from soul import knownSouls


def createPersons(num: int = None):
    assert num is not None, 'Specify number of persons to create.'
    assert type(num) is int

    return [Person(soul='null',
                   age=0) for _ in range(num)]


class Person:
    def __init__(self, soul: str = 'null', age: int = 0):
        assert type(soul) is str
        soul = soul.strip().lower()
        assert soul in knownSouls

        assert type(age) is int
        assert age >= 0, 'Age of person must be >= 0.'

        self.soul = soul
        self.age = age

        self.alive = True
        self.sex = 'M' if random() < 0.5 else 'F'

    def ageUp(self):
        self.age += 1
