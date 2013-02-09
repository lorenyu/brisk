from .. import *
from ..probabilities import *
from sys import stdout

from pprint import pprint

class BonusBot():

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

        temp_map_state.compute_map_values()

        a_p0 = temp_map_state.num_armies_for_player(player)
        f_p0 = temp_map_state.num_fronts_for_player(player)
        af_p0 = temp_map_state.num_armies_at_front_for_player(player)
        ar_p0 = temp_map_state.num_armies_next_round_for_player(player)
        a_e0 = temp_map_state.num_armies_for_player(enemy)
        f_e0 = temp_map_state.num_fronts_for_player(enemy)
        af_e0 = temp_map_state.num_armies_at_front_for_player(enemy)
        ar_e0 = temp_map_state.num_armies_next_round_for_player(enemy)

        for territory in path[1:]:
            temp_map_state.set_player_controlling_territory(territory, player)
            temp_map_state.set_num_armies_for_territory(territory, 1)
        temp_map_state.set_num_armies_for_territory(path[-1], path.expected_num_armies_left())

        temp_map_state.compute_map_values()

        a_p1 = temp_map_state.num_armies_for_player(player)
        f_p1 = temp_map_state.num_fronts_for_player(player)
        af_p1 = temp_map_state.num_armies_at_front_for_player(player)
        ar_p1 = temp_map_state.num_armies_next_round_for_player(player)
        a_e1 = temp_map_state.num_armies_for_player(enemy)
        f_e1 = temp_map_state.num_fronts_for_player(enemy)
        af_e1 = temp_map_state.num_armies_at_front_for_player(enemy)
        ar_e1 = temp_map_state.num_armies_next_round_for_player(enemy)

        # compute deltas
        dar_p = ar_p1 - ar_p0 # change in num armies per round for player
        dar_e = ar_e1 - ar_e0 # change in num armies per round for enemy

        da_p = a_p1 - a_p0 # change in number of armies for player
        da_e = a_e1 - a_e0 # change in number of armies for enemy

        df_p = f_p1 - f_p0 # change in fronts for player
        df_e = f_e1 - f_e0 # change in fronts for enemy

        daf_p = af_p1 - af_p0 # change in number of armies at front for player
        daf_e = af_e1 - af_e0 # change in number of armies at front for enemy

        # print player.id, path, dar_p, df_p, f_p0, f_p1
        # if df_p < 0:
        #     print player.id, path, df_p

        return 0.8*ar_p1 - ar_e1
        # return 0.0*dar_p + 0.0*da_p - 1.0*df_p + 0.0*daf_p - 0.0*dar_e - 0.0*da_e + 0.0*df_e - 0.0*daf_e


    def compute_num_armies_to_transfer(self, attacker_territory, defender_territory):
        temp_map_state = TempMapState(self.brisk_map)
        # Now we have the map post attack. Get the best path for this new map
        best_path = self.get_best_path( attacker_territory.player )
        # Now, figure out if attacker_territory is a frontier in this new best_path
        # For that, create a TempMapState and set the player controlling all territories
        for territory in best_path:
            temp_map_state.set_player_controlling_territory( territory, attacker_territory.player )
        temp_map_state.compute_map_values()
        #assert defender_territory.player.id == attacker_territory.player.id
        #if defender_territory not in temp_map_state.fronts_for_player(defender_territory.player):
        #    if defender_territory not in best_path:
        #        return 0
        if attacker_territory in temp_map_state.fronts_for_player( attacker_territory.player):
            max_enemy_troops_in_adj = 0
            for territory in attacker_territory.adjacent_territories:
                if territory.player.id != attacker_territory.player.id:
                    if territory.num_armies > max_enemy_troops_in_adj:
                        max_enemy_troops_in_adj = territory.num_armies
            numToTransfer = attacker_territory.num_armies - max_enemy_troops_in_adj
            if numToTransfer < 0:
                numToTransfer = 0
            if numToTransfer == attacker_territory.num_armies:
                numToTransfer -= 1
            return numToTransfer
        return attacker_territory.num_armies - 1

    def get_best_path( self, player ):
        best_path = None
        best_path_value = float('-inf')
        for path in self.brisk_map.get_paths_accessible_by_player(player):
            if len(path) <= 1:
                continue
            value_of_conquering_territory_path = self.value_of_path(path)
            path_value = value_of_conquering_territory_path * path.probability_of_conquering_path
            if path_value > best_path_value:
                best_path = path
                best_path_value = path_value
        return best_path

    def compute_next_action(self):

        player = self.player
        enemy = self.enemy
        brisk_map = self.brisk_map

        enemy_id = enemy.id

        max_armies_in_territory = max([territory.num_armies for territory in player.territories])

        if player.num_reserves > 0 and len(player.territories) > 0:
            best_path = self.get_best_path( player )
            if best_path:
                territory = best_path[0]
            else:
                territory = player.territories[0]
            # pprint(best_path)
            return 'place_armies', {
                'territory': territory,
                'num_armies': player.num_reserves
            }

        best_path = self.get_best_path( player )

        if best_path:
            attacker_territory = best_path[0]
            defender_territory = best_path[1]
            if attacker_territory.num_armies - 1 > defender_territory.num_armies:
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
