from numpy.random import default_rng
from cProfile import Profile
from pstats import Stats, SortKey

from inout import writeIndividuals, writeInit, writeSummary
from person import createPersons, chancesOfDeath, tryChildren, tryPartners
from soul import soulTable


def main(r, initialPop: int = 100, years: int = 100, **kwargs):
    assert type(initialPop) is int
    assert initialPop > 0, 'Need non-zero initial population.'

    assert type(years) is int
    assert years > 0, 'Need to run for a non-zero number of years.'

    persons = createPersons(r, num=initialPop, minAge=0, maxAge=100, leaveNulls=True, **kwargs)

    writeInit(persons)

    with open('deaths.dat', 'w') as fileDeaths:
        for year in range(years):
            if not len(persons):
                break

            deaths = chancesOfDeath(r, ages=[person.age for person in persons])

            for person, death in zip(persons, deaths):
                # Set it so no one has had a child this year yet.
                person.childThisYear = False

                # Age up the population.
                person.ageUp()

                # See if anyone dies.
                if death:
                    person.die()

                    if person.partner is not None:
                        person.partner.losePartner()

                    fileDeaths.write(str(person) + '\n')

            # Remove dead people.
            persons = [person for person in persons if person.alive]

            # Set up partners.
            tryPartners(persons)

            # Try for children.
            newChildren = tryChildren(r, persons)

            persons += newChildren

            print(f'ending year {year} with pop {len(persons)}')  # ... {persons}')

    writeIndividuals(persons)
    writeSummary(persons, soulTable)


if __name__ == '__main__':
    rng = default_rng(seed=None)

    initPop = 2_000_000

    init = {'water': 50000,
            'fire': 50000,
            'earth': 25000,
            'wind': 25000,
            'light': 10000,
            'dark': 5000,
            'stone': 2500,
            'metal': 2500,
            'flying': 2500,
            'ice': 2500,
            'lightning': 1000,
            'poison': 1000,
            'ghost': 1000,
            'psychic': 1000,
            'nuclear': 1000,
            'gravity': 1000,
            'life': 100,
            'death': 100}

    with Profile() as pr:
        main(r=rng, initialPop=initPop, years=200, **init)

    stats = Stats(pr)
    stats.sort_stats(SortKey.TIME)
    stats.print_stats()
    stats.dump_stats('timeProfiling.dat')
