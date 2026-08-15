import json

from dateutil import parser
from tqdm import tqdm

from utility import constants
from utility.api_manager import manager
from utility.util import json_serialize_datetime


def get_taken_players():
    result = []

    for user in tqdm(manager.users, desc="Collecting taken players for each manager"):
        taken_players = []

        transfers = manager.get_transfers_raw(user['i'])
        transfers = sorted(transfers, key=lambda e: e['dt'])
        transfers.reverse()

        for player in manager.league_user_players(user['i']):
            # Default values in case the player got randomly assigned on league join
            buy_value = 0
            bought_date = manager.start

            # Get date and value of newest buy transfer for that player
            for transfer in transfers:
                if transfer['tty'] != 2 or transfer['pi'] != player["pi"]:
                    continue

                buy_value = transfer['trp']
                bought_date = parser.parse(transfer['dt'])

                break
            real_player = manager.get(f'/leagues/{manager.leagueid}/players/{player["pi"]}')
            taken_players.append({
                'first_name': real_player['fn'],
                'last_name': real_player['ln'],
                'team_id': real_player['tid'],
                'points': real_player.get('tp'),
                'average_points': real_player.get('ap'),
                'market_value': real_player['mv'],
                'buy_price': buy_value,
                'user': user['n'],
                'player_id': real_player['i'],
                'date': bought_date,
                'position': constants.POSITIONS[real_player['pos']],
                'trend': real_player['tfhmvt']
            })

        result = result + taken_players

    with open('./data/taken_players.json', 'w') as f:
        f.writelines(json.dumps(result, default=json_serialize_datetime))

    get_free_players(result)


def get_free_players(taken_players):
    free_players = []

    taken_player_ids = [x['player_id'] for x in taken_players]

    
    for player in manager.get(f'/competitions/2/players')["it"]: #change the number for other leagues then bundesliga
        if player["pi"] not in taken_player_ids:
            real_player = manager.get(f'/leagues/{manager.leagueid}/players/{player["pi"]}')
            free_players.append({ 'first_name': real_player['fn'],
                                  'last_name': real_player['ln'],
                                  'team_id': real_player['tid'],
                                  'points': real_player.get('tp'),
                                  'average_points': real_player.get('ap'),
                                  'market_value': real_player['mv'],
                                  'buy_price': real_player['cv'],
                                  'player_id': real_player['i'],
                                  'position': constants.POSITIONS[real_player['pos']],
                                  'trend': real_player['tfhmvt']})

    with open('./data/free_players.json', 'w') as f:
        f.writelines(json.dumps(free_players))


def get_players_mw_change():
    result = []

    players = []
    for player in manager.get(f'/competitions/1/players')["it"]:
            players.append(player)

    for player in tqdm(players, desc="Collecting market value change of last three days for each player", miniters=2):
        player_stats = manager.get(f'/leagues/{manager.leagueid}/players/{player["pi"]}')

        if player_stats['oui'] != "0":
            manager_name = player_stats['oui']
        else:
            manager_name = 'Computer'

        market_values = manager.get(f'/leagues/{manager.leagueid}/players/8329/marketvalue/365')["it"]
        market_values.reverse()

        result.append({'player_id': player_stats['i'],
                       'first_name': player_stats['fn'],
                       'last_name': player_stats['ln'],
                       'market_value': player_stats['mv'],
                       'today': market_values[0]['mv'] - market_values[1]['mv'],
                       'one_day_ago': market_values[1]['mv'] - market_values[2]['mv'],
                       'two_days_ago': market_values[2]['mv'] - market_values[3]['mv'],
                       'team_id': player_stats['tid'],
                       'manager': manager_name})

    with open('./data/mw_changes.json', 'w') as f:
        f.writelines(json.dumps(result))
