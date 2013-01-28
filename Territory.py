class Territory():

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.adjacent_territories = []
        self.player = None
        self.num_armies = 0

    def add_adjacent_territory(self, adjacent_territory):
        self.adjacent_territories.append(adjacent_territory)
        