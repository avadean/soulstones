from numpy.random import default_rng
from cProfile import Profile
from pstats import Stats, SortKey

from inout import writeIndividuals, writeSummary
from person import createPersons, chancesOfDeath, tryChildren, tryPartners
from soul import soulTable


def main(r, initialPop: int = 100, years: int = 100, **kwargs):
    assert type(initialPop) is int
    assert initialPop > 0, 'Need non-zero initial population.'

    assert type(years) is int
    assert years > 0, 'Need to run for a non-zero number of years.'

    persons = createPersons(r, num=initialPop, minAge=0, maxAge=100, **kwargs)

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

    initPop = 10_000

    init = {'water': 400,
            'fire': 400,
            'earth': 200,
            'wind': 200,
            'light': 100,
            'dark': 50,
            'stone': 25,
            'metal': 25,
            'flying': 25,
            'ice': 25,
            'lightning': 10,
            'poison': 10,
            'ghost': 10,
            'psychic': 10,
            'nuclear': 10,
            'gravity': 10,
            'life': 5,
            'death': 1}

    with Profile() as pr:
        main(r=rng, initialPop=initPop, years=200, **init)

    stats = Stats(pr)
    stats.sort_stats(SortKey.TIME)
    stats.print_stats()
    stats.dump_stats('timeProfiling.dat')
