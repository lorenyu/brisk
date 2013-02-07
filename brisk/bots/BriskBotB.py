from .. import *
from ..probabilities import *
from sys import stdout

from pprint import pprint

class BriskBotB():

    def __init__(self, brisk_map, player):
        self.brisk_map = brisk_map
        self.player = player
        self.probability_calculator = RiskProbabilityCalculator()
        pass

    def num_territories_needed_for_extra_base_armies(self, player_id):
        num_territories = sum([1 for territory in self.brisk_map.get_territories() if territory.player.id == player_id])
        # print 'num_territories', num_territories
        return 3 - (num_territories % 3)

    def territories_needed_for_continent(self, player, continent):
        return [territory for territory in continent.territories if territory.player.id != player.id]

    def territories_needed_for_each_continent(self, player):
        return [(continent, self.territories_needed_for_continent(player, continent)) for continent in self.brisk_map.get_continents()]

    def compute_next_action(self):

        player = self.player
        brisk_map = self.brisk_map

        enemy_id = 1 if player.id == 2 else 2
        enemy = Player.get(enemy_id)

        print 'player', player.id

        if player.num_reserves > 0 and len(player.territories) > 0:
            best_path = None
            best_path_value = 0.0
            for path in self.brisk_map.get_paths_accessible_by_player(player):
                num_armies_in_attacking_territory = path[0].num_armies + player.num_reserves
                num_armies_in_defending_territories = [territory.num_armies for territory in path[1:]]
                probability_of_conquering_territory_path = self.probability_calculator.probability_of_conquering_territory_path((num_armies_in_attacking_territory, num_armies_in_defending_territories))
                value_of_conquering_territory_path = brisk_map.value_if_player_conquered_path(player, path)
                path_value = value_of_conquering_territory_path * probability_of_conquering_territory_path + player.num_armies_next_round * (1.0 - probability_of_conquering_territory_path)
                if path_value > best_path_value:
                    best_path = path
                    best_path_value = path_value

            if best_path:
                territory = best_path[0]
            else:
                territory = player.territories[0]
            pprint(best_path)
            return 'place_armies', {
                'territory': territory,
                'num_armies': player.num_reserves
            }

        best_path = None
        best_path_value = 0.0
        for path in self.brisk_map.get_paths_accessible_by_player(player):
            if len(path) <= 1:
                continue
            num_armies_in_attacking_territory = path[0].num_armies + player.num_reserves
            num_armies_in_defending_territories = [territory.num_armies for territory in path[1:]]
            probability_of_conquering_territory_path = self.probability_calculator.probability_of_conquering_territory_path((num_armies_in_attacking_territory, num_armies_in_defending_territories))
            value_of_conquering_territory_path = brisk_map.value_if_player_conquered_path(player, path)
            path_value = value_of_conquering_territory_path * probability_of_conquering_territory_path + player.num_armies_next_round * (1.0 - probability_of_conquering_territory_path)
            if path_value > best_path_value:
                best_path = path
                best_path_value = path_value

        if best_path:
            pprint(best_path)
            attacker_territory = best_path[0]
            defender_territory = best_path[1]
            return 'attack', {
                'attacker_territory': attacker_territory,
                'defender_territory': defender_territory,
                'num_attacker_armies': attacker_territory.num_armies - 1
            }
        
        self.territories_with_new_armies = []
        return 'end_turn', ()

class ContinentStats():

    def compute_easiest_continent(self, brisk_map, game_state):

        for continent in brisk_map.continents:

            compute_continent_difficulty(continent)

    def compute_continent_difficulty(self, continent, game_state):

        # for territory in continent.territories:

        #     if game_state['territories'][territory.id]

        pass
