from matplotlib.pyplot import plot, show
from numpy.random import default_rng
from cProfile import Profile
from pstats import Stats, SortKey

from person import createPersons, chancesOfDeath, tryChildren, tryPartners


def main(r, initialPop: int = 100, years: int = 100):
    assert type(initialPop) is int
    assert initialPop > 0, 'Need non-zero initial population.'

    assert type(years) is int
    assert years > 0, 'Need to run for a non-zero number of years.'

    persons = createPersons(r, num=initialPop, minAge=0, maxAge=100)

    for year in range(years):
        if not len(persons):
            break

        deaths = chancesOfDeath(r, ages=[person.age for person in persons])

        for num, person in enumerate(persons):
            # Set it so no one has had a child this year yet.
            person.childThisYear = False

            # Age up the population.
            person.ageUp()

            # See if anyone dies.
            if deaths[num]:
                person.die()

                if person.partner is not None:
                    person.partner.losePartner()

        # Remove dead people.
        persons = [person for person in persons if person.alive]

        # Set up partners.
        tryPartners(r, persons)

        # Try for children.
        newChildren = tryChildren(r, persons)

        persons += newChildren

        print(f'ending year {year} with pop {len(persons)}')  # ... {persons}')

    with open('individuals.dat', 'w') as f:
        f.write('\n'.join([f'{person.soul}  {person.age:>3}{person.sex}  partner={bool(person.partner):<5}  children={len(person.children)}/{person.numChildrenWanted}' for person in persons]))

    print('')

    if persons:
        print('average age', round(sum([person.age for person in persons]) / len(persons), 2))

    print('population', len(persons))

    ages = [person.age for person in persons]

    x = range(110)
    y = [ages.count(age) for age in x]

    #plot(x, y)
    #show()


if __name__ == '__main__':
    rng = default_rng(seed=None)

    with Profile() as pr:
        main(r=rng, initialPop=10000, years=200)

    stats = Stats(pr)
    stats.sort_stats(SortKey.TIME)
    stats.print_stats()
    stats.dump_stats('timeProfiling.dat')






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
    soul_probs  = calc_soul_probs(gamma)

    death_probs = calc_chance_die(a, b)

    persons = []
    for soul in dict_num:
        persons += [people.Person(False, False, soul_probs, soul, math.floor(npr.normal(25, 15))) for _ in range(dict_num[soul])]

    for year in range(years):
        print('starting year ' + str(year) + ' out of ' + str(years))

        for person in persons:
            person.age_up()
            person.chance_to_die(year, death_probs)

        deaths = [person for person in persons if not person.alive]
        with open('individuals.dat', 'a') as f:
            for person in deaths:
                f.write(person.soul + ' yearofdeath=' + str(person.year_of_death) + ' sex=' + person.sex + ' age=' + str(person.age) + ' partner=' + str(True if person.partner else False) + ' children=' + str(person.num_children) + '\n')

        persons = [person for person in persons if person.alive]

        for person in persons:
            person.find_partner(persons)

        for person in persons:
            child = person.have_child(soul_probs)
            if child:
                persons.append(child)

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

    with open('individuals.dat', 'a') as f:
        for person in persons:
            f.write(person.soul + ' alive=' + str(person.alive) + (str(person.year_of_death) if not person.alive else '') + ' sex=' + person.sex + ' age=' + str(person.age) + ' partner=' + str(True if person.partner else False) + ' children=' + str(person.num_children) + '/' + str(person.children_wanted) + '\n')
