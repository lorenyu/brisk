class Territory():

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.adjacent_territories = []
        self.player = None
        self.num_armies = 0
        self.continent = None

    def is_adjacent_to(self, territory):
        return territory.id in [territory.id for territory in self.adjacent_territories]

    def is_adjacent_to_territories(self, territories):
        return any([self.is_adjacent_to(territory) for territory in territories])

    def add_adjacent_territory(self, adjacent_territory):
        self.adjacent_territories.append(adjacent_territory)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __repr__(self):
        return '<Territory:' + str(self.id) + ':' + self.name + '>'

    def __hash__(self):
        return hash(repr(self))
      
    @staticmethod  
    def partition_territories(territories):
        partitions = []
        for territory in territories:
            is_new_partition = True
            for partition in partitions:
                if territory.is_adjacent_to_territories(partition):
                    partition.append(territory)
                    is_new_partition = False
                    break
            if is_new_partition:
                partition = [territory]
                partitions.append(partition)
        return partitions