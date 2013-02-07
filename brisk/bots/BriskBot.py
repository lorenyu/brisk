from .. import *

from pprint import pprint

class BriskBot():

    def __init__(self, brisk_map, player):
        self.brisk_map = brisk_map
        self.player = player
        self.territories_with_new_armies = []
        pass

    def num_enemy_armies_next_round(self, player_id):
        enemy_id = 1 if player_id == 2 else 2
        num_enemy_territories = sum([1 for territory in self.brisk_map.get_territories() if territory.player.id == enemy_id])
        base = int(num_enemy_territories / 3)
        enemy_continents = [continent for continent in self.brisk_map.get_continents() if continent.player and continent.player.id == enemy_id]
        bonus = sum([continent.bonus for continent in enemy_continents])
        return base + bonus

    def num_territories_needed_for_extra_base_armies(self, player_id):
        num_territories = sum([1 for territory in self.brisk_map.get_territories() if territory.player.id == player_id])
        # print 'num_territories', num_territories
        return 3 - (num_territories % 3)

    def territories_needed_for_continent(self, player, continent):
        return [territory for territory in continent.territories if territory.player.id != player.id]

    def territories_needed_for_each_continent(self, player):
        return [(continent, self.territories_needed_for_continent(player, continent)) for continent in self.brisk_map.get_continents()]

    def probability_of_winning_partition_from_starting_territory_and_num_armies(self, territories_in_partition, starting_territory, num_armies):
        pass

    def units_needed_to_win_partition_from_territory(self, territories_in_partition):
        pass

    def compute_next_action(self):

        player = self.player
        player_id = player.id
        enemy_id = 1 if player.id == 2 else 2
        enemy = Player.get(enemy_id)

        print 'player', player.id

        print pprint(player.territories)

        enemy_id = 1 if player_id == 2 else 2
        num_enemy_territories = sum([1 for territory in self.brisk_map.get_territories() if territory.player.id == enemy_id])
        num_enemy_continents = sum([1 for continent in self.brisk_map.get_continents() if continent.player and continent.player.id == enemy_id])

        print self.num_enemy_armies_next_round(player_id)
        print self.num_territories_needed_for_extra_base_armies(player_id)

        print 'num_enemy_territories', num_enemy_territories
        print 'num_enemy_continents', num_enemy_continents

        for continent in self.brisk_map.get_continents():
            print 'territories_needed_for_continent', continent.name
            territories_needed_for_continent = self.territories_needed_for_continent(player, continent)
            print [territory.name for territory in territories_needed_for_continent]
            print 'partitions'
            pprint(Territory.partition_territories(territories_needed_for_continent))


        continent_to_attack = self.brisk_map.get_continent(6)
        enemy_territories = [territory for territory in continent_to_attack.territories if territory.player.id == enemy_id]
        australian_territories = [territory for territory in player.territories if territory.continent and territory.continent.id == 6]

        if player.num_reserves > 0 and len(player.territories) > 0:
            for enemy_territory in enemy_territories:
                for territory in enemy_territory.adjacent_territories:
                    if territory.player.id == player.id:
                        self.territories_with_new_armies.append(territory)
                        print 'player', player, 'placing', player.num_reserves, 'in', territory
                        return 'place_armies', {
                            'territory_id': territory.id,
                            'num_armies': player.num_reserves
                        }
                    
            print 'player', player, 'placing', player.num_reserves, 'in', player.territories[0]
            return 'place_armies', {
                'territory_id': player.territories[0].id,
                'num_armies': player.num_reserves
            }

        if len(australian_territories) > 0:
            if len(enemy_territories) <= 0:
                print 'no enemy territories'
                self.territories_with_new_armies = []
                return 'end_turn', ()

            if len(self.territories_with_new_armies) <= 0:
                print 'no territories with new armies'
                self.territories_with_new_armies = []
                return 'end_turn', ()

            attacker_territory = self.territories_with_new_armies[0]
            for territory in attacker_territory.adjacent_territories:
                print territory.name
                if territory.continent.id == continent_to_attack.id and territory.player.id == enemy_id:
                    defender_territory = territory
                    num_armies = min(attacker_territory.num_armies - 1, 3)
                    if num_armies <= 0:
                        self.territories_with_new_armies = []
                        return 'end_turn', ()
                    print 'attacking from', attacker_territory.name, 'to', defender_territory.name, 'with', num_armies
                    return 'attack', {
                        'attacker_territory_id': attacker_territory.id,
                        'defender_territory_id': defender_territory.id,
                        'num_attacker_armies': num_armies
                    }
        
        # find the continent that is easiest to take over
        # look at the enemy controlled territories in that continent,
        # and the adjacent territories that we control
        # and take the total number of units we can use to attack
        # minus the total number of enemy units
        # minus the number of enemy territories

        # game_state = BriskGameState.create_from_game_state_data(game_state_data)
        
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
