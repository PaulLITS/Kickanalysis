from datetime import datetime
from data.utility.api_manager import parse_date
class BaseModel:
    _json_mapping = {
    }

    _json_transform = {
    }

    def __init__(self, d: dict):
        for key in d.keys():
            value = d[key]

            # Transform if necessary
            if key in self._json_transform:
                value = self._json_transform[key](value)

            if key in self._json_mapping.keys():
                setattr(self, self._json_mapping[key], value)
            setattr(self, key, value)
            

class LeagueMatchDayStatsData(BaseModel):
    user_id: str = None
    day_earnings: float = None
    day_points: int = None
    day_placement: int = None
    day_tendency: int = None
    team_value: int = None
    points: int = None
    placement: int = None
    tendency: int = None
    flags: int = None
    
    def __init__(self, d: dict):
        self._json_transform = {
        }
        self._json_mapping = {
            "dayEarnings": "day_earnings",
            "dayPoints": "day_points",
            "dayPlacement": "day_placement",
            "dayTendency": "day_tendency",
            "teamValue": "team_value"
        }
        
        super().__init__(d)
        
class LeagueData(BaseModel):
    id: str = None
    name: str = None
    
    creator: str = None
    creator_id: int = None
    creation_date: datetime = None
    
    activity_index: float = None
    total_transfers: int = None
    active_users: int = None
    max_users: int = None
    average_points: int = None
    
    pub: bool = None
    gm: int = None
    
    player_limit_active: bool = None
    player_limit: bool = None
    
    image_path: str = None
    
    def __init__(self, d: dict):
        self._json_transform = {
            "creation": parse_date
        }
        self._json_mapping = {
            "creatorId": "creator_id",
            "creation": "creation_date",
            "mpl": "player_limit_active",
            "pl": "player_limit",
            "ci": "image_path",
            "ai": "activity_index",
            "t": "total_transfers",
            "au": "active_users",
            "mu": "max_users",
            "ap": "average_points"
        }
        
        super().__init__(d)