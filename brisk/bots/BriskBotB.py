from .. import *
from ..probabilities import *

from pprint import pprint

class BriskBotB():

    def __init__(self, brisk_map, player):
        self.brisk_map = brisk_map
        self.player = player
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

        enemy_id = 1 if player.id == 2 else 2
        enemy = Player.get(enemy_id)

        print 'player', player.id

        if player.num_reserves > 0 and len(player.territories) > 0:
            for enemy_territory in enemy_territories:
                for territory in enemy_territory.adjacent_territories:
                    if territory.player.id == player.id:
                        self.territories_with_new_armies.append(territory)
                        # print 'player', player, 'placing', player.num_reserves, 'in', territory
                        return 'place_armies', {
                            'territory_id': territory.id,
                            'num_armies': player.num_reserves
                        }
                    
            # print 'player', player, 'placing', player.num_reserves, 'in', player.territories[0]
            return 'place_armies', {
                'territory_id': player.territories[0].id,
                'num_armies': player.num_reserves
            }

        if len(australian_territories) > 0:
            if len(enemy_territories) <= 0:
                # print 'no enemy territories'
                self.territories_with_new_armies = []
                return 'end_turn', ()

            if len(self.territories_with_new_armies) <= 0:
                # print 'no territories with new armies'
                self.territories_with_new_armies = []
                return 'end_turn', ()

            attacker_territory = self.territories_with_new_armies[0]
            for territory in attacker_territory.adjacent_territories:
                # print territory.name
                if territory.continent.id == continent_to_attack.id and territory.player.id == enemy_id:
                    defender_territory = territory
                    num_armies = min(attacker_territory.num_armies - 1, 3)
                    if num_armies <= 0:
                        self.territories_with_new_armies = []
                        return 'end_turn', ()
                    # print 'attacking from', attacker_territory.name, 'to', defender_territory.name, 'with', num_armies
                    return 'attack', {
                        'attacker_territory_id': attacker_territory.id,
                        'defender_territory_id': defender_territory.id,
                        'num_attacker_armies': num_armies
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
