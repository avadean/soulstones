# A change.

import person


if __name__ == '__main__':

    num_dict = { 'null'      : 10,
                 'water'     : 5,
                 'fire'      : 3,
                 'earth'     : 7,
                 'wind'      : 8,
                 'light'     : 10,
                 'dark'      : 0,
                 'stone'     : 0,
                 'metal'     : 0,
                 'flying'    : 0,
                 'ice'       : 0,
                 'lightning' : 0,
                 'poison'    : 0,
                 'ghost'     : 0,
                 'psychic'   : 0,
                 'nuclear'   : 0,
                 'gravity'   : 0,
                 'life'      : 0,
                 'death'     : 0,
                 'soul'      : 0,
                 'luna'      : 0,
                 'jade'      : 0,
                 'dragon'    : 0,
                 'dream'     : 0,
                 'blood'     : 0,
                 'arcane'    : 0
                }

    persons = []
    for soul in num_dict:
        persons += [person.InitialPerson(soul) for n in range(num_dict[soul])]




