from Brisk import Brisk
from BriskBot import BriskBot
from BriskObserver import BriskObserver
import argparse
from pprint import pprint
from time import sleep

def main(args):
    # if args.game_id:
    #     brisk = Brisk(game_id=args.game_id)
    brisk = Brisk()

    while True:
        initial_game_state = brisk.get_game_state()
        if initial_game_state['territories']:
            break
        print 'trying again'
        sleep(1)

    bot = BriskBot(map_layout=brisk.get_map_layout(), initial_game_state=initial_game_state)

    brisk_observer = BriskObserver()

    while True:
        player_status = brisk.get_player_status()

        if player_status['eliminated']:
            print 'Player eliminated'
            break
        action, params = bot.compute_next_action(brisk.player_id, brisk.get_player_status(), brisk.get_game_state())
        if action == 'place_armies':
            pprint(brisk.place_armies(params['territory_id'], params['num_armies']))
        elif action == 'attack':
            pprint(brisk.attack(params['attacker_territory_id'], params['defender_territory_id'], params['num_attacker_armies']))
        elif action == 'transfer_armies':
            pprint(brisk.transfer_armies(params['from_territory_id'], params['to_territory_id'], params['num_armies']))
        elif action == 'end_turn':
            pprint(brisk.end_turn())
        
        brisk_observer.update(brisk)
        sleep(1)


parser = argparse.ArgumentParser()
parser.add_argument('-g', '--game-id', dest='game_id', type=int)
parser.set_defaults(func=main)

args = parser.parse_args()
args.func(args)
