from brisk import *
from brisk.bots import *
import argparse
from pprint import pprint
from time import sleep
import urllib2

def main(args):
    # if args.game_id:
    #     brisk = Brisk(game_id=args.game_id)
    brisks = []
    brisks.append(Brisk('bot A'))
    #brisks.append(Brisk('bot B'))

    brisks[0].create_new_game(False)
    #brisks[1].join_game(brisks[0].game_id)

    players = [Player.get(brisk.player_id) for brisk in brisks]

    while not brisk.get_player_status()['current_turn']:
        print "Game hasn't started yet"
        sleep(1)

    map_layout = brisks[0].get_map_layout()
    initial_game_state = brisks[0].get_game_state()
    brisk_map = BriskMap.create(map_layout, initial_game_state)

    bots = []
    bots.append(BriskBotB(brisk_map, players[0]))
    #bots.append(BriskBotB(brisk_map, players[1]))

    brisk_observer = BriskObserver()

    i = 0
    while True:        

        try:
            player_status = brisk.get_player_status()

            game_state = brisk.get_game_state()
            brisk_map.update(game_state)
            for brisk, player in zip(brisks, players):
                player.update(brisk.get_player_status(), brisk_map)

            bot = bots[i]
            brisk = brisks[i]
            player = players[i]

            if player.is_eliminated:
                print 'Player eliminated'
                break

            if not player.is_current_turn:
                print 'Not player', i,"'s turn"
                #i = (i + 1) % 2
                sleep(1)
                continue

            action, params = bot.compute_next_action()

            if action == 'place_armies':
                territory = params['territory']
                if territory.player != player:
                    print 'Cannot put armies on territory', territory, 'owned by', territory.player
                    continue
                num_armies = min(params['num_armies'], player.num_reserves)
                if num_armies <= 0:
                    print 'Cannot place zero armies'
                    continue
                print 'player ', player.id, 'placed', num_armies, 'in', territory
                brisk.place_armies(territory.id, num_armies)
            elif action == 'attack':
                attacker_territory = params['attacker_territory']
                defender_territory = params['defender_territory']
                num_armies = min(params['num_attacker_armies'], attacker_territory.num_armies - 1, 3)
                if num_armies <= 0:
                    print 'Cannot attack with zero armies'
                    continue
                print 'player ', player.id, 'attacked', defender_territory, 'from', attacker_territory
                result = brisk.attack(attacker_territory.id, defender_territory.id, num_armies)
                if result['defender_territory_captured']:
                    defender_territory.player = attacker_territory.player
                    attacker_territory.num_armies = result['attacker_territory_armies_left']
                    defender_territory.num_armies = result['defender_territory_armies_left']
                    num_armies = bot.compute_num_armies_to_transfer(attacker_territory, defender_territory)
                    print 'player ', player.id, 'transferred', num_armies, 'armies from', attacker_territory, 'to', defender_territory
                    if num_armies > 0:
                        brisk.transfer_armies(attacker_territory.id, defender_territory.id, num_armies)
            elif action == 'transfer_armies':
                #i = (i + 1) % 2
                brisk.transfer_armies(params['from_territory_id'], params['to_territory_id'], params['num_armies'])
            elif action == 'end_turn':
                #i = (i + 1) % 2
                print 'player ', player.id, 'ended their turn'
                brisk.end_turn()
            
            brisk_observer.update(brisk)
        except urllib2.HTTPError, e:
            # i = (i + 1) % 2
            print e


parser = argparse.ArgumentParser()
parser.add_argument('-g', '--game-id', dest='game_id', type=int)
parser.set_defaults(func=main)

args = parser.parse_args()
args.func(args)
