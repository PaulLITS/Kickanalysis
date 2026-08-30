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
        
        if new:
            events_data[user["n"]] = {}
        
        
            
        if manager.league_current_matchday(min) <= len(result[user["i"]]):
            for player in result[user["i"]][str(manager.league_current_matchday(min))]: 
                performance = manager.get(f"/leagues/{manager.leagueid}/players/{player}/performance")["it"][-1]["ph"][manager.league_current_matchday(min)-2]
                
                events = performance.get("k")
                
                if events == None:
                    continue
                
                for x in events:
                    events_data[user["n"]][x] += 1
                    
    with open("./data/events.json", "w", encoding="utf-8") as f:
        json.dump(events_data, f, indent=2, ensure_ascii=False,)
                
                
                
                
                