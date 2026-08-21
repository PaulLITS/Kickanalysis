import json

from dateutil import parser
from tqdm import tqdm

from utility import constants
from utility.api_manager import manager
from utility.util import json_serialize_datetime
from turnovers import get_mv_on_date

def get_taken_players():
    result = []

    for user in tqdm(manager.users, desc="Collecting taken players for each manager"):
        taken_players = []

        transfers = manager.get_transfers_raw(user['i'])
        transfers = sorted(transfers, key=lambda e: e['dt'])
        transfers.reverse()

        for player in manager.league_user_players(user['i']):
            # Default values in case the player got randomly assigned on league join
            
            response = manager.get(f"/leagues/{manager.leagueid}/players/{player["pi"]}/marketvalue/365")["it"]
            buy_value = get_mv_on_date(response,manager.start.date())
            bought_date = manager.start

            # Get date and value of newest buy transfer for that player
            for transfer in transfers:
                if transfer['tty'] != 1 or transfer['pi'] != player["pi"]:
                    continue
                if parser.parse(transfer.get('dt')).date() < manager.start.date():
                    continue
                buy_value = transfer['trp']
                bought_date = parser.parse(transfer['dt'])

                break
            real_player = manager.get(f'/leagues/{manager.leagueid}/players/{player["pi"]}')
            taken_players.append({
                'first_name': real_player.get('fn'),
                'last_name': real_player.get('ln'),
                'team_id': real_player.get('tid'),
                'points': real_player.get('tp'),
                'average_points': real_player.get('ap'),
                'market_value': real_player.get('mv'),
                'buy_price': buy_value,
                'user': user.get('n'),
                'player_id': real_player.get('i'),
                'date': bought_date,
                'position': constants.POSITIONS[real_player['pos']],
                'trend': real_player.get('tfhmvt')
            })

        result = result + taken_players

    with open('./data/taken_players.json', 'w') as f:
        f.writelines(json.dumps(result, default=json_serialize_datetime))

    get_free_players(result)


def get_free_players(taken_players):
    free_players = []

    taken_player_ids = [x['player_id'] for x in taken_players]
    players = []
    pbar = tqdm(constants.TEAM_IDS)

    for team in pbar:
        pbar.set_description(
            f"Getting free players from {constants.TEAM_NAMES[f"{team}"]}"
        )
        for player in manager.get(f'/competitions/1/teams/{team}/teamprofile')["it"]: #change number for different league
            players.append(player)
    
    for player in players:
        if player["i"] not in taken_player_ids:
            real_player = manager.get(f'/leagues/{manager.leagueid}/players/{player["i"]}')
            free_players.append({ 'first_name': real_player.get('fn'),
                                  'last_name': real_player.get('ln'),
                                  'team_id': real_player.get('tid'),
                                  'points': real_player.get('tp'),
                                  'average_points': real_player.get('ap'),
                                  'market_value': real_player.get('mv'),
                                  'player_id': real_player.get('i'),
                                  'position': constants.POSITIONS[real_player['pos']],
                                  'trend': real_player.get('tfhmvt')})

    with open('./data/free_players.json', 'w') as f:
        f.writelines(json.dumps(free_players))


def get_players_mw_change():
    result = []

    players = []
    for team in constants.TEAM_IDS:
        for player in manager.get(f'/competitions/1/teams/{team}/teamprofile')["it"]: #change number for different league
            players.append(player)

    for player in tqdm(players, desc="Collecting market value change of last three days for each player", miniters=2):
        player_stats = manager.get(f'/leagues/{manager.leagueid}/players/{player["i"]}')

        if player_stats['oui'] != "0":
            manager_name = manager.get(f"/leagues/{manager.leagueid}/managers/{player_stats['oui']}/dashboard")['unm']
        else:
            manager_name = 'Computer'

        market_values = manager.get(f'/leagues/{manager.leagueid}/players/{player["i"]}/marketvalue/365')["it"]
        market_values.reverse()

        result.append({'player_id': player_stats.get('i'),
                       'first_name': player_stats.get('fn'),
                       'last_name': player_stats.get('ln'),
                       'market_value': player_stats.get('mv'),
                       'today': market_values[0].get('mv') - market_values[1].get('mv'),
                       'one_day_ago': market_values[1].get('mv') - market_values[2].get('mv'),
                       'two_days_ago': market_values[2].get('mv') - market_values[3].get('mv'),
                       'team_id': player_stats['tid'],
                       'manager': manager_name})

    with open('./data/mw_changes.json', 'w') as f:
        f.writelines(json.dumps(result))


def get_matchday_elevens():
    try:
        with open("./data/matchday_teams.json", "r") as f:
            result = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        result = {}

    current_match_day = manager.league_current_matchday("min")
    if (not result or not all(str(current_match_day) in manager_data
        for manager_data in result.values())) and current_match_day != None:
        
        for user in tqdm(
            manager.users,
            desc="Collecting teams for each Manager"
        ):
            manager_squad = manager.get(
                f"/leagues/{manager.leagueid}/managers/{user['i']}/squad"
            )

            # Get current team value
            current_matchday_team = [player["pi"] for player in manager_squad["it"] if "lo" in player]

            # Get existing manager data or create it
            manager_teams = result.setdefault(user["i"], {})

            # Add current match day's value
            manager_teams[str(current_match_day)] = current_matchday_team

    with open("./data/matchday_teams.json", "w") as f:
        json.dump(result, f, indent=2)
#lol