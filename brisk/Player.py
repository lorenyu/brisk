from itertools import groupby
from operator import itemgetter

class Player():

    players = {}

    def __init__(self, player_id):
        self.id = player_id
        self.is_current_turn = False
        self.is_eliminated = False
        self.num_armies = 0
        self.num_reserves = 0
        self.territories = []
        self.territories_by_continent = {}

    @property
    def controlled_continents(self):
        return [continent for continent, territories in self.territories_by_continent.iteritems() if len(continent.territories) == len(territories)]

    @property
    def continents_with_controlled_territory(self):
        return list(set([territory.continent for territory in self.territories]))

    @property
    def num_armies_next_round(self):
        return Player.compute_num_armies_per_round(len(self.territories), self.controlled_continents)

    def get_num_armies_next_round_with_extra_territories(self, extra_territories):
        extra_territories_by_continent_id = {}
        for territory in extra_territories:
            if not extra_territories_by_continent_id.has_key(territory.continent.id):
                extra_territories_by_continent_id[territory.continent.id] = []
            extra_territories_by_continent_id[territory.continent.id].append(territory)
        continents = []
        for continent, territories in self.territories_by_continent.iteritems():
            num_extra_territories_in_continent = len(extra_territories_by_continent_id[continent.id]) if extra_territories_by_continent_id.has_key(continent,id) else 0
            if len(territories) + num_extra_territories_in_continent == len(continent.territories):
                continents.append(continent)

        return Player.compute_num_armies_per_round(len(self.territories) + len(extra_territories), continents)

    @property
    def num_territories_needed_for_extra_base_armies(self):
        num_territories = len(self.territories)
        return 3 - (num_territories % 3)

    def territories_needed_for_continent(self, continent):
        return [territory for territory in continent.territories if territory.player != self]

    def reset_territories(self):
        self.territories = []
        self.territories_by_continent = {}

    def add_territory(self, territory):
        if territory in self.territories:
            return
        self.territories.append(territory)
        if not self.territories_by_continent.has_key(territory.continent):
            self.territories_by_continent[territory.continent] = []
        self.territories_by_continent[territory.continent].append(territory)


    def update(self, player_status_data, brisk_map):
        self.is_current_turn = player_status_data['current_turn']
        self.is_eliminated = player_status_data['eliminated']
        self.num_armies = player_status_data['num_armies']
        self.num_reserves = player_status_data['num_reserves']
        self.reset_territories()
        for territory_data in player_status_data['territories']:
            self.add_territory(brisk_map.get_territory(territory_data['territory']))

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __repr__(self):
        return '<Player:' + str(self.id) + ':' + self.name + '>'

    def __hash__(self):
        return hash(repr(self))

    @staticmethod
    def get(player_id):
        if not Player.players.has_key(player_id):
            Player.players[player_id] = Player(player_id)
        return Player.players[player_id]

    @staticmethod
    def contained_continents(territories):
        territories = set(territories)
        continents = set([territory.continent for territory in territories])
        return filter(lambda continent: territories.issuperset(continent.territories), continents)

    @staticmethod
    def num_armies_per_round_with_territories(territories):
        num_territories = len(territories)
        base = int(num_territories / 3)
        bonus = sum([continent.bonus for continent in Player.contained_continents(territories)])
        return base + bonus

    @staticmethod
    def compute_num_armies_per_round(num_territories, continents):
        base = int(num_territories / 3)
        bonus = sum([continent.bonus for continent in continents])
        return base + bonus