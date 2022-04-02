from collections import Counter


def writeSoulDict(soulDict: dict = None):
    with open('soulDict.dat', 'w') as fileSoulDict:
        for fSoul, mSoulDict in soulDict.items():
            for mSoul, cSoul in mSoulDict.items():
                fSoul = str(fSoul)
                mSoul = str(mSoul)
                cSoul = str(cSoul)
                fileSoulDict.write(f'{fSoul:>12} + {mSoul:^12} = {cSoul:<12}\n')


def writeInit(persons: list = None):
    souls = Counter([person.soul for person in persons])

    with open('init.dat', 'w') as fileInit:
        for soul, numSoul in souls.items():
            fileInit.write(f'{soul:>12} : {numSoul:>9}\n')


def writeIndividuals(persons: list = None):
    with open('individuals.dat', 'w') as fileIndividuals:
        for person in persons:
            fileIndividuals.write(str(person) + '\n')


def writeMythical(person=None):
    with open('mythicals.dat', 'a') as fileMythicals:
        fileMythicals.write(str(person) + '\n')


def writeSummary(persons: list = None, soulTbl: list = None):
    souls = [person.soul for person in persons]
    cTotal = len(souls)

    if cTotal == 0:
        return

    with open('summary.dat', 'w') as fileSummary:
        cNull = souls.count('null')

        fileSummary.write('/==================================================\\\n')
        fileSummary.write(f'|{"total":>12} : {cTotal:>7}                            |\n')
        fileSummary.write('|                                                  |\n')
        fileSummary.write(f'|{"null":>12} : {cNull:>7}    {100.0 * cNull / cTotal:8.3f} % of total     |\n')
        fileSummary.write('|==================================================|\n')

        souls = [s for s in souls if s != 'null']
        cMagical = len(souls)

        if cMagical == 0:
            return

        fileSummary.write(f'|{"magical":>12} : {cMagical:>7}    {100.0 * cMagical / cTotal:8.3f} % of total     |\n')
        fileSummary.write('|                                                  |\n')

        soulTbl.remove('null')

        for soul in soulTbl:
            cSoul = souls.count(soul)

            fileSummary.write(f'|{soul:>12} : {cSoul:>7}    {100.0 * cSoul / cMagical:8.3f} % of magical   |\n')

        fileSummary.write('\\==================================================/')
