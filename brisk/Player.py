class Player():

    players = {}

    def __init__(self, player_id):
        self.id = player_id
        self.is_current_turn = False
        self.is_eliminated = False
        self.num_armies = 0
        self.num_reserves = 0
        self.territories = []

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
