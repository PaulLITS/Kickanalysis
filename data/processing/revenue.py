import json
from datetime import datetime
from collections import defaultdict
import pandas as pd
from tqdm import tqdm

from utility.api_manager import manager
from utility.constants import MATCH_DAYS
from utility.constants import TIMEZONE_DE

def days_since(date):
    return (datetime.now().date() - date).days

def calculate_revenue_data_daily(turnovers):
    user_transfer_revenue = {user['n']: [] for user in manager.users}
    for buy, sell in turnovers:
        revenue = sell['value'] - buy['value']
        user_transfer_revenue[buy['user']].append((revenue, sell['date']))

    # Add start and end points
    for _, data in user_transfer_revenue.items():
        data.append((0, manager.start))
        data.append((0, datetime.now(TIMEZONE_DE)))

    dataframes = {}
    for user, data in tqdm(user_transfer_revenue.items(), desc="Calculating transfer revenue of transfers"):
        df = pd.DataFrame(data, columns=['revenue', 'date'])
        df['date'] = pd.to_datetime(df['date'], utc=True)
        df = df.groupby(pd.Grouper(key='date', freq='D'))['revenue'] \
            .sum().reset_index().sort_values('date')
        df['revenue'] = df['revenue'].cumsum()
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')

        dataframes[user] = df

    data = {user['n']: [] for user in manager.users}
    for user, df in dataframes.items():
        for entry in df.to_numpy().tolist():
            data[user].append((entry[0], entry[1]))

    with open('./data/revenue_sum.json', 'w') as f:
        f.writelines(json.dumps(data))

        
def calculate_team_value_per_match_day():
    try:
        with open("./data/team_values.json", "r") as f:
            result = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        result = {}
    current_match_day = manager.league_current_matchday("min")
    if (not result or not all(
    str(current_match_day) in manager_data
    for manager_data in result.values())) and current_match_day != None:
        for user in tqdm(
            manager.users,
            desc="Collecting team values for current match day"
        ):
            manager_stats = manager.get(
                f"/leagues/{manager.leagueid}/managers/{user['i']}/dashboard"
            )

            # Get current team value
            current_team_value = manager_stats["tv"]

            # Get existing manager data or create it
            manager_values = result.setdefault(user["i"], {})

            # Add current match day's value
            manager_values[str(current_match_day)] = current_team_value

    with open("./data/team_values.json", "w") as f:
        json.dump(result, f, indent=2)


def calculate_daily_budget():
    # Load existing revenue data
    with open("./data/revenue_sum.json", "r", encoding="utf-8") as f:
        revenue_data = json.load(f)

    current_day = datetime.now().strftime("%Y-%m-%d")

    for user in tqdm(manager.users, desc="Calculating budget for every Manager"):
    
        Response = manager.get(f'/leagues/{manager.leagueid}/managers/{user["i"]}/squad')
        
        total_mvgl = sum(
            player.get("mvgl", 0)
            for player in Response["it"]
        ) + 150000000 + 100000*(days_since(manager.start)+1)

        # user should already exist in revenue_sum.json
        if user["n"] not in revenue_data:
            revenue_data[user["n"]] = []

        # Add MVGL to today's revenue
        if revenue_data[user["n"]]:
            revenue_data[user["n"]][-1][1] += total_mvgl

        else:
            revenue_data[user["n"]].append(
                [current_day, total_mvgl]
            )

    # Save updated data
    with open("./data/budget_sum.json", "w", encoding="utf-8") as f:
        json.dump(revenue_data, f, indent=2, ensure_ascii=False)