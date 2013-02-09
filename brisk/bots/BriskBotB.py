from .. import *
from ..probabilities import *
from sys import stdout

from pprint import pprint

class BriskBotB():

    def __init__(self, brisk_map, player):
        self.brisk_map = brisk_map
        self.player = player

        enemy_id = 1 if player.id == 2 else 2
        self.enemy = Player.get(enemy_id)

        probability_calculator = RiskProbabilityCalculator()
        self.last_move = None
        pass

    def num_territories_needed_for_extra_base_armies(self, player_id):
        num_territories = sum([1 for territory in self.brisk_map.get_territories() if territory.player.id == player_id])
        # print 'num_territories', num_territories
        return 3 - (num_territories % 3)

    def territories_needed_for_continent(self, player, continent):
        return [territory for territory in continent.territories if territory.player.id != player.id]

    def territories_needed_for_each_continent(self, player):
        return [(continent, self.territories_needed_for_continent(player, continent)) for continent in self.brisk_map.get_continents()]

    def value_of_path(self, path):
        brisk_map = self.brisk_map
        player = self.player
        enemy = self.enemy

        temp_map_state = TempMapState(brisk_map)
        for territory in path[1:]:
            temp_map_state.set_player_controlling_territory(territory, player)
            temp_map_state.set_num_armies_for_territory(territory, 1)
        temp_map_state.set_num_armies_for_territory(path[-1], path.expected_num_armies_left())

        temp_map_state.compute_map_values()

        a_p = temp_map_state.num_armies_for_player(player)
        f_p = temp_map_state.num_fronts_for_player(player)
        af_p = temp_map_state.num_armies_at_front_for_player(player)
        ar_p = temp_map_state.num_armies_next_round_for_player(player)
        a_e = temp_map_state.num_armies_for_player(enemy)
        f_e = temp_map_state.num_fronts_for_player(enemy)
        af_e = temp_map_state.num_armies_at_front_for_player(enemy)
        ar_e = temp_map_state.num_armies_next_round_for_player(enemy)

        return 1.0*a_p + 0.0*f_p + 0.0*af_p + 0.0*ar_p - 0.0*a_e - 0.0*f_e - 0.0*af_e - 0.0*ar_e


    def compute_num_armies_to_transfer(self, attacker_territory, defender_territory):
        return attacker_territory.num_armies - 1

    def compute_next_action(self):

        player = self.player
        enemy = self.enemy
        brisk_map = self.brisk_map

        enemy_id = enemy.id

        max_armies_in_territory = max([territory.num_armies for territory in player.territories])

        if player.num_reserves > 0 and len(player.territories) > 0:
            best_path = None
            best_path_value = 0.0
            for path in self.brisk_map.get_paths_accessible_by_player(player, max_armies_in_territory + player.num_reserves):
                # num_armies_in_attacking_territory = path[0].num_armies + player.num_reserves
                # num_armies_in_defending_territories = [territory.num_armies for territory in path[1:]]
                # probability_of_conquering_territory_path = probability_calculator.probability_of_conquering_territory_path((num_armies_in_attacking_territory, num_armies_in_defending_territories))
                value_of_conquering_territory_path = self.value_of_path(path)
                path_value = value_of_conquering_territory_path * path.probability_of_conquering_path + player.num_armies_next_round * (1.0 - path.probability_of_conquering_path)
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
            # num_armies_in_attacking_territory = path[0].num_armies + player.num_reserves
            # num_armies_in_defending_territories = [territory.num_armies for territory in path[1:]]
            # probability_of_conquering_territory_path = probability_calculator.probability_of_conquering_territory_path((num_armies_in_attacking_territory, num_armies_in_defending_territories))
            value_of_conquering_territory_path = self.value_of_path(path)
            path_value = value_of_conquering_territory_path * path.probability_of_conquering_path + player.num_armies_next_round * (1.0 - path.probability_of_conquering_path)
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
