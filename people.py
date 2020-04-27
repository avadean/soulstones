import time
import math
import numpy.random as npr

dict_souls = { 'null'      : [ [ 'null', 'null' ] , [ 'fire', 'water' , 'wind', 'earth' , 'light', 'dark' ] , [ 'stone', 'metal', 'flying', 'ice', 'lightning', 'poison', 'ghost', 'psychic', 'nuclear', 'gravity', 'life', 'death' ] , [ 'soul', 'luna', 'jade', 'dragon', 'dream', 'blood', 'arcane' ] , [] , [] ] ,
               'water'     : [ [          ] , [ ] , [ 'water'            ] , [ 'light', 'null'     ] , [ 'wind'               ] , [ 'earth'                ] , [ 'fire'                 ] ] ,
               'fire'      : [ [          ] , [ ] , [ 'fire'             ] , [ 'dark', 'null'      ] , [ 'earth'              ] , [ 'wind'                 ] , [ 'water'                ] ] ,
               'earth'     : [ [          ] , [ ] , [ 'earth'            ] , [                     ] , [ 'null'               ] , [ 'wind'                 ] , [                        ] ] ,
               'wind'      : [ [          ] , [ ] , [ 'wind'             ] , [                     ] , [ 'null'               ] , [ 'earth'                ] , [                        ] ] ,
               'light'     : [ [          ] , [ ] , [ 'light'            ] , [ 'dark', 'water'     ] , [                      ] , [                        ] , [                        ] ] ,
               'dark'      : [ [          ] , [ ] , [ 'dark'             ] , [                     ] , [ 'light', 'fire'      ] , [                        ] , [                        ] ] ,
               'stone'     : [ [          ] , [ ] , [                    ] , [ 'stone'             ] , [ 'metal', 'earth'     ] , [ 'wind'                 ] , [                        ] ] ,
               'metal'     : [ [          ] , [ ] , [                    ] , [ 'metal'             ] , [ 'stone', 'earth'     ] , [ 'wind'                 ] , [                        ] ] ,
               'flying'    : [ [          ] , [ ] , [                    ] , [ 'flying'            ] , [ 'wind'               ] , [                        ] , [                        ] ] ,
               'ice'       : [ [          ] , [ ] , [                    ] , [ 'ice'               ] , [ 'lightning'          ] , [ 'water'                ] , [                        ] ] ,
               'lightning' : [ [          ] , [ ] , [                    ] , [ 'lightning'         ] , [ 'ice'                ] , [ 'fire'                 ] , [                        ] ] ,
               'poison'    : [ [          ] , [ ] , [                    ] , [ 'poison'            ] , [ 'psychic'            ] , [ 'dark'                 ] , [ 'water'                ] ] ,
               'ghost'     : [ [          ] , [ ] , [                    ] , [ 'ghost'             ] , [ 'poison'             ] , [ 'wind'                 ] , [ 'fire'                 ] ] ,
               'psychic'   : [ [          ] , [ ] , [                    ] , [ 'psychic'           ] , [ 'ghost'              ] , [ 'light'                ] , [ 'earth'                ] ] ,
               'nuclear'   : [ [          ] , [ ] , [                    ] , [ 'nuclear', 'metal'  ] , [                      ] , [                        ] , [                        ] ] ,
               'gravity'   : [ [          ] , [ ] , [                    ] , [ 'gravity', 'flying' ] , [                      ] , [                        ] , [                        ] ] ,
               'life'      : [ [          ] , [ ] , [                    ] , [ 'life'              ] , [ 'light'              ] , [ 'earth', 'wind'        ] , [ 'fire', 'water'        ] ] ,
               'death'     : [ [ 'death'  ] , [ ] , [                    ] , [ 'dark'              ] , [                      ] , [                        ] , [                        ] ] ,
               'soul'      : [ [          ] , [ ] , [                    ] , [                     ] , [ 'soul'               ] , [ 'life'                 ] , [                        ] ] ,
               'luna'      : [ [          ] , [ ] , [                    ] , [                     ] , [ 'luna'               ] , [ 'psychic'              ] , [                        ] ] ,
               'jade'      : [ [          ] , [ ] , [                    ] , [                     ] , [ 'jade'               ] , [ 'ice'                  ] , [                        ] ] ,
               'dragon'    : [ [          ] , [ ] , [                    ] , [                     ] , [ 'dragon'             ] , [ 'death'                ] , [                        ] ] ,
               'dream'     : [ [          ] , [ ] , [                    ] , [                     ] , [ 'dream'              ] , [ 'ghost'                ] , [                        ] ] ,
               'blood'     : [ [ 'blood'  ] , [ ] , [                    ] , [                     ] , [                      ] , [ 'poison'               ] , [                        ] ] ,
               'arcane'    : [ [ 'arcane' ] , [ ] , [                    ] , [                     ] , [                      ] , [ 'lightning'            ] , [                        ] ] ,
              }

