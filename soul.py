from openpyxl import load_workbook
from random import choices

from inout import writeSoulDict


PATH = "/Users/Ava/OneDrive/Documents/writing/Soulstones NEW/Soulstones.xlsx"
CELLS = ('C3', 'AB28')


def getSoulDict(souls: list = None, path: str = None, cellRange: tuple = None):
    """ Get the soul dictionary which defines the resultant soul
        based off the parents. This comes from a specified Excel
        file where the cell range must be given. """

    assert type(souls) is list
    assert all(type(s) is str for s in souls)
    assert type(path) is str
    assert type(cellRange) is tuple
    assert len(cellRange) == 2

    start, end = cellRange

    workbook = load_workbook(filename=PATH, read_only=True, data_only=True)

    sheet = workbook.active

    cells = sheet[start:end]

    s = {motherSoul: {fatherSoul: cells[nM][nF].value if cells[nM][nF].value is None else cells[nM][nF].value.lower()
                      for nF, fatherSoul in enumerate(soulTable)}
         for nM, motherSoul in enumerate(soulTable)}

    return s


def getSoul(A=None, B=None):
    """ Get the soul of a person based off parents.
        If the resultant soul is null, it is returned
        as a None value in the anticipation that it is
        updated in a batch process later. """

    fatherSoul, motherSoul = (A.soul, B.soul) if A.sex == 'M' else (B.soul, A.soul)

    return soulDict.get(motherSoul).get(fatherSoul)


def getSouls(n: int = 0):
    """ Get a given number of souls based off pre-
        defined probabilities. These souls are expected
        to pass through here because they have initially
        been assigned the value of 'null' (None). """

    return choices(soulTable, k=n, weights=probs)


def createSouls(fill: int = None, **kwargs):
    """ Create souls based on soul type given in kwargs.
        If fill is specified then any remaining souls that
        have no explicit type are given null. """

    if fill is not None:
        assert type(fill) is int
        assert fill >= sum(kwargs.values()), 'Null filler less than number of specified souls'

    assert all(s in soulTable for s in kwargs)
    assert all(type(v) is int for v in kwargs.values())

    souls = sum([[soul] * n for soul, n in kwargs.items()], [])

    if fill is not None:
        souls += ['null'] * (fill - len(souls))

    return souls


# Rarity of souls.
commons = ['null']
uncommons = ['water', 'fire', 'earth', 'wind', 'light']
rares = ['dark', 'stone', 'metal', 'flying', 'ice']
epics = ['lightning', 'poison', 'ghost', 'psychic', 'nuclear', 'gravity', 'life', 'death']
legendaries = ['soul', 'luna', 'jade', 'dragon', 'dream', 'blood', 'arcane']

# Probability of falling into a rarity of soul.
probUncommon = 0.01
probRare = 0.001
probEpic = 0.0001
probLegendary = 0.00001
probCommon = 1.0 - probUncommon - probRare - probEpic - probLegendary

# Probability of each soul in each rarity category.
probUncommons = [0.25, 0.25, 0.2, 0.2, 0.1]
probRares = [0.4, 0.15, 0.15, 0.15, 0.15]
probEpics = [0.2, 0.2, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05]
probLegendaries = [0.2, 0.2, 0.2, 0.125, 0.125, 0.075, 0.075]
probCommons = [1.0]

# Getting the overall probability of a soul.
probUncommons = [p * probUncommon for p in probUncommons]
probRares = [p * probRare for p in probRares]
probEpics = [p * probEpic for p in probEpics]
probLegendaries = [p * probLegendary for p in probLegendaries]
probCommons = [p * probCommon for p in probCommons]

# Compile probabilities together.
probs = probCommons\
        + probUncommons\
        + probRares\
        + probEpics\
        + probLegendaries

# Compile souls together.
soulTable = commons\
            + uncommons\
            + rares\
            + epics\
            + legendaries

# Zipped up dictionary if needed.
soulProbs = dict(zip(soulTable, probs))

# Soul dictionary from Excel file.
soulDict = getSoulDict(souls=soulTable, path=PATH, cellRange=CELLS)

writeSoulDict(soulDict)
