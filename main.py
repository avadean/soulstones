import math
import numpy.random as npr
import time

import people


if __name__ == '__main__':

    years = 1000

    dict_num = { 'null'      : 10000,
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
        persons += [people.Person(False, False, soul, math.floor(npr.normal(25, 15))) for n in range(dict_num[soul])]

    for year in range(years):
        print('starting year ' + str(year) + ' out of ' + str(years))

        start = time.time()
        for person in persons:
            person.age_up()
            person.chance_to_die(year)

        deaths  = [person for person in persons if not person.alive]
        with open('individuals.dat', 'a') as f:
            for person in deaths:
                f.write(person.soul + ' yearofdeath=' + str(person.year_of_death) + ' sex=' + person.sex + ' age=' + str(person.age) + ' partner=' + str(True if person.partner else     False) + ' children=' + str(person.num_children) + '\n')

        persons = [person for person in persons if person.alive]
        end   = time.time()
        #print('time to age up ' + str(end - start))

        start = time.time()
        for person in persons:
            person.find_partner(persons)
        end    = time.time()
        #print('time to find partners ' + str(end-start))

        start = time.time()
        for person in persons:
            child = person.have_child()
            if child:
                persons.append(child)
        end   = time.time()
        #print('time to have children ' + str(end-start))

        with open('yearlysummary.dat', 'a') as f:
            f.write('year ' + str(year) + ' out of ' + str(years) + '\n')
            for soul in people.dict_souls:
                num = len([True for person in persons if person.soul == soul])
                if num > 0:
                    f.write(soul + ' = ' + str(num) + '\n')

        with open('population.dat', 'a') as f:
            f.write(str(year) + ' ' + str(len(persons)) +\
                                ' ' + str(len([True for person in persons if person.soul == 'null'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'water'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'fire'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'earth'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'wind'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'light'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'dark'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'stone'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'metal'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'flying'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'ice'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'lightning'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'poison'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'ghost'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'psychic'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'nuclear'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'gravity'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'life'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'death'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'soul'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'luna'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'jade'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'dragon'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'dream'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'blood'])) +\
                                ' ' + str(len([True for person in persons if person.soul == 'arcane'])) +\
                    '\n')

    #for person in persons:
    #    print(person.soul, 'alive=' + str(person.alive) + (str(person.year_of_death) if not person.alive else ''), 'sex=' + person.sex, 'age=' + str(person.age), 'partner=' + str(True if person.partner else False), 'children=' + str(person.num_children))

    #for soul in people.dict_souls:
    #    print(soul + ' = ' + str(len([True for person in persons if person.soul == soul])))


    with open('individuals.dat', 'a') as f:
        for person in persons:
            f.write(person.soul + ' alive=' + str(person.alive) + (str(person.year_of_death) if not person.alive else '') + ' sex=' + person.sex + ' age=' + str(person.age) + ' partner=' + str(True if person.partner else False) + ' children=' + str(person.num_children) + '\n')






