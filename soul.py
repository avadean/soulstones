# from numpy import zeros


soulTable = \
    {'null':
        {'null': 'null',
         'water': 'null',
         'fire': 'null',
         'earth': 'null',
         'wind': 'null',
         'light': 'water',
         'dark': 'fire',

         'death': 'null'},

     'water':
        {'null': 'null',
         'water': 'water',
         'fire': 'water',
         'earth': 'earth',
         'wind': 'water',
         'light': 'null',
         'dark': 'null',

         'death': 'death'},

     'fire':
        {'null': 'null',
         'water': 'water',
         'fire': 'fire',
         'earth': 'earth',
         'wind': 'fire',
         'light': 'null',
         'dark': 'null',

         'death': 'death'},

     'earth':
        {'null': 'null',
         'water': 'earth',
         'fire': 'earth',
         'earth': 'earth',
         'wind': 'wind',
         'light': 'null',
         'dark': 'null',

         'death': 'death'},

     'wind':
        {'null': 'null',
         'water': 'water',
         'fire': 'fire',
         'earth': 'wind',
         'wind': 'wind',
         'light': 'null',
         'dark': 'null',

         'death': 'death'},

     'light':
        {'null': 'water',
         'water': 'water',
         'fire': 'fire',
         'earth': 'earth',
         'wind': 'wind',
         'light': 'light',
         'dark': 'dark',

         'death': 'death'},

     'dark':
        {'null': 'fire',
         'water': 'null',
         'fire': 'null',
         'earth': 'null',
         'wind': 'null',
         'light': 'light',
         'dark': 'death',

         'death': 'death'},

     'death':
        {'null': 'null',
         'water': 'death',
         'fire': 'death',
         'earth': 'death',
         'wind': 'death',
         'light': 'death',
         'dark': 'death',

         'death': 'death'}
     }

# soulTable = {0: 'null'}


def getSoul(A=None, B=None):
    assert A.sex != B.sex

    father, mother = (A, B) if A.sex == 'M' else (B, A)

    soulDict = soulTable.get(father.soul, None)

    assert soulDict is not None, f'Cannot find soulDict for soul {father.soul}'

    soul = soulDict.get(mother.soul, None)

    assert soul is not None, f'Cannot find soul for soul {mother.soul}'

    return soul


'''
def createNulls(num: int = 1):
    assert type(num) is int

    return zeros(shape=(num,), dtype=int)
'''
