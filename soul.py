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
    father, mother = (A, B) if A.sex == 'M' else (B, A)

    return soulTable.get(father.soul, None).get(mother.soul, None)


'''
def createNulls(num: int = 1):
    assert type(num) is int

    return zeros(shape=(num,), dtype=int)
'''
