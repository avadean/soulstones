import math
import numpy.random as npr
import time

import people


if __name__ == '__main__':

    years = 5

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

        start = time.time()
        sls = [person.soul for person in persons]
        with open('population.dat', 'a') as f:
            f.write(str(year) + ' ' + str(len(sls)) +\
                                ' ' + str(sls.count('null')) +\
                                ' ' + str(sls.count('water')) +\
                                ' ' + str(sls.count('fire')) +\
                                ' ' + str(sls.count('earth')) +\
                                ' ' + str(sls.count('wind')) +\
                                ' ' + str(sls.count('light')) +\
                                ' ' + str(sls.count('dark')) +\
                                ' ' + str(sls.count('stone')) +\
                                ' ' + str(sls.count('metal')) +\
                                ' ' + str(sls.count('flying')) +\
                                ' ' + str(sls.count('ice')) +\
                                ' ' + str(sls.count('lightning')) +\
                                ' ' + str(sls.count('poison')) +\
                                ' ' + str(sls.count('ghost')) +\
                                ' ' + str(sls.count('psychic')) +\
                                ' ' + str(sls.count('nuclear')) +\
                                ' ' + str(sls.count('gravity')) +\
                                ' ' + str(sls.count('life')) +\
                                ' ' + str(sls.count('death')) +\
                                ' ' + str(sls.count('soul')) +\
                                ' ' + str(sls.count('luna')) +\
                                ' ' + str(sls.count('jade')) +\
                                ' ' + str(sls.count('dragon')) +\
                                ' ' + str(sls.count('dream')) +\
                                ' ' + str(sls.count('blood')) +\
                                ' ' + str(sls.count('arcane')) +\
                    '\n')
        end = time.time()
        #print('time' + str(end-start))

    with open('individuals.dat', 'a') as f:
        for person in persons:
            f.write(person.soul + ' alive=' + str(person.alive) + (str(person.year_of_death) if not person.alive else '') + ' sex=' + person.sex + ' age=' + str(person.age) + ' partner=' + str(True if person.partner else False) + ' children=' + str(person.num_children) + '\n')






