from datetime import datetime

import pytz

TIMEZONE_DE = pytz.timezone('Europe/Berlin')

# 2 Bayern
# 3 BVB
# 4 Frankfurt
# 5 Freiburg
# 7 Bayer
# 8 Schalke
# 9 Stuttgart
# 10 Bremen
# 11 Wolfsburg
# 13 Augsburg
# 14 Hoffenheim
# 15 Gladbach
# 18 Mainz
# 20 Hertha
# 24 Bochum
# 28 Köln
# 39 St Pauli
# 40 Union
# 42 Darmstadt
# 43 Leipzig
# 50 Heidenheim
# 51 Holstein Kiel
"""TEAM_NAMES = {
    "2": "FC Bayern München",
    "3": "Borussia Dortmund",
    "4": "Eintracht Frankfurt",
    "5": "SC Freiburg",
    "6": "Hamburger SV",
    "7": "Bayer 04 Leverkusen",
    "8": "FC Schalke 04",
    "9": "VfB Stuttgart",
    "10": "SV Werder Bremen",
    "13": "FC Augsburg",
    "14": "TSG Hoffenheim",
    "15": "Borussia Mönchengladbach",
    "18": "1. FSV Mainz 05",
    "28": "1. FC Köln",
    "29": "SC Paderborn 07",
    "40": "1. FC Union Berlin",
    "43": "RB Leipzig",
    "77": "SV Elversberg"
}"""


TEAM_IDS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 18, 28, 29, 40, 43, 77]

POSITIONS = {1: 'TW', 2: 'ABW', 3: 'MF', 4: 'ANG'}

MATCH_DAYS = {
    1: datetime(2026, 8, 28, 20, 30, tzinfo=TIMEZONE_DE),
    2: datetime(2026, 9, 4, 20, 30, tzinfo=TIMEZONE_DE),
    3: datetime(2026, 9, 11, 20, 30, tzinfo=TIMEZONE_DE),
    4: datetime(2026, 9, 18, 20, 30, tzinfo=TIMEZONE_DE),
    5: datetime(2026, 10, 10, 15, 30, tzinfo=TIMEZONE_DE),
    6: datetime(2026, 10, 17, 15, 30, tzinfo=TIMEZONE_DE),
    7: datetime(2026, 10, 24, 15, 30, tzinfo=TIMEZONE_DE),
    8: datetime(2026, 10, 31, 14, 30, tzinfo=TIMEZONE_DE),
    9: datetime(2026, 11, 7, 14, 30, tzinfo=TIMEZONE_DE),
    10: datetime(2026, 11, 21, 14, 30, tzinfo=TIMEZONE_DE),
    11: datetime(2026, 11, 28, 14, 30, tzinfo=TIMEZONE_DE),
    12: datetime(2026, 12, 5, 14, 30, tzinfo=TIMEZONE_DE),
    13: datetime(2026, 12, 12, 14, 30, tzinfo=TIMEZONE_DE),
    14: datetime(2026, 12, 19, 14, 30, tzinfo=TIMEZONE_DE),
    15: datetime(2027, 1, 9, 14, 30, tzinfo=TIMEZONE_DE),
    16: datetime(2027, 1, 13, 14, 30, tzinfo=TIMEZONE_DE),
    17: datetime(2027, 1, 16, 14, 30, tzinfo=TIMEZONE_DE),
    18: datetime(2027, 1, 23, 14, 30, tzinfo=TIMEZONE_DE),
    19: datetime(2027, 1, 30, 14, 30, tzinfo=TIMEZONE_DE),
    20: datetime(2027, 2, 6, 14, 30, tzinfo=TIMEZONE_DE),
    21: datetime(2027, 2, 13, 14, 30, tzinfo=TIMEZONE_DE),
    22: datetime(2027, 2, 20, 14, 30, tzinfo=TIMEZONE_DE),
    23: datetime(2027, 2, 27, 14, 30, tzinfo=TIMEZONE_DE),
    24: datetime(2027, 3, 3, 14, 30, tzinfo=TIMEZONE_DE),
    25: datetime(2027, 3, 6, 14, 30, tzinfo=TIMEZONE_DE),
    26: datetime(2027, 3, 13, 14, 30, tzinfo=TIMEZONE_DE),
    27: datetime(2027, 3, 20, 14, 30, tzinfo=TIMEZONE_DE),
    28: datetime(2027, 4, 3, 15, 30, tzinfo=TIMEZONE_DE),
    29: datetime(2027, 4, 10, 15, 30, tzinfo=TIMEZONE_DE),
    30: datetime(2027, 4, 17, 15, 30, tzinfo=TIMEZONE_DE),
    31: datetime(2027, 4, 24, 15, 30, tzinfo=TIMEZONE_DE),
    32: datetime(2027, 5, 8, 15, 30, tzinfo=TIMEZONE_DE),
    33: datetime(2027, 5, 15, 15, 30, tzinfo=TIMEZONE_DE),
    34: datetime(2027, 5, 22, 15, 30, tzinfo=TIMEZONE_DE),
}