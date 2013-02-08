from .. import *
from ..probabilities import *
from sys import stdout

from pprint import pprint

class BriskBotB():

    def __init__(self, brisk_map, player):
        self.brisk_map = brisk_map
        self.player = player
        self.probability_calculator = RiskProbabilityCalculator()
        self.last_move = None
        pass

    def compute_path_value(self, path, brisk_map, player, enemy):
        brisk_map.save()
        print player.num_armies_next_round - enemy.num_armies_next_round
        for territory in path[1:]:
            territory.player = player
        value = player.num_armies_next_round - enemy.num_armies_next_round
        print player.num_armies_next_round - enemy.num_armies_next_round
        brisk_map.load()
        print player.num_armies_next_round - enemy.num_armies_next_round
        print '---------------'
        return value

    def compute_num_armies_to_transfer(self, attacker_territory, defender_territory):
        return attacker_territory.num_armies - 1

    def compute_next_action(self):

        player = self.player
        brisk_map = self.brisk_map

        enemy_id = 1 if player.id == 2 else 2
        enemy = Player.get(enemy_id)

        max_armies_in_territory = max([territory.num_armies for territory in player.territories])

        if player.num_reserves > 0 and len(player.territories) > 0:
            best_path = None
            best_path_value = 0.0
            for path in self.brisk_map.get_paths_accessible_by_player(player, max_armies_in_territory + player.num_reserves):
                num_armies_in_attacking_territory = path[0].num_armies + player.num_reserves
                num_armies_in_defending_territories = [territory.num_armies for territory in path[1:]]
                probability_of_conquering_territory_path = self.probability_calculator.probability_of_conquering_territory_path((num_armies_in_attacking_territory, num_armies_in_defending_territories))
                value_of_conquering_territory_path = self.compute_path_value(path, brisk_map, player, enemy)
                path_value = value_of_conquering_territory_path * probability_of_conquering_territory_path + player.num_armies_next_round * (1.0 - probability_of_conquering_territory_path)
                if path_value > best_path_value:
                    best_path = path
                    best_path_value = path_value

            if best_path:
                territory = best_path[0]
            else:
                territory = player.territories[0]
            # pprint(best_path)
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
            value_of_conquering_territory_path = self.compute_path_value(path, brisk_map, player, enemy)
            path_value = value_of_conquering_territory_path * probability_of_conquering_territory_path + player.num_armies_next_round * (1.0 - probability_of_conquering_territory_path)
            if path_value > best_path_value:
                best_path = path
                best_path_value = path_value

        if best_path:
            attacker_territory = best_path[0]
            defender_territory = best_path[1]
            if attacker_territory.num_armies >= 4:
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
