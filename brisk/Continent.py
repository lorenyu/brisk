from Player import Player

class Continent():

    def __init__(self, id, bonus, name, territories):
        self.id = id
        self.bonus = bonus
        self.name = name
        self.territories = territories
        self.boundary_territories = []
        self.player = None


    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id
        
    def __repr__(self):
        return '<Continent:' + str(self.id) + ':' + self.name + '>'

    def __hash__(self):
        return hash(repr(self))
