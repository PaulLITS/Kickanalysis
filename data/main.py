import json
import time
from datetime import datetime

import configargparse
from dateutil.tz import tzlocal

from processing.market import get_market_players
from processing.players import get_players_mw_change,get_matchday_elevens
from processing.players import get_taken_players
from processing.revenue import calculate_team_value_per_day
from processing.turnovers import get_turnovers
from utility.api_manager import manager

p = configargparse.ArgParser(default_config_files=['settings.conf'])
p.add('--mail', required=True)
p.add('--pw', required=True)
p.add('--league', required=False)
p.add('--start', required=True)
p.add('--ignore', required=False, action='append', default=[])

options = p.parse_args()


def main():
    start = time.time()

    manager.init(options)
    manager.get_bonus
    get_turnovers()
    get_taken_players()
    get_players_mw_change()
    calculate_team_value_per_day()
    get_market_players()
    get_matchday_elevens()
    
    # Timestamp for frontend
    # TODO: Possible to use file creation timestamp in frontend, so that this can be removed?
    with open('./data/timestamp.json', 'w') as f:
        f.writelines(json.dumps({'time': datetime.now(tz=tzlocal()).isoformat()}))

    print(f'Total execution time: {round(time.time() - start, 2)}s')


if __name__ == '__main__':
    main()
