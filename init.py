import main

gamma       = 1.35 # Determines the probability fall-off of accepted souls.
a           = 0.00075
b           = 0.05000

years       = 7500

dict_num = { 'null'      : 15,
             'water'     : 0,
             'fire'      : 0,
             'earth'     : 0,
             'wind'      : 0,
             'light'     : 0,
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

main.run(gamma, a, b, years, dict_num)



