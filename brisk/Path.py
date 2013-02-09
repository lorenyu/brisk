from probabilities import *

class Path:
    def __init__(self, territories):
        self.territories = territories
        self.probability_of_conquering_path = 0.0
        self.probability_of_conquering_path_by_num_armies_left = {}

    def __getitem__(self, i):
        return self.territories[i]

    def __len__(self):
        return len(self.territories)

    def __repr__(self):
        return repr(self.territories)

    @staticmethod
    def create_with_single_territory(territory):
        result = Path((territory,))
        result.probability_of_conquering_path = 1.0
        result.probability_of_conquering_path_by_num_armies_left[territory.num_armies] = 1.0
        return result

    @staticmethod
    def create_by_appending_path_with_territory(path, territory):
        result = Path(path.territories + (territory,))
        # a_0 = num_armies_left in last territory of path
        # p_0 = probability of conquering path with a_0 armies left in last territory of path
        # a_1 = num_armies_left after conquering appended territory
        # p_1 = probability of conquering appended territory with a_1 armies left, yielding a_1 - 1 armies left in appended territory if all armies are transferred to appended_territory
        # p_01 = probability of conquering appended territory with a_0 units and having a_1 units left
        for a_0, p_0 in path.probability_of_conquering_path_by_num_armies_left.iteritems():
            for a_1 in range(2, a_0 + 1):
                p_01 = probability_calculator.probability_when_attacking_territory((a_1, 0), (a_0, territory.num_armies, strategies.all_in))
                p_1 = p_0 * p_01
                result.probability_of_conquering_path_by_num_armies_left[a_1 - 1] = p_1
            result.probability_of_conquering_path = sum(result.probability_of_conquering_path_by_num_armies_left.values())
        return result

