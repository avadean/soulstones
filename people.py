import math
import numpy.random as npr
import numba

dict_souls = { 'null'      : [ [ 'null' ] , [ 'fire', 'water', 'wind', 'earth' ] , [ 'light', 'dark' ] , [ 'stone', 'metal', 'flying', 'ice', 'lightning', 'poison', 'ghost', 'psychic', 'nuclear', 'gravity', 'life', 'death', 'soul', 'luna', 'jade', 'dragon', 'dream', 'blood', 'arcane' ] , [] ] ,
               'water'     : [ [ 'water'            ] , [ 'light', 'null'    ] , [ 'wind'            ] , [ 'earth'                ] , [ 'fire'                 ] ] ,
               'fire'      : [ [ 'fire'             ] , [ 'dark', 'null'     ] , [ 'earth'           ] , [ 'wind'                 ] , [ 'water'                ] ] ,
               'earth'     : [ [ 'earth'            ] , [                    ] , [ 'null'            ] , [ 'wind'                 ] , [                        ] ] ,
               'wind'      : [ [ 'wind'             ] , [                    ] , [ 'null'            ] , [ 'earth'                ] , [                        ] ] ,
               'light'     : [ [ 'light'            ] , [ 'dark'             ] , [                   ] , [                        ] , [                        ] ] ,
               'dark'      : [ [ 'dark'             ] , [                    ] , [ 'light'           ] , [                        ] , [                        ] ] ,
               'stone'     : [ [                    ] , [ 'stone'            ] , [ 'metal'           ] , [ 'earth'                ] , [                        ] ] ,
               'metal'     : [ [                    ] , [ 'metal'            ] , [ 'stone'           ] , [ 'earth'                ] , [                        ] ] ,
               'flying'    : [ [                    ] , [ 'flying'           ] , [ 'wind'            ] , [                        ] , [                        ] ] ,
               'ice'       : [ [                    ] , [ 'ice'              ] , [ 'lightning'       ] , [                        ] , [                        ] ] ,
               'lightning' : [ [                    ] , [ 'lightning'        ] , [ 'ice'             ] , [                        ] , [                        ] ] ,
               'poison'    : [ [                    ] , [ 'poison'           ] , [ 'flying'          ] , [ 'earth', 'wind'        ] , [ 'psychic'              ] ] ,
               'ghost'     : [ [                    ] , [ 'ghost'            ] , [ 'flying'          ] , [ 'fire', 'water'        ] , [ 'poison'               ] ] ,
               'psychic'   : [ [                    ] , [ 'psychic'          ] , [ 'flying'          ] , [ 'light', 'dark'        ] , [ 'ghost'                ] ] ,
               'nuclear'   : [ [                    ] , [ 'nuclear', 'metal' ] , [                   ] , [                        ] , [                        ] ] ,
               'gravity'   : [ [                    ] , [ 'gravity', 'stone' ] , [                   ] , [                        ] , [                        ] ] ,
               'life'      : [ [                    ] , [ 'life'             ] , [ 'light', 'dark'   ] , [ 'earth', 'wind'        ] , [ 'fire', 'water'        ] ] ,
               'death'     : [ [                    ] , [ 'death'            ] , [ 'dark'            ] , [                        ] , [                        ] ] ,
               'soul'      : [ [                    ] , [ 'soul'             ] , [ 'life'            ] , [                        ] , [                        ] ] ,
               'luna'      : [ [                    ] , [ 'luna'             ] , [ 'psychic'         ] , [                        ] , [                        ] ] ,
               'jade'      : [ [                    ] , [ 'jade'             ] , [ 'ice'             ] , [                        ] , [                        ] ] ,
               'dragon'    : [ [                    ] , [                    ] , [ 'dragon'          ] , [ 'lightning'            ] , [                        ] ] ,
               'dream'     : [ [                    ] , [                    ] , [ 'dream'           ] , [ 'soul', 'luna', 'jade' ] , [                        ] ] ,
               'blood'     : [ [ 'blood'            ] , [                    ] , [                   ] , [ 'poison'               ] , [                        ] ] ,
               'arcane'    : [ [ 'arcane'           ] , [                    ] , [                   ] , [                        ] , [ 'soul', 'luna', 'jade' ] ] ,
              }

l = 1.5 # Global float that determines the probability fall-off of accepted souls.

class Person:
    def __init__(self, father, mother, soul=False):
        self.age             = 0
        self.sex             = 'M' if npr.random() < 0.5 else 'F'
        self.alive           = True
        self.year_of_death   = False
        self.father          = father
        self.mother          = mother
        self.siblings        = self.father.children + self.mother.children if self.father and self.mother else []
        self.partner         = False
        self.children        = []
        self.num_children    = 0
        self.children_wanted = npr.choice([0, 1, 2, 3])
        self.soul            = soul if soul else self.get_soul()

    def get_soul(self):
        souls = [soul for soul in dict_souls]
        probs = []

        total = 0.0 # To normalise.
        for soul in dict_souls: # Looping through all the possible souls that this new person could be.
            soul_prob = 0.0 # Probability of being this soul.

            for power, accepted_souls in enumerate(dict_souls[soul], 1): # Accepted souls are those that this soul accepts as increasing its chances of occuring.
                for accepted_soul in accepted_souls: # There's a list of accepted souls for each power.
                    num_parents = (1 if self.father.soul == accepted_soul else 0) + (1 if self.mother.soul == accepted_soul else 0) # Number of parents that are accepted soul.
                    if num_parents > 0: # Only increases the chances of this soul occuring if there are parents with this accepted soul.
                        soul_prob += math.exp(-1 * (l ** power) / num_parents)

            probs.append(soul_prob)
            total += soul_prob

        #for num, soul in enumerate(souls):
        #    print(soul, probs[num])

        return npr.choice(souls, p=[prob / total for prob in probs])

    def age_up(self):
        if self.alive:
            self.age += 1

    def chance_to_die(self, current_year):
        if self.alive:
            a = 0.00075
            b = 0.06000

            if npr.random() < a * math.exp(b * float(self.age)):
                self.alive               = False
                self.year_of_death       = current_year
                if self.partner:
                    self.partner.partner = False

    def find_partner(self, other_people):
        if self.alive and 65 >= self.age >= 18 and not self.partner:
            potential_partners = [person for person in other_people                               \
                                  if person.alive and                                             \
                                     person not in [self.father, self.mother] + self.siblings and \
                                     65 >= person.age >= 18 and                                   \
                                     person.sex == ('M' if self.sex == 'F' else 'F')]

            if len(potential_partners) > 0:
                self.partner         = npr.choice(potential_partners)
                self.partner.partner = self

    def have_child(self):
        if self.alive and self.partner and self.age >= 25 and self.partner.age >= 25 and self.num_children < self.children_wanted and self.partner.num_children < self.children_wanted:
            if self.sex == 'M':
                child = Person(self, self.partner)
            else:
                child = Person(self.partner, self)

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

        return False





