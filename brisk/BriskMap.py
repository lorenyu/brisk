from Territory import Territory
from Continent import Continent
from Player import Player

from collections import deque

class BriskMap():

    def __init__(self):
        self.territories_by_id = {}
        self.continents_by_id = {}

    def add_territory(self, territory):
        self.territories_by_id[territory.id] = territory

    def add_continent(self, continent):
        self.continents_by_id[continent.id] = continent

    def get_territory(self, territory_id):
        return self.territories_by_id[territory_id]

    @property
    def territories(self):
        return self.territories_by_id.values()

    def get_territories(self):
        return self.territories_by_id.values()

    def get_continent(self, continent_id):
        return self.continents_by_id[continent_id]

    @property
    def continents(self):
        return self.continents_by_id.values()

    def get_continents(self):
        return self.continents_by_id.values()

    def get_player_value(self, player):
        return player.num_armies_next_round

    def get_paths_accessible_by_player(self, player, max_length=9999):
        paths = []
        seen_territory_ids = set()

        partial_paths = deque()
        for territory in player.territories:
            partial_paths.append((territory,))
        while len(partial_paths) > 0:
            path = partial_paths.popleft()
            paths.append(path)
            for territory in path[-1].adjacent_territories:
                if territory.player != player and territory not in path:
                    partial_paths.append(path + (territory,))

        return paths

    def value_if_player_conquered_path(self, player, path):
        return float(player.get_num_armies_next_round_with_extra_territories(path))

    def update(self, game_state_data):
        for territory_data in game_state_data['territories']:
            territory = self.get_territory(territory_data['territory'])
            territory.player = Player.get(territory_data['player'])
            territory.num_armies = territory_data['num_armies']

    @staticmethod
    def create(map_layout, game_state_data):
        brisk_map = BriskMap()

        for territory_data in map_layout['territories']:
            territory = Territory(territory_data['territory'], territory_data['territory_name'])
            brisk_map.add_territory(territory)

        for territory_data in map_layout['territories']:
            territory = brisk_map.get_territory(territory_data['territory'])
            for adjacent_territory_id in territory_data['adjacent_territories']:
                territory.add_adjacent_territory(brisk_map.get_territory(adjacent_territory_id))

        for continent_data in map_layout['continents']:
            territories = [brisk_map.get_territory(territory_id) for territory_id in continent_data['territories']]
            continent = Continent(continent_data['continent'], continent_data['continent_bonus'], continent_data['continent_name'], territories)
            for territory in territories:
                territory.continent = continent
            brisk_map.add_continent(continent)

        brisk_map.update(game_state_data)

        return brisk_map

