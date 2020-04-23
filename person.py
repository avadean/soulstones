
class Person:
    def __init__(self, father, mother, soul=False):
        self.age    = 0
        self.father = father
        self.mother = mother
        self.soul   = soul if soul else self.get_soul()

    def get_soul(self):
        pass

    def age_up(self):
        self.age += 1


class InitialPerson(Person):
    def __init__(self, soul):
        super().__init__(False, False, soul)


