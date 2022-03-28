from soul import soulTable


def writeIndividuals(persons: list = None):
    with open('individuals.dat', 'w') as fileIndividuals:
        for person in persons:
            fileIndividuals.write(str(person) + '\n')


def writeSummary(persons: list = None):
    with open('summary.dat', 'w') as fileSummary:
        souls = [person.soul for person in persons]
        cTotal = len(souls)
        cNull = souls.count('null')

        fileSummary.write('/==================================================\\\n')
        fileSummary.write(f'|{"total":>12} : {cTotal:>7}                            |\n')
        fileSummary.write('|                                                  |\n')
        fileSummary.write(f'|{"null":>12} : {cNull:>7}    {100.0 * cNull / cTotal:8.3f} % of total     |\n')
        fileSummary.write('|==================================================|\n')

        souls = [s for s in souls if s != 'null']
        cMagical = len(souls)

        fileSummary.write(f'|{"magical":>12} : {cMagical:>7}    {100.0 * cMagical / cTotal:8.3f} % of total     |\n')
        fileSummary.write('|                                                  |\n')

        soulTbl = soulTable.copy()
        soulTbl.remove('null')

        for soul in soulTbl:
            cSoul = souls.count(soul)

            fileSummary.write(f'|{soul:>12} : {cSoul:>7}    {100.0 * cSoul / cMagical:8.3f} % of magical   |\n')

        fileSummary.write('\\==================================================/')
