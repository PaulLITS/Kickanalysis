import json
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from pytz import timezone
from tqdm import tqdm

from utility import constants
from utility.api_manager import manager
from utility.util import json_serialize_datetime


def get_market_players():
    result = []

    players = [player for player in manager.get(f"/leagues/{manager.leagueid}/market")["it"] if not player.get("u")]

    for player in tqdm(players, desc="Collecting players on market"):
        real_player = manager.get(f'/leagues/{manager.leagueid}/players/{player["i"]}')
        expiration_time = (datetime.now(timezone('Europe/Berlin')) + timedelta(seconds=int(real_player["exs"])))
        result.append({'first_name': real_player['fn'],
                       'last_name': real_player['ln'],
                       'market_value': real_player['mv'],
                       'expiration': expiration_time,
                       'team_id': real_player['tid'],
                       'position': constants.POSITIONS[real_player['pos']],
                       'trend': real_player['tfhmvt']})

    with open('./data/market.json', 'w') as f:
        f.writelines(json.dumps(result, default=json_serialize_datetime))
