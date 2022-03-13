from numpy import arange, asarray, ceil, concatenate, exp, floor, full, zeros
from numpy.random import choice, normal, randint, random

from soul import createNulls, soulTable

MIN_PARTNER_AGE = 16
MAX_PARTNER_AGE = 65

MIN_CHILD_AGE = 18
MAX_CHILD_AGE = 45

INIT_CHANCE_DEATH = 0.0001  #0.001
EXPO_CHANCE_DEATH = 0.078   #0.051
MAX_AGE = 150

deathProbs = INIT_CHANCE_DEATH * exp(EXPO_CHANCE_DEATH * arange(MAX_AGE))


def initPopulation(num: int = None, minAge: int = 0, maxAge: int = 100):
    assert type(num) is int
    assert type(minAge) is int
    assert type(maxAge) is int

    souls = createNulls(num)  # TODO: soulstones
    ages = randint(low=minAge, high=maxAge, size=(num,), dtype=int)

    return Population(souls, ages)


def createBabies(souls=None):
    souls = asarray(souls, dtype=int)
    ages = zeros(shape=(len(souls),), dtype=int)

    return Population(souls, ages)


def chanceOfDeath(ages=None):
    ages = asarray(ages, dtype=int)

    assert (ages <= MAX_AGE).all(), 'An age is too high.'

    return random(size=len(ages)) < deathProbs[ages]


class Population:
    def __init__(self, souls=None, ages=None):
        self.souls = asarray(souls, dtype=int)
        self.ages = asarray(ages, dtype=int)

        assert all(soul in soulTable for soul in self.souls)
        assert (self.ages >= 0).all()

        self.pop = len(self.souls)

        self.alive = full(shape=(self.pop,), fill_value=True, dtype=bool)
        self.females = choice(a=(True, False), size=(self.pop,))

        self.children = zeros(shape=(self.pop,), dtype=int)
        self.numChildrenWanted = choice([0, 1, 2, 3, 4, 5], size=self.pop, p=[0.05, 0.1, 0.2, 0.35, 0.2, 0.1])
        self.minChildWantAge = ceil(normal(loc=25, scale=5, size=self.pop)).astype(int)
        self.maxChildWantAge = floor(normal(loc=45, scale=5, size=self.pop)).astype(int)
        self.childThisYear = full(shape=(self.pop,), fill_value=False, dtype=bool)

    def __len__(self):
        return len(self.souls)

    def __repr__(self):
        return f'pop={len(self.souls)}'

    def __add__(self, other):
        assert isinstance(other, Population)

        self.souls = concatenate((self.souls, other.souls), axis=0)
        self.ages = concatenate((self.ages, other.ages), axis=0)

        self.pop += other.pop

        self.alive = concatenate((self.alive, other.alive), axis=0)
        self.females = concatenate((self.females, other.females), axis=0)

        self.children = concatenate((self.children, other.children), axis=0)
        self.numChildrenWanted = concatenate((self.numChildrenWanted, other.numChildrenWanted), axis=0)
        self.minChildWantAge = concatenate((self.minChildWantAge, other.minChildWantAge), axis=0)
        self.maxChildWantAge = concatenate((self.maxChildWantAge, other.maxChildWantAge), axis=0)
        self.childThisYear = concatenate((self.childThisYear, other.childThisYear), axis=0)

        return self

    def __iadd__(self, other):
        return self.__add__(other)

    def ageUp(self):
        self.ages += 1

    def calibrate(self):
        self.pop = len(self.souls)
        self.childThisYear = full(shape=(self.pop,), fill_value=False, dtype=bool)

    def deaths(self, deaths=None):
        survive = ~asarray(deaths, dtype=bool)

        self.souls = self.souls[survive]
        self.ages = self.ages[survive]
        self.alive = self.alive[survive]
        self.females = self.females[survive]
        self.children = self.children[survive]
        self.numChildrenWanted = self.numChildrenWanted[survive]
        self.minChildWantAge = self.minChildWantAge[survive]
        self.maxChildWantAge = self.maxChildWantAge[survive]
        #self.childThisYear = self.childThisYear[survive]

    def numBirths(self):
        # Each person in the population thinks about having a children with a random person each year.

        num = 0

        # TODO: can speed this up

        for A in range(self.pop):
            B = randint(low=0, high=self.pop, size=1, dtype=int)

            # Random chance to not want children this year or things not working out.
            if random() < 0.125:
                continue

            # Check they've not already had a child this year.
            if self.childThisYear[A] or self.childThisYear[B]:
                continue

            # Check they still want more children.
            if self.children[A] >= self.numChildrenWanted[A] or self.children[B] >= self.numChildrenWanted[B]:
                continue

            # Check they're not too young.
            if self.ages[A] < MIN_CHILD_AGE or self.ages[B] < MIN_CHILD_AGE:
                continue

            # Check they're not too old.
            if self.ages[A] > MAX_CHILD_AGE or self.ages[B] > MAX_CHILD_AGE:
                continue

            # Check they're at least the age they want to be.
            if self.ages[A] < self.minChildWantAge[A] or self.ages[B] < self.minChildWantAge[B]:
                continue

            # Check they're not above the age they want to be.
            if self.ages[A] > self.maxChildWantAge[A] or self.ages[B] > self.maxChildWantAge[B]:
                continue

            # We have a baby!
            num += 1

        return num
