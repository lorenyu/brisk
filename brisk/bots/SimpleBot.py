from .. import *

from pprint import pprint

class SimpleBot():

    def __init__(self, brisk_map, player):
        self.brisk_map = brisk_map
        self.player = player
        pass

    def compute_num_armies_to_transfer(self, attacker_territory, defender_territory):
        return 0

    def compute_next_action(self):

        player = self.player

        if player.num_reserves > 0 and len(player.territories) > 0:
            return 'place_armies', {
                'territory': player.territories[0],
                'num_armies': player.num_reserves
            }
        
        # find the continent that is easiest to take over
        # look at the enemy controlled territories in that continent,
        # and the adjacent territories that we control
        # and take the total number of units we can use to attack
        # minus the total number of enemy units
        # minus the number of enemy territories

        # game_state = BriskGameState.create_from_game_state_data(game_state_data)
        
        return 'end_turn', ()

class ContinentStats():

    def compute_easiest_continent(self, brisk_map, game_state):

        for continent in brisk_map.continents:

            compute_continent_difficulty(continent)

    def compute_continent_difficulty(self, continent, game_state):

        # for territory in continent.territories:

        #     if game_state['territories'][territory.id]

        pass
