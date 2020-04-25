import time

import people


if __name__ == '__main__':

    years = 2

    dict_num = { 'null'      : 100000,
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

    persons = []
    for soul in dict_num:
        persons += [people.Person(False, False, soul) for n in range(dict_num[soul])]

    for year in range(years):

        start = time.time()
        for person in persons:
            person.age_up()
            person.chance_to_die(year)
        end   = time.time()
        print('time to age up ' + str(end - start))

        start = time.time()
        for person in persons:
            person.find_partner(persons)
        end    = time.time()
        print('time to find partners ' + str(end-start))

        start = time.time()
        for person in persons:
            child = person.have_child()
            if child:
                persons.append(child)
        end   = time.time()
        print('time to have children ' + str(end-start))

    #for person in persons:
    #    print(person.soul, 'alive=' + str(person.alive) + (str(person.year_of_death) if not person.alive else ''), 'sex=' + person.sex, 'age=' + str(person.age), 'partner=' + str(True if person.partner else False), 'children=' + str(person.num_children))

    #for soul in people.dict_souls:
    #    print(soul + ' = ' + str(len([True for person in persons if person.soul == soul])))







