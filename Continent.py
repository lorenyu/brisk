class Continent():

    def __init__(self, id, bonus, name, territories):
        self.id = id
        self.bonus = bonus
        self.name = name
        self.territories = territories
        pass

    @property
    def player(self):
        player_ids_in_continent = set()
        for territory in self.territories:
            player_ids_in_continent.add(territory.player.id)
        
        if len(players_in_continent) == 1:
            return Player.get(player_ids_in_continent.pop())

        return None