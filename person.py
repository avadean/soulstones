from numpy import arange, ceil, exp, floor
from numpy.random import choice, normal, random
from random import choices, randint

from soul import soulTable

MIN_PARTNER_AGE = 16
MAX_PARTNER_AGE = 65

MIN_CHILD_AGE = 18
MAX_CHILD_AGE = 45

INIT_CHANCE_DEATH = 0.0001  #0.001
EXPO_CHANCE_DEATH = 0.078   #0.051
MAX_AGE = 150

deathProbs = INIT_CHANCE_DEATH * exp(EXPO_CHANCE_DEATH * arange(MAX_AGE))


def createPersons(num: int = None, maxAge: int = 100):
    assert type(num) is int
    assert type(maxAge) is int

    return [Person(soul='null',
                   age=randint(0, 100)) for _ in range(num)]


def chanceOfDeath(age: int = None):
    assert type(age) is int
    assert age <= MAX_AGE, 'Age too high.'

    return random() < deathProbs[age]


def tryChildren(persons: list = None):
    assert type(persons) is list
    assert all(type(person) is Person for person in persons)

    partneredPersons = [person for person in persons if person.partner is not None]

    babies = []

    for person in partneredPersons:
        A, B = person, person.partner

        # Random chance to not want children this year and things not working out by chance.
        if random() < 0.125:
            continue

        # Check they've not already had a child this year.
        if A.childThisYear or B.childThisYear:
            continue

        # Check they still want more children.
        if len(A.children) >= A.numChildrenWanted or len(B.children) >= B.numChildrenWanted:
            continue

        # Check they're not too young.
        if A.age < MIN_CHILD_AGE or B.age < MIN_CHILD_AGE:
            continue

        # Check they're not too old.
        if A.age > MAX_CHILD_AGE or B.age > MAX_CHILD_AGE:
            continue

        # Check they're at least the age they want to be.
        if A.age < A.minChildWantAge or B.age < B.minChildWantAge:
            continue

        # Check they're not above the age they want to be.
        if A.age > A.maxChildWantAge or B.age > B.maxChildWantAge:
            continue

        # We have a baby!
        baby = Person(soul='null',  # TODO: souls.
                      age=0,
                      parents=[A, B],
                      siblings=list(set(A.children + B.children)))

        A.addChild(baby)
        B.addChild(baby)

        babies.append(baby)

    return babies


def tryPartners(persons: list = None):
    assert type(persons) is list
    assert all(type(person) is Person for person in persons)

    # Try "the SINGLE population" number of times to set up partners.

    singlePersons = [person for person in persons if person.partner is None]

    #for _ in range(len(singlePersons)):  # // 2):
    for A in singlePersons:
        '''
        # Select two people at random.
        A, B = choices(singlePersons, k=2)
        '''

        # k attempts of finding love this year.
        for B in choices(singlePersons, k=3):
            '''
            # Random chance things don't work out!
            if random() < 0.5:
                continue
            '''

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
    def __init__(self, soul: str = 'null', age: int = 0,
                 parents: list = None, siblings: list = None):

        assert type(soul) is str
        soul = soul.strip().lower()
        assert soul in soulTable

        assert type(age) is int
        assert age >= 0, 'Age of person must be >= 0.'

        if parents is not None:
            assert type(parents) is list
            assert all(type(person) is Person for person in parents)

        if siblings is not None:
            assert type(siblings) is list
            assert all(type(sibling) is Person for sibling in siblings)

        self.soul = soul
        self.age = age
        self.parents = parents if parents is not None else []
        self.siblings = siblings if siblings is not None else []

        self.alive = True
        self.sex = 'M' if random() < 0.5 else 'F'
        self.partner = None
        self.children = []
        self.numChildrenWanted = choice([0, 1, 2, 3, 4, 5], size=1, p=[0.05, 0.1, 0.2, 0.35, 0.2, 0.1])
        self.minChildWantAge = ceil(normal(25, 5))
        self.maxChildWantAge = floor(normal(45, 5))

        self.childThisYear = False

    def __repr__(self):
        #return f'{str(id(self))[-5:]}+{str(id(self.partner))[-5:] if self.partner is not None else "None"}     '
        return f'({self.soul}, {self.age})'

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
