import json
import os
from utility import constants
from utility.api_manager import manager


def calculate_events_for_each_manager():
    with open("./data/matchday_teams.json", "r") as f:
            result = json.load(f)
    
    if os.path.exists("./data/events.json"):
            with open("./data/events.json", "r", encoding="utf-8") as I:
                events_data = json.load(I)
            new = False
    else:
        new = True
        events_data = {}
        
    for user in manager.users:
        events_data[user["n"]]["day"] = 0
        if new:
            events_data[user["n"]] = {}
            events_data[user["n"]]["day"] = 0
        
            
        if (manager.league_current_matchday(min) <= len(result[user["i"]])):# -1 and manager.league_current_matchday(min)-1 > events_data[user["n"]]["day"]:
            events_data[user["n"]]["day"] += 1 
            for player in result[user["i"]][str(manager.league_current_matchday(min))]:#-1
                performance = manager.get(f"/leagues/{manager.leagueid}/players/{player}/performance")["it"][-1]["ph"][manager.league_current_matchday(min)-1]
                
                events = performance.get("k")
                
                if events == None:
                    continue
                
                for x in events:
                    events_data[user["n"]][str(x)] = events_data[user["n"]].get(str(x), 0) + 1         
                  
    with open("./data/events.json", "w", encoding="utf-8") as f:
        json.dump(events_data, f, indent=2, ensure_ascii=False,)
                
                
                
                
                