class Person:
    def __init__(self, father, mother, probs, soul=False, age=0):
        self.age             = age if age > 0 else 0
        self.sex             = 'M' if npr.random() < 0.5 else 'F'
        self.alive           = True
        self.year_of_death   = False
        self.father          = father
        self.mother          = mother
        self.siblings        = self.father.children + self.mother.children if self.father and self.mother else []
        self.partner         = False
        self.children        = []
        self.num_children    = 0
        self.children_wanted = npr.randint(5) #npr.choice([0, 1, 2, 3])
        self.soul            = soul if soul else self.get_soul(probs)

        self.min_age_partner = 18
        self.max_age_partner = 65
        self.min_age_child   = 25
        self.max_age_child   = 55

    def get_soul(self, probs):
        return npr.choice([soul for soul in dict_souls], p=probs[self.father.soul][self.mother.soul])

    def age_up(self):
        if self.alive:
            self.age += 1

    def chance_to_die(self, current_year, probs):
        if self.alive and npr.random() < probs[self.age]:
            self.alive               = False
            self.year_of_death       = current_year
            if self.partner:
                self.partner.partner = False

    def find_partner(self, persons):
        '''
        if self.alive and 65 >= self.age >= 18 and not self.partner:
            potential_partners = [person for person in persons                                    \
                                  if person != self and                                           \
                                     person.alive and                                             \
                                     person not in [self.father, self.mother] + self.siblings and \
                                     65 >= person.age >= 18 and                                   \
                                     person.sex == ('M' if self.sex == 'F' else 'F')]

            if len(potential_partners) > 0:
                self.partner         = npr.choice(potential_partners)
                self.partner.partner = self
        '''

        if self.max_age_partner >= self.age >= self.min_age_partner and not self.partner:
            for i in range(10): # Try up to 10 times to find a partner.
                potential_partner = persons[npr.randint(len(persons))] #npr.choice(persons)

                if potential_partner != self and\
                        potential_partner not in [self.father, self.mother] + self.siblings and\
                        potential_partner.max_age_partner >= potential_partner.age >= potential_partner.min_age_partner and\
                        potential_partner.sex == ('M' if self.sex == 'F' else 'F'):

                    self.partner         = potential_partner
                    self.partner.partner = self
                    break

    def have_child(self, probs):
        if self.alive and self.partner and self.max_age_child >= self.age >= self.min_age_child and self.partner.max_age_child >= self.partner.age >= self.partner.min_age_child and self.num_children < self.children_wanted and self.partner.num_children < self.children_wanted:
            if self.sex == 'M':
                child = Person(self, self.partner, probs)
            else:
                child = Person(self.partner, self, probs)

            # Add child to children
            self.children.append(child)
            self.num_children += 1

            # Add child to partner's children.
            self.partner.children.append(child)
            self.partner.num_children += 1

            # Add child to children's siblings.
            for other_child in self.children:
                other_child.siblings.append(child)

            return child
        else:
            return False


