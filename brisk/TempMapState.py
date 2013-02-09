class TempMapState:
    def __init__(self, brisk_map):
        self.brisk_map = brisk_map
        self.players_controlling_territory_by_territory_id = {}
        self.num_armies_by_territory_id = {}

        player_ids = range(1, self.brisk_map.num_players + 1)

        self.num_controlled_territories_by_player_id = dict([(player_id, 0) for player_id in player_ids])
        self.num_controlled_territories_by_player_id_and_continent_id = dict([((player_id, continent.id), 0) for player_id in player_ids for continent in self.brisk_map.continents])
        self.controlled_continents_by_player_id = dict([(player_id, []) for player_id in player_ids])
        self.num_fronts_by_player_id = dict([(player_id, 0) for player_id in player_ids])
        self.num_armies_by_player_id = dict([(player_id, 0) for player_id in player_ids])
        self.num_armies_at_front_by_player_id = dict([(player_id, 0) for player_id in player_ids])
        

    def set_player_controlling_territory(self, territory, player):
        self.players_controlling_territory_by_territory_id[territory.id] = player

    def set_num_armies_for_territory(self, territory, num_armies):
        self.num_armies_by_territory_id[territory.id] = num_armies

    def compute_map_values(self):
        for territory in self.brisk_map.territories:
            player = self.player_controlling_territory(territory)
            num_armies = self.num_armies_in_territory(territory)

            self.num_armies_by_player_id[player.id] += num_armies

            self.num_controlled_territories_by_player_id[player.id] += 1
            self.num_controlled_territories_by_player_id_and_continent_id[(player.id, territory.continent.id)] += 1
            if self.num_controlled_territories_by_player_id_and_continent_id[(player.id, territory.continent.id)] == len(territory.continent.territories):
                self.controlled_continents_by_player_id[player.id].append(territory.continent)

            if any([adjacent_territory.player != territory.player for adjacent_territory in territory.adjacent_territories]):
                self.num_fronts_by_player_id[player.id] += 1
                self.num_armies_at_front_by_player_id[player.id] += num_armies

    def num_armies_for_player(self, player):
        return self.num_armies_by_player_id[player.id]

    def num_fronts_for_player(self, player):
        return self.num_fronts_by_player_id[player.id]

    def num_armies_at_front_for_player(self, player):
        return self.num_armies_at_front_by_player_id[player.id]

    def num_armies_next_round_for_player(self, player):
        num_territories = self.num_controlled_territories_by_player_id[player.id]
        continents = self.controlled_continents_by_player_id[player.id]
        return TempMapState.compute_num_armies_per_round(num_territories, continents)

    # def push_state(self, players_controlling_territory_by_territory_id={}, num_armies_by_territory_id = {}):
    #     self.temp_states.append((players_controlling_territory_by_territory_id, num_armies_by_territory_id))

    # def pop_state(self):
    #     self.temp_states.pop()

    def player_controlling_territory(self, territory):
        if self.players_controlling_territory_by_territory_id.has_key(territory.id):
            return self.players_controlling_territory_by_territory_id[territory.id]
        return territory.player

    def num_armies_in_territory(self, territory):
        if self.num_armies_by_territory_id.has_key(territory.id):
            return self.num_armies_by_territory_id[territory.id]
        return territory.num_armies

    @staticmethod
    def compute_num_armies_per_round(num_territories, continents):
        base = int(num_territories / 3)
        bonus = sum([continent.bonus for continent in continents])
        return base + bonus
