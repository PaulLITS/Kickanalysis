from data.utility.Api_utility.League_Match_Day_Stats_Data import LeagueMatchDayStatsData
class LeagueStatsResponse:
    
    current_day: int = None
    match_days: dict[int, list[LeagueMatchDayStatsData]] = {}

    def __init__(self, d: dict):
        self.current_day = d["currentDay"]
        for match_day in d["matchDays"]:
            self.match_days[match_day["day"]] = [LeagueMatchDayStatsData(_d) for _d in match_day["users"]]