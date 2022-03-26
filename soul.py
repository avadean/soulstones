# from numpy import zeros
from openpyxl import load_workbook

soulTable = ['null',
             'water', 'fire', 'earth', 'wind', 'light',
             'dark', 'stone', 'metal', 'flying', 'ice',
             'lightning', 'poison', 'ghost', 'psychic', 'nuclear', 'gravity', 'life', 'death',
             'soul', 'luna', 'jade', 'dragon', 'dream', 'blood', 'arcane']

# soulTable = {0: 'null'}

path = "/Users/Ava/OneDrive/Documents/writing/Soulstones NEW/Soulstones.xlsx"
wb_obj = load_workbook(path)
sheet_obj = wb_obj.active
cell_obj = sheet_obj['C3' : 'AB28']

soulDict = {fatherSoul: {motherSoul: cell_obj[nF][nM].value
                         for nM, motherSoul in enumerate(soulTable)}
            for nF, fatherSoul in enumerate(soulTable)}


def getSoul(A=None, B=None):
    father, mother = (A, B) if A.sex == 'M' else (B, A)

    soul = soulDict.get(father.soul).get(mother.soul)

    soul = 'null' if soul is None else soul

    soul = soul.strip().lower()

    return soul


'''
def createNulls(num: int = 1):
    assert type(num) is int

    return zeros(shape=(num,), dtype=int)
'''
