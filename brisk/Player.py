class Player():

    players = {}

    def __init__(self, player_id):
        self.id = player_id
        self.is_current_turn = False
        self.is_eliminated = False
        self.num_armies = 0
        self.num_reserves = 0
        self.territories = []

    @property
    def controlled_continents(self):
        return Player.contained_continents(self.territories)

    @property
    def continents_with_controlled_territory(self):
        return list(set([territory.continent for territory in self.territories]))

    @property
    def num_armies_next_round(self):
        return Player.num_armies_per_round_with_territories(self.territories)

    def get_num_armies_next_round_with_extra_territories(self, extra_territories):
        territories = set(self.territories)
        territories.update(extra_territories)
        return Player.num_armies_per_round_with_territories(territories)

    @property
    def num_territories_needed_for_extra_base_armies(self):
        num_territories = len(self.territories)
        return 3 - (num_territories % 3)

    def territories_needed_for_continent(self, continent):
        return [territory for territory in continent.territories if territory.player != self]

    def update(self, player_status_data, brisk_map):
        self.is_current_turn = player_status_data['current_turn']
        self.is_eliminated = player_status_data['eliminated']
        self.num_armies = player_status_data['num_armies']
        self.num_reserves = player_status_data['num_reserves']
        self.territories = [ brisk_map.get_territory(territory_data['territory']) for territory_data in player_status_data['territories'] ]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __repr__(self):
        return '<Player:%d>' % self.id

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