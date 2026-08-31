import json
import os
from utility import constants
from utility.api_manager import manager
from tqdm import tqdm

def calculate_expected_points_for_each_manager():
    with open("./data/matchday_teams.json", "r") as f:
            result = json.load(f)
    
    expected_points = {}
        
    for user in tqdm(manager.users,desc="calculating expected points for each user"):
        
        
        expected_points[user["n"]] = [0,0] 
        for day_id,day in result[user["i"]]:
            for player in day:
                performance = manager.get(f"/leagues/{manager.leagueid}/players/{player}/performance")["it"][-1]["ph"][day_id-1]
                player_stats = manager.get(f'/leagues/{manager.leagueid}/players/{player["i"]}')
                
                minutes = performance.get("mp",0)
                points = performance.get("p",0)
                avg_minutes = player_stats.get("sec",0)/60
                avg_points = player_stats.get("ap",0)
                
                if minutes == 0 or avg_minutes == 0:
                    continue
                else:
                    expected_points[user["n"]][1] += avg_points * minutes/avg_minutes
                    expected_points[user["n"]][0] += points
                
    with open("./data/expected_points.json", "w", encoding="utf-8") as f:
        json.dump(expected_points, f, indent=2, ensure_ascii=False,)
                