from numpy import arange, ceil, exp, floor
from random import choices

from inout import writeMythical
from soul import createSouls, getSoul, mythicals

MIN_PARTNER_AGE = 16
MAX_PARTNER_AGE = 65

MIN_CHILD_AGE = 18
MAX_CHILD_AGE = 45

INIT_CHANCE_DEATH = 0.0001  #0.001
EXPO_CHANCE_DEATH = 0.078   #0.051
MAX_AGE = 150

deathProbs = INIT_CHANCE_DEATH * exp(EXPO_CHANCE_DEATH * arange(MAX_AGE))

NUM_CHILDREN_WANTEDS = (0, 1, 2, 3, 4, 5)
WGT_CHILDREN_WANTEDS = (0.05, 0.1, 0.225, 0.325, 0.2, 0.1)

SEXES = ('M', 'F')


def createPersons(r, num: int = None,
                  minAge: int = 0, maxAge: int = 100,
                  **kwargs):

    assert 'null' not in kwargs, 'No need to specify nulls in souls'

    souls = createSouls(fill=num, **kwargs)

    ages = r.integers(low=minAge, high=maxAge, size=num)

    persons = [Person(soul=soul, age=int(age)) for soul, age in zip(souls, ages)]

    batchUpdate(r, persons)

    return persons


def chancesOfDeath(r, ages: list = None):
    return r.random(size=len(ages)) < deathProbs[ages]


def batchUpdate(r, persons: list = None):
    n = len(persons)

    sexes = choices(SEXES, k=n)
    numChildrenWanteds = choices(NUM_CHILDREN_WANTEDS, k=n, weights=WGT_CHILDREN_WANTEDS)
    minChildWantAges = ceil(r.normal(loc=25, scale=5, size=n))
    maxChildWantAges = floor(r.normal(loc=45, scale=5, size=n))

    for num, p in enumerate(persons):
        if p.soul in mythicals:
            writeMythical(p)

        p.sex = sexes[num]
        p.numChildrenWanted = numChildrenWanteds[num]
        p.minChildWantAge = minChildWantAges[num]
        p.maxChildWantAge = maxChildWantAges[num]


def tryChildren(r, persons: list = None):
    babies = []

    randoms = r.random(size=len(persons)) < 0.125

    for person, rand in zip(persons, randoms):
        # Can only have a child if the person has a partner.
        if person.partner is None:
            continue

        # Random chance to not want children this year and things not working out by chance.
        if rand:
            continue

        A, B = person, person.partner

        # Check they still want more children.
        if len(A.children) >= A.numChildrenWanted or len(B.children) >= B.numChildrenWanted:
            continue

        # Check they're not above the age they want to be.
        if A.age > A.maxChildWantAge or B.age > B.maxChildWantAge:
            continue

        # Check they're not too old.
        if A.age > MAX_CHILD_AGE or B.age > MAX_CHILD_AGE:
            continue

        # Check they're not too young.
        if A.age < MIN_CHILD_AGE or B.age < MIN_CHILD_AGE:
            continue

        # Check they've not already had a child this year.
        if A.childThisYear or B.childThisYear:
            continue

        # Check they're at least the age they want to be.
        if A.age < A.minChildWantAge or B.age < B.minChildWantAge:
            continue

        # We have a baby!
        baby = Person(soul=getSoul(A, B),
                      age=0,
                      parents=[A, B],
                      siblings=list(set(A.children + B.children)))

        A.addChild(baby)
        B.addChild(baby)

        babies.append(baby)

    batchUpdate(r, babies)

    return babies


def tryPartners(persons: list = None):
    singlePersons = [person for person in persons if person.partner is None]
    nonNullPersons = [person for person in singlePersons if person.soul != 'null']

    # 'a' attempts of finding love for each person.
    a = 3
    #potentialPartners = choices(singlePersons, k=a*len(singlePersons))

    for n, A in enumerate(singlePersons):

        if A.soul == 'null':
            potentialPartners = choices(singlePersons, k=a)
        else:
            potentialPartners = choices(nonNullPersons, k=a)

        for B in potentialPartners:#[n:n+a]:
            # Make sure they're not taken. Remember this can be updated mid-loop so we do need this check here.
            if A.partner is not None or B.partner is not None:
                continue

            # Gotta be able to make babies! This will also catch if A==B.
            if A.sex == B.sex:
                continue

            # Make sure they're not out of suitable range of each other.
            if abs(A.age - B.age) > 10:
                continue

            # Make sure they're not too young.
            if A.age < MIN_PARTNER_AGE or B.age < MIN_PARTNER_AGE:
                continue

            '''
            # Make sure they're not too old.
            if A.age > MAX_PARTNER_AGE or B.age > MAX_PARTNER_AGE:
                continue
            '''

            # Make sure they're not related.
            if A in (*B.parents, *B.children, *B.siblings) or B in (*A.parents, *A.children, *A.siblings):
                continue

            # We have a match!
            A.addPartner(B)
            B.addPartner(A)

            break


class Person:
    __slots__ = ('soul', 'age', 'parents', 'siblings',
                 'alive', 'sex', 'partner', 'children',
                 'numChildrenWanted', 'minChildWantAge', 'maxChildWantAge',
                 'childThisYear')

    def __init__(self, soul: str = None, age: int = 0,
                 parents: list = None, siblings: list = None):

        self.soul = soul
        self.age = age
        self.parents = parents if parents is not None else []
        self.siblings = siblings if siblings is not None else []

        self.alive = True
        self.partner = None
        self.children = []

        self.childThisYear = False

    def __repr__(self):
        #return f'{str(id(self))[-5:]}+{str(id(self.partner))[-5:] if self.partner is not None else "None"}     '
        return f'({self.soul}, {self.age})'

    def __str__(self):
        return f'{self.soul:>10}    {self.age:>3}{self.sex}    alive={self.alive:5<}    partner={bool(self.partner):5<}    children={len(self.children)}/{self.numChildrenWanted}'

    def __bool__(self):
        return True

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def ageUp(self):
        self.age += 1

    def die(self):
        self.alive = False

    def addChild(self, child):
        self.children.append(child)
        self.childThisYear = True

    def addPartner(self, partner):
        self.partner = partner

    def losePartner(self):
        self.partner = None
