import gc
import os
import math
import numpy.random as npr
import time

import people


def calc_soul_probs(gamma):
    father_list = {} # For each father...
    for soul_father in people.dict_souls:
        mother_list = {} # ... and mother combination...
        for soul_mother in people.dict_souls:
            prob_list = [] # ... there is a probability list.

            total = 0.0 # To normalise.
            for soul in people.dict_souls: # Looping through all the possible souls that this new person could be.
                soul_prob = 0.0 # Probability of being this soul.

                for power, accepted_souls in enumerate(people.dict_souls[soul], 1): # Accepted souls are those that this soul accepts as increasing its chances of occuring.
                    for accepted_soul in accepted_souls: # There's a list of accepted souls for each power.
                        num_parents = (1 if soul_father == accepted_soul else 0) + (1 if soul_mother == accepted_soul else 0) # Number of parents that are accepted soul.
                        if num_parents > 0: # Only increases the chances of this soul occuring if there are parents with this accepted soul.
                            soul_prob += math.exp(-1 * (gamma ** power) / num_parents)

                prob_list.append(soul_prob)
                total += soul_prob

            mother_list[soul_mother] = [p / total for p in prob_list]

        father_list[soul_father] = mother_list

    return father_list

def calc_chance_die(a, b):
    age   = 0
    prob  = 0.0
    probs = {}

    while prob <= 1.0:
        prob       = a * math.exp(b * float(age))
        probs[age] = prob
        age       += 1

    return probs


def run(gamma, a, b, years, dict_num):
    START_TOTAL=time.time()
    souls       = [soul for soul in people.dict_souls]

    START=time.time()
    soul_probs  = calc_soul_probs(gamma)
    END=time.time()
    time_calc_soul_probs=END-START

    START=time.time()
    death_probs = calc_chance_die(a, b)
    END=time.time()
    time_calc_death_probs=END-START

    START=time.time()
    persons = []
    for soul in dict_num:
        persons += [people.Person(False, False, soul_probs, soul, math.floor(npr.normal(25, 15))) for n in range(dict_num[soul])]
    END=time.time()
    time_gen_initial_persons=END-START

    #a=people.Person(False, False, 'arcane', 30)
    #b=people.Person(False, False, 'arcane', 30)
    #kid=people.Person(a, b)
    #exit(2)

    time_aging_dying=0.0
    time_writing_deaths=0.0
    time_finding_partners=0.0
    time_having_children=0.0
    time_writing_populations=0.0
    time_garbage_collecting=0.0
    for year in range(years):
        print('starting year ' + str(year) + ' out of ' + str(years))

        START=time.time()
        for person in persons:
            person.age_up()
            person.chance_to_die(year, death_probs)
        END=time.time()
        time_aging_dying+=(END-START)

        START=time.time()
        deaths = [person for person in persons if not person.alive]
        with open('individuals.dat', 'a') as f:
            for person in deaths:
                f.write(person.soul + ' yearofdeath=' + str(person.year_of_death) + ' sex=' + person.sex + ' age=' + str(person.age) + ' partner=' + str(True if person.partner else     False) + ' children=' + str(person.num_children) + '\n')
        END=time.time()
        time_writing_deaths+=(END-START)

        persons = [person for person in persons if person.alive]

        START=time.time()
        for person in persons:
            person.find_partner(persons)
        END=time.time()
        time_finding_partners+=(END-START)

        START=time.time()
        for person in persons:
            child = person.have_child(soul_probs)
            if child:
                persons.append(child)
        END=time.time()
        time_having_children+=(END-START)

        START=time.time()
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
        END=time.time()
        time_writing_populations+=(END-START)

        '''
        START=time.time()
        gc.collect()
        end=time.time()
        time_garbage_collecting+=(END-START)
        '''

    START=time.time()
    with open('endsummary.dat', 'a') as f:
        total      = len(persons)
        total_null = len([True for person in persons if person.soul == 'null'])
        f.write('total = ' + str(total) + '\n')
        if total > 0:
            for soul in people.dict_souls:
                num = len([True for person in persons if person.soul == soul])
                if num > 0:
                    if soul == 'null':
                        f.write(soul + ' = ' + str(num) + ', ' + str(round(100.0 * float(num)/float(total), 2)) + '% of total\n')
                    else:
                        f.write(soul + ' = ' + str(num) + ', ' + str(round(100.0 * float(num)/float(total-total_null), 2)) + '% of magical\n')
    END=time.time()
    time_writing_end_summary=(END-START)

    START=time.time()
    with open('individuals.dat', 'a') as f:
        for person in persons:
            f.write(person.soul + ' alive=' + str(person.alive) + (str(person.year_of_death) if not person.alive else '') + ' sex=' + person.sex + ' age=' + str(person.age) + ' partner=' + str(True if person.partner else False) + ' children=' + str(person.num_children) + '/' + str(person.children_wanted) + '\n')
    END=time.time()
    time_writing_individuals=END-START

    END_TOTAL=time.time()

    with open('times.dat', 'a') as f:
        f.write('time calculating soul probabilities  = ' + str(time_calc_soul_probs) + '\n')
        f.write('time calculating death probabilities = ' + str(time_calc_death_probs) + '\n')
        f.write('time generating initial persons      = ' + str(time_gen_initial_persons) + '\n')
        f.write('\n')
        f.write('time aging and dying                 = ' + str(time_aging_dying) + '\n')
        f.write('time writing deaths                  = ' + str(time_writing_deaths) + '\n')
        f.write('time finding partners                = ' + str(time_finding_partners) + '\n')
        f.write('time having children                 = ' + str(time_having_children) + '\n')
        f.write('\n')
        f.write('time writing end summary             = ' + str(time_writing_end_summary) + '\n')
        f.write('time writing populations             = ' + str(time_writing_populations) + '\n')
        f.write('time writing individuals             = ' + str(time_writing_individuals) + '\n')
        f.write('\n')
        f.write('time garbage collecting              = ' + str(time_garbage_collecting) + '\n')
        f.write('\n')
        f.write('total                                = ' + str(END_TOTAL-START_TOTAL) + '\n')



