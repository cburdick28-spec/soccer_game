"""
game_data.py - Player database + game-logic helpers for Soccer Career Guesser.
"""

from __future__ import annotations
import random
from typing import Optional

LEAGUES = [
    "All Leagues", "Premier League", "La Liga", "Serie A",
    "Bundesliga", "Ligue 1", "MLS", "Eredivisie",
    "Primeira Liga", "Saudi Pro League",
]

POSITIONS = {
    "Goalkeeper": ["GK"],
    "Defender":   ["CB", "RB", "LB", "SW"],
    "Midfielder": ["CM", "CDM", "CAM", "LM", "RM"],
    "Forward":    ["LW", "RW", "CF", "ST"],
}

ERAS = {
    "All Eras":  (1900, 2100),
    "1990s":     (1990, 1999),
    "2000s":     (2000, 2009),
    "2010s":     (2010, 2019),
    "2020s":     (2020, 2030),
}

LEAGUE_COLOURS = {
    "Premier League":   "#38003c",
    "La Liga":          "#ee8707",
    "Serie A":          "#003399",
    "Bundesliga":       "#d20515",
    "Ligue 1":          "#00529f",
    "MLS":              "#1e3f6e",
    "Eredivisie":       "#ff6600",
    "Primeira Liga":    "#006600",
    "Saudi Pro League": "#006400",
    "Other":            "#555555",
}

FLAGS = {
    "Argentina": "🇦🇷", "Portugal": "🇵🇹", "Brazil": "🇧🇷",
    "France": "🇫🇷", "Germany": "🇩🇪", "Spain": "🇪🇸",
    "Netherlands": "🇳🇱", "Belgium": "🇧🇪", "Italy": "🇮🇹",
    "Croatia": "🇭🇷", "Sweden": "🇸🇪", "Poland": "🇵🇱",
    "Senegal": "🇸🇳", "Egypt": "🇪🇬", "Ivory Coast": "🇨🇮",
    "Cameroon": "🇨🇲", "Norway": "🇳🇴", "Denmark": "🇩🇰",
    "England": "🏴", "Scotland": "🏴",
}

ATTRIBUTE_LABELS = {
    "nationality":       "Nationality",
    "position_group":    "Position Group",
    "league":            "Main League",
    "age":               "Age Group",
    "current_club":      "Current / Last Club",
    "ballon_dor_winner": "Ballon d'Or Winner",
}

PLAYERS = [
    {
        "name": "Lionel Messi",
        "nationality": "Argentina",
        "position": "RW/CF",
        "position_group": "Forward",
        "birth_year": 1987,
        "current_club": "Inter Miami",
        "career": [
            {
                "club": "Barcelona B",
                "league": "Segunda Division B",
                "years": "2003-04",
                "start": 2003,
                "end": 2004
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2004-21",
                "start": 2004,
                "end": 2021
            },
            {
                "club": "Paris Saint-Germain",
                "league": "Ligue 1",
                "years": "2021-23",
                "start": 2021,
                "end": 2023
            },
            {
                "club": "Inter Miami",
                "league": "MLS",
                "years": "2023-",
                "start": 2023,
                "end": None
            }
        ],
        "trophies": [
            "FIFA World Cup 2022",
            "Copa America 2021",
            "UEFA Champions League x4",
            "La Liga x10",
            "Copa del Rey x7"
        ],
        "ballon_dor": 8,
        "difficulty": "Easy"
    },
    {
        "name": "Cristiano Ronaldo",
        "nationality": "Portugal",
        "position": "LW/ST",
        "position_group": "Forward",
        "birth_year": 1985,
        "current_club": "Al-Nassr",
        "career": [
            {
                "club": "Sporting CP",
                "league": "Primeira Liga",
                "years": "2002-03",
                "start": 2002,
                "end": 2003
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "2003-09",
                "start": 2003,
                "end": 2009
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2009-18",
                "start": 2009,
                "end": 2018
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2018-21",
                "start": 2018,
                "end": 2021
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "2021-22",
                "start": 2021,
                "end": 2022
            },
            {
                "club": "Al-Nassr",
                "league": "Saudi Pro League",
                "years": "2023-",
                "start": 2023,
                "end": None
            }
        ],
        "trophies": [
            "UEFA Champions League x5",
            "Premier League x3",
            "La Liga x2",
            "Serie A x2",
            "UEFA Euro 2016"
        ],
        "ballon_dor": 5,
        "difficulty": "Easy"
    },
    {
        "name": "Neymar Jr",
        "nationality": "Brazil",
        "position": "LW/CF",
        "position_group": "Forward",
        "birth_year": 1992,
        "current_club": "Al-Hilal",
        "career": [
            {
                "club": "Santos",
                "league": "Brasileirao",
                "years": "2009-13",
                "start": 2009,
                "end": 2013
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2013-17",
                "start": 2013,
                "end": 2017
            },
            {
                "club": "Paris Saint-Germain",
                "league": "Ligue 1",
                "years": "2017-23",
                "start": 2017,
                "end": 2023
            },
            {
                "club": "Al-Hilal",
                "league": "Saudi Pro League",
                "years": "2023-",
                "start": 2023,
                "end": None
            }
        ],
        "trophies": [
            "Copa America 2019",
            "UEFA Champions League 2015",
            "La Liga x2",
            "Ligue 1 x5"
        ],
        "ballon_dor": 0,
        "difficulty": "Easy"
    },
    {
        "name": "Kylian Mbappe",
        "nationality": "France",
        "position": "CF/LW",
        "position_group": "Forward",
        "birth_year": 1998,
        "current_club": "Real Madrid",
        "career": [
            {
                "club": "AS Monaco",
                "league": "Ligue 1",
                "years": "2015-17",
                "start": 2015,
                "end": 2017
            },
            {
                "club": "Paris Saint-Germain",
                "league": "Ligue 1",
                "years": "2017-24",
                "start": 2017,
                "end": 2024
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2024-",
                "start": 2024,
                "end": None
            }
        ],
        "trophies": [
            "FIFA World Cup 2018",
            "UEFA Nations League 2021",
            "Ligue 1 x7",
            "UEFA Champions League 2024"
        ],
        "ballon_dor": 0,
        "difficulty": "Easy"
    },
    {
        "name": "Erling Haaland",
        "nationality": "Norway",
        "position": "ST",
        "position_group": "Forward",
        "birth_year": 2000,
        "current_club": "Manchester City",
        "career": [
            {
                "club": "Bryne FK",
                "league": "Norwegian Football",
                "years": "2016-17",
                "start": 2016,
                "end": 2017
            },
            {
                "club": "Molde",
                "league": "Eliteserien",
                "years": "2017-19",
                "start": 2017,
                "end": 2019
            },
            {
                "club": "RB Salzburg",
                "league": "Austrian Bundesliga",
                "years": "2019-20",
                "start": 2019,
                "end": 2020
            },
            {
                "club": "Borussia Dortmund",
                "league": "Bundesliga",
                "years": "2020-22",
                "start": 2020,
                "end": 2022
            },
            {
                "club": "Manchester City",
                "league": "Premier League",
                "years": "2022-",
                "start": 2022,
                "end": None
            }
        ],
        "trophies": [
            "Premier League x2",
            "FA Cup 2023",
            "UEFA Champions League 2023"
        ],
        "ballon_dor": 0,
        "difficulty": "Easy"
    },
    {
        "name": "Thierry Henry",
        "nationality": "France",
        "position": "ST/LW",
        "position_group": "Forward",
        "birth_year": 1977,
        "current_club": "Retired",
        "career": [
            {
                "club": "Monaco",
                "league": "Ligue 1",
                "years": "1994-99",
                "start": 1994,
                "end": 1999
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "1999",
                "start": 1999,
                "end": 1999
            },
            {
                "club": "Arsenal",
                "league": "Premier League",
                "years": "1999-07",
                "start": 1999,
                "end": 2007
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2007-10",
                "start": 2007,
                "end": 2010
            },
            {
                "club": "New York Red Bulls",
                "league": "MLS",
                "years": "2010-14",
                "start": 2010,
                "end": 2014
            }
        ],
        "trophies": [
            "FIFA World Cup 1998",
            "UEFA Euro 2000",
            "Premier League x2",
            "FA Cup x3"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Ronaldo Nazario",
        "nationality": "Brazil",
        "position": "CF/ST",
        "position_group": "Forward",
        "birth_year": 1976,
        "current_club": "Retired",
        "career": [
            {
                "club": "Cruzeiro",
                "league": "Brasileirao",
                "years": "1993-94",
                "start": 1993,
                "end": 1994
            },
            {
                "club": "PSV Eindhoven",
                "league": "Eredivisie",
                "years": "1994-96",
                "start": 1994,
                "end": 1996
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "1996-97",
                "start": 1996,
                "end": 1997
            },
            {
                "club": "Inter Milan",
                "league": "Serie A",
                "years": "1997-02",
                "start": 1997,
                "end": 2002
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2002-07",
                "start": 2002,
                "end": 2007
            },
            {
                "club": "AC Milan",
                "league": "Serie A",
                "years": "2007-08",
                "start": 2007,
                "end": 2008
            },
            {
                "club": "Corinthians",
                "league": "Brasileirao",
                "years": "2009-11",
                "start": 2009,
                "end": 2011
            }
        ],
        "trophies": [
            "FIFA World Cup 1994 & 2002",
            "UEFA Champions League 1998",
            "La Liga 2003"
        ],
        "ballon_dor": 3,
        "difficulty": "Hard"
    },
    {
        "name": "Karim Benzema",
        "nationality": "France",
        "position": "CF/ST",
        "position_group": "Forward",
        "birth_year": 1987,
        "current_club": "Al-Ittihad",
        "career": [
            {
                "club": "Lyon",
                "league": "Ligue 1",
                "years": "2004-09",
                "start": 2004,
                "end": 2009
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2009-23",
                "start": 2009,
                "end": 2023
            },
            {
                "club": "Al-Ittihad",
                "league": "Saudi Pro League",
                "years": "2023-",
                "start": 2023,
                "end": None
            }
        ],
        "trophies": [
            "UEFA Champions League x5",
            "La Liga x4",
            "Ballon d'Or 2022"
        ],
        "ballon_dor": 1,
        "difficulty": "Medium"
    },
    {
        "name": "Harry Kane",
        "nationality": "England",
        "position": "ST",
        "position_group": "Forward",
        "birth_year": 1993,
        "current_club": "Bayern Munich",
        "career": [
            {
                "club": "Tottenham Hotspur",
                "league": "Premier League",
                "years": "2011-23",
                "start": 2011,
                "end": 2023
            },
            {
                "club": "Leyton Orient (loan)",
                "league": "League One",
                "years": "2011",
                "start": 2011,
                "end": 2011
            },
            {
                "club": "Millwall (loan)",
                "league": "Championship",
                "years": "2012",
                "start": 2012,
                "end": 2012
            },
            {
                "club": "Norwich City (loan)",
                "league": "Championship",
                "years": "2012-13",
                "start": 2012,
                "end": 2013
            },
            {
                "club": "Leicester City (loan)",
                "league": "Championship",
                "years": "2013",
                "start": 2013,
                "end": 2013
            },
            {
                "club": "Bayern Munich",
                "league": "Bundesliga",
                "years": "2023-",
                "start": 2023,
                "end": None
            }
        ],
        "trophies": [
            "League Cup 2008"
        ],
        "ballon_dor": 0,
        "difficulty": "Easy"
    },
    {
        "name": "Zlatan Ibrahimovic",
        "nationality": "Sweden",
        "position": "ST",
        "position_group": "Forward",
        "birth_year": 1981,
        "current_club": "Retired",
        "career": [
            {
                "club": "Malmo FF",
                "league": "Allsvenskan",
                "years": "1999-01",
                "start": 1999,
                "end": 2001
            },
            {
                "club": "Ajax",
                "league": "Eredivisie",
                "years": "2001-04",
                "start": 2001,
                "end": 2004
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2004-06",
                "start": 2004,
                "end": 2006
            },
            {
                "club": "Inter Milan",
                "league": "Serie A",
                "years": "2006-09",
                "start": 2006,
                "end": 2009
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2009-10",
                "start": 2009,
                "end": 2010
            },
            {
                "club": "AC Milan",
                "league": "Serie A",
                "years": "2010-12",
                "start": 2010,
                "end": 2012
            },
            {
                "club": "Paris Saint-Germain",
                "league": "Ligue 1",
                "years": "2012-16",
                "start": 2012,
                "end": 2016
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "2016-18",
                "start": 2016,
                "end": 2018
            },
            {
                "club": "LA Galaxy",
                "league": "MLS",
                "years": "2018-19",
                "start": 2018,
                "end": 2019
            },
            {
                "club": "AC Milan",
                "league": "Serie A",
                "years": "2020-23",
                "start": 2020,
                "end": 2023
            }
        ],
        "trophies": [
            "Serie A x5",
            "Ligue 1 x4",
            "Europa League 2017",
            "La Liga 2010"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Robert Lewandowski",
        "nationality": "Poland",
        "position": "ST",
        "position_group": "Forward",
        "birth_year": 1988,
        "current_club": "Barcelona",
        "career": [
            {
                "club": "Znicz Pruszkow",
                "league": "II Liga",
                "years": "2006-08",
                "start": 2006,
                "end": 2008
            },
            {
                "club": "Lech Poznan",
                "league": "Ekstraklasa",
                "years": "2008-10",
                "start": 2008,
                "end": 2010
            },
            {
                "club": "Borussia Dortmund",
                "league": "Bundesliga",
                "years": "2010-14",
                "start": 2010,
                "end": 2014
            },
            {
                "club": "Bayern Munich",
                "league": "Bundesliga",
                "years": "2014-22",
                "start": 2014,
                "end": 2022
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2022-",
                "start": 2022,
                "end": None
            }
        ],
        "trophies": [
            "UEFA Champions League 2020",
            "Bundesliga x9",
            "La Liga 2023"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Didier Drogba",
        "nationality": "Ivory Coast",
        "position": "ST",
        "position_group": "Forward",
        "birth_year": 1978,
        "current_club": "Retired",
        "career": [
            {
                "club": "Le Mans",
                "league": "Ligue 2",
                "years": "1998-02",
                "start": 1998,
                "end": 2002
            },
            {
                "club": "Gueugnon",
                "league": "Ligue 2",
                "years": "2002-03",
                "start": 2002,
                "end": 2003
            },
            {
                "club": "Marseille",
                "league": "Ligue 1",
                "years": "2003-04",
                "start": 2003,
                "end": 2004
            },
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "2004-12",
                "start": 2004,
                "end": 2012
            },
            {
                "club": "Shanghai Shenhua",
                "league": "Chinese Super League",
                "years": "2012-13",
                "start": 2012,
                "end": 2013
            },
            {
                "club": "Galatasaray",
                "league": "Super Lig",
                "years": "2013-14",
                "start": 2013,
                "end": 2014
            },
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "2014-15",
                "start": 2014,
                "end": 2015
            },
            {
                "club": "Montreal Impact",
                "league": "MLS",
                "years": "2015-16",
                "start": 2015,
                "end": 2016
            }
        ],
        "trophies": [
            "Premier League x4",
            "FA Cup x4",
            "UEFA Champions League 2012"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Samuel Eto'o",
        "nationality": "Cameroon",
        "position": "CF/ST",
        "position_group": "Forward",
        "birth_year": 1981,
        "current_club": "Retired",
        "career": [
            {
                "club": "Mallorca",
                "league": "La Liga",
                "years": "1997-04",
                "start": 1997,
                "end": 2004
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2004-09",
                "start": 2004,
                "end": 2009
            },
            {
                "club": "Inter Milan",
                "league": "Serie A",
                "years": "2009-11",
                "start": 2009,
                "end": 2011
            },
            {
                "club": "Anzhi Makhachkala",
                "league": "Russian Premier League",
                "years": "2011-13",
                "start": 2011,
                "end": 2013
            },
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "2013-14",
                "start": 2013,
                "end": 2014
            },
            {
                "club": "Everton",
                "league": "Premier League",
                "years": "2014-15",
                "start": 2014,
                "end": 2015
            },
            {
                "club": "Sampdoria",
                "league": "Serie A",
                "years": "2015-16",
                "start": 2015,
                "end": 2016
            }
        ],
        "trophies": [
            "UEFA Champions League x2",
            "La Liga x3",
            "Serie A 2010",
            "Africa Cup of Nations 2000"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Sadio Mane",
        "nationality": "Senegal",
        "position": "LW/ST",
        "position_group": "Forward",
        "birth_year": 1992,
        "current_club": "Al-Nassr",
        "career": [
            {
                "club": "Metz",
                "league": "Ligue 2",
                "years": "2011-12",
                "start": 2011,
                "end": 2012
            },
            {
                "club": "Red Bull Salzburg",
                "league": "Austrian Bundesliga",
                "years": "2012-14",
                "start": 2012,
                "end": 2014
            },
            {
                "club": "Southampton",
                "league": "Premier League",
                "years": "2014-16",
                "start": 2014,
                "end": 2016
            },
            {
                "club": "Liverpool",
                "league": "Premier League",
                "years": "2016-22",
                "start": 2016,
                "end": 2022
            },
            {
                "club": "Bayern Munich",
                "league": "Bundesliga",
                "years": "2022-23",
                "start": 2022,
                "end": 2023
            },
            {
                "club": "Al-Nassr",
                "league": "Saudi Pro League",
                "years": "2023-",
                "start": 2023,
                "end": None
            }
        ],
        "trophies": [
            "Premier League 2020",
            "UEFA Champions League 2019",
            "Africa Cup of Nations 2022",
            "Bundesliga 2023"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Mohamed Salah",
        "nationality": "Egypt",
        "position": "RW",
        "position_group": "Forward",
        "birth_year": 1992,
        "current_club": "Liverpool",
        "career": [
            {
                "club": "El Mokawloon",
                "league": "Egyptian Premier League",
                "years": "2010-12",
                "start": 2010,
                "end": 2012
            },
            {
                "club": "Basel",
                "league": "Swiss Super League",
                "years": "2012-14",
                "start": 2012,
                "end": 2014
            },
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "2014-16",
                "start": 2014,
                "end": 2016
            },
            {
                "club": "Fiorentina (loan)",
                "league": "Serie A",
                "years": "2015",
                "start": 2015,
                "end": 2015
            },
            {
                "club": "Roma (loan)",
                "league": "Serie A",
                "years": "2015-16",
                "start": 2015,
                "end": 2016
            },
            {
                "club": "Roma",
                "league": "Serie A",
                "years": "2016-17",
                "start": 2016,
                "end": 2017
            },
            {
                "club": "Liverpool",
                "league": "Premier League",
                "years": "2017-",
                "start": 2017,
                "end": None
            }
        ],
        "trophies": [
            "Premier League 2020",
            "UEFA Champions League 2019"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Eden Hazard",
        "nationality": "Belgium",
        "position": "CAM/LW",
        "position_group": "Forward",
        "birth_year": 1991,
        "current_club": "Retired",
        "career": [
            {
                "club": "Lille",
                "league": "Ligue 1",
                "years": "2005-12",
                "start": 2005,
                "end": 2012
            },
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "2012-19",
                "start": 2012,
                "end": 2019
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2019-23",
                "start": 2019,
                "end": 2023
            }
        ],
        "trophies": [
            "Premier League x2",
            "FA Cup x2",
            "Europa League x2",
            "UEFA Champions League x2"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Ronaldinho",
        "nationality": "Brazil",
        "position": "CAM/LW",
        "position_group": "Forward",
        "birth_year": 1980,
        "current_club": "Retired",
        "career": [
            {
                "club": "Gremio",
                "league": "Brasileirao",
                "years": "1998-01",
                "start": 1998,
                "end": 2001
            },
            {
                "club": "Paris Saint-Germain",
                "league": "Ligue 1",
                "years": "2001-03",
                "start": 2001,
                "end": 2003
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2003-08",
                "start": 2003,
                "end": 2008
            },
            {
                "club": "AC Milan",
                "league": "Serie A",
                "years": "2008-11",
                "start": 2008,
                "end": 2011
            },
            {
                "club": "Flamengo",
                "league": "Brasileirao",
                "years": "2011-12",
                "start": 2011,
                "end": 2012
            },
            {
                "club": "Atletico Mineiro",
                "league": "Brasileirao",
                "years": "2012-14",
                "start": 2012,
                "end": 2014
            },
            {
                "club": "Queretaro",
                "league": "Liga MX",
                "years": "2014-15",
                "start": 2014,
                "end": 2015
            }
        ],
        "trophies": [
            "FIFA World Cup 2002",
            "UEFA Champions League 2006",
            "La Liga x2"
        ],
        "ballon_dor": 2,
        "difficulty": "Medium"
    },
    {
        "name": "Wayne Rooney",
        "nationality": "England",
        "position": "CF/ST",
        "position_group": "Forward",
        "birth_year": 1985,
        "current_club": "Retired",
        "career": [
            {
                "club": "Everton",
                "league": "Premier League",
                "years": "2002-04",
                "start": 2002,
                "end": 2004
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "2004-17",
                "start": 2004,
                "end": 2017
            },
            {
                "club": "Everton",
                "league": "Premier League",
                "years": "2017-18",
                "start": 2017,
                "end": 2018
            },
            {
                "club": "DC United",
                "league": "MLS",
                "years": "2018-19",
                "start": 2018,
                "end": 2019
            },
            {
                "club": "Derby County",
                "league": "Championship",
                "years": "2020-21",
                "start": 2020,
                "end": 2021
            }
        ],
        "trophies": [
            "Premier League x5",
            "UEFA Champions League 2008",
            "FA Cup 2016"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Filippo Inzaghi",
        "nationality": "Italy",
        "position": "ST",
        "position_group": "Forward",
        "birth_year": 1973,
        "current_club": "Retired",
        "career": [
            {
                "club": "Piacenza",
                "league": "Serie A",
                "years": "1991-95",
                "start": 1991,
                "end": 1995
            },
            {
                "club": "Parma",
                "league": "Serie A",
                "years": "1995-96",
                "start": 1995,
                "end": 1996
            },
            {
                "club": "Atalanta",
                "league": "Serie A",
                "years": "1996-97",
                "start": 1996,
                "end": 1997
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "1997-01",
                "start": 1997,
                "end": 2001
            },
            {
                "club": "AC Milan",
                "league": "Serie A",
                "years": "2001-12",
                "start": 2001,
                "end": 2012
            }
        ],
        "trophies": [
            "UEFA Champions League x2",
            "Serie A x4",
            "FIFA World Cup 2006"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Andres Iniesta",
        "nationality": "Spain",
        "position": "CM/CAM",
        "position_group": "Midfielder",
        "birth_year": 1984,
        "current_club": "Retired",
        "career": [
            {
                "club": "Barcelona B",
                "league": "Segunda Division B",
                "years": "2001-02",
                "start": 2001,
                "end": 2002
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2002-18",
                "start": 2002,
                "end": 2018
            },
            {
                "club": "Vissel Kobe",
                "league": "J-League",
                "years": "2018-23",
                "start": 2018,
                "end": 2023
            }
        ],
        "trophies": [
            "FIFA World Cup 2010",
            "UEFA Euro x2",
            "UEFA Champions League x4",
            "La Liga x9"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Xavi Hernandez",
        "nationality": "Spain",
        "position": "CM",
        "position_group": "Midfielder",
        "birth_year": 1980,
        "current_club": "Retired",
        "career": [
            {
                "club": "Barcelona B",
                "league": "Segunda Division B",
                "years": "1997-98",
                "start": 1997,
                "end": 1998
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "1998-15",
                "start": 1998,
                "end": 2015
            },
            {
                "club": "Al-Sadd",
                "league": "Qatar Stars League",
                "years": "2015-19",
                "start": 2015,
                "end": 2019
            }
        ],
        "trophies": [
            "FIFA World Cup 2010",
            "UEFA Euro x2",
            "UEFA Champions League x4",
            "La Liga x8"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Kevin De Bruyne",
        "nationality": "Belgium",
        "position": "CM/CAM",
        "position_group": "Midfielder",
        "birth_year": 1991,
        "current_club": "Manchester City",
        "career": [
            {
                "club": "Genk",
                "league": "Belgian First Division A",
                "years": "2008-12",
                "start": 2008,
                "end": 2012
            },
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "2012-14",
                "start": 2012,
                "end": 2014
            },
            {
                "club": "Werder Bremen (loan)",
                "league": "Bundesliga",
                "years": "2012-13",
                "start": 2012,
                "end": 2013
            },
            {
                "club": "VfL Wolfsburg",
                "league": "Bundesliga",
                "years": "2014-15",
                "start": 2014,
                "end": 2015
            },
            {
                "club": "Manchester City",
                "league": "Premier League",
                "years": "2015-",
                "start": 2015,
                "end": None
            }
        ],
        "trophies": [
            "Premier League x6",
            "UEFA Champions League 2023",
            "FA Cup 2023"
        ],
        "ballon_dor": 0,
        "difficulty": "Easy"
    },
    {
        "name": "Luka Modric",
        "nationality": "Croatia",
        "position": "CM",
        "position_group": "Midfielder",
        "birth_year": 1985,
        "current_club": "Real Madrid",
        "career": [
            {
                "club": "Dinamo Zagreb",
                "league": "Croatian Football League",
                "years": "2003-08",
                "start": 2003,
                "end": 2008
            },
            {
                "club": "Tottenham Hotspur",
                "league": "Premier League",
                "years": "2008-12",
                "start": 2008,
                "end": 2012
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2012-",
                "start": 2012,
                "end": None
            }
        ],
        "trophies": [
            "UEFA Champions League x5",
            "La Liga x4",
            "Ballon d'Or 2018"
        ],
        "ballon_dor": 1,
        "difficulty": "Medium"
    },
    {
        "name": "Zinedine Zidane",
        "nationality": "France",
        "position": "CAM/CM",
        "position_group": "Midfielder",
        "birth_year": 1972,
        "current_club": "Retired",
        "career": [
            {
                "club": "Cannes",
                "league": "Ligue 1",
                "years": "1989-92",
                "start": 1989,
                "end": 1992
            },
            {
                "club": "Bordeaux",
                "league": "Ligue 1",
                "years": "1992-96",
                "start": 1992,
                "end": 1996
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "1996-01",
                "start": 1996,
                "end": 2001
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2001-06",
                "start": 2001,
                "end": 2006
            }
        ],
        "trophies": [
            "FIFA World Cup 1998",
            "UEFA Euro 2000",
            "Serie A x2",
            "La Liga 2003",
            "UEFA Champions League 2002"
        ],
        "ballon_dor": 1,
        "difficulty": "Hard"
    },
    {
        "name": "Steven Gerrard",
        "nationality": "England",
        "position": "CM",
        "position_group": "Midfielder",
        "birth_year": 1980,
        "current_club": "Retired",
        "career": [
            {
                "club": "Liverpool",
                "league": "Premier League",
                "years": "1998-15",
                "start": 1998,
                "end": 2015
            },
            {
                "club": "LA Galaxy",
                "league": "MLS",
                "years": "2015-16",
                "start": 2015,
                "end": 2016
            }
        ],
        "trophies": [
            "UEFA Champions League 2005",
            "FA Cup x2",
            "UEFA Cup 2001"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Frank Lampard",
        "nationality": "England",
        "position": "CM",
        "position_group": "Midfielder",
        "birth_year": 1978,
        "current_club": "Retired",
        "career": [
            {
                "club": "West Ham United",
                "league": "Premier League",
                "years": "1995-01",
                "start": 1995,
                "end": 2001
            },
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "2001-14",
                "start": 2001,
                "end": 2014
            },
            {
                "club": "Manchester City",
                "league": "Premier League",
                "years": "2014-15",
                "start": 2014,
                "end": 2015
            },
            {
                "club": "New York City FC",
                "league": "MLS",
                "years": "2015-16",
                "start": 2015,
                "end": 2016
            }
        ],
        "trophies": [
            "Premier League x3",
            "FA Cup x4",
            "UEFA Champions League 2012"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Paul Pogba",
        "nationality": "France",
        "position": "CM",
        "position_group": "Midfielder",
        "birth_year": 1993,
        "current_club": "Juventus",
        "career": [
            {
                "club": "Le Havre",
                "league": "Ligue 2",
                "years": "2007-09",
                "start": 2007,
                "end": 2009
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "2009-12",
                "start": 2009,
                "end": 2012
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2012-16",
                "start": 2012,
                "end": 2016
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "2016-22",
                "start": 2016,
                "end": 2022
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2022-24",
                "start": 2022,
                "end": 2024
            }
        ],
        "trophies": [
            "FIFA World Cup 2018",
            "Serie A x4",
            "Europa League 2017",
            "FA Cup 2016"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "N'Golo Kante",
        "nationality": "France",
        "position": "CDM/CM",
        "position_group": "Midfielder",
        "birth_year": 1991,
        "current_club": "Al-Ittihad",
        "career": [
            {
                "club": "Boulogne",
                "league": "Championnat National",
                "years": "2011-13",
                "start": 2011,
                "end": 2013
            },
            {
                "club": "Caen",
                "league": "Ligue 2",
                "years": "2013-15",
                "start": 2013,
                "end": 2015
            },
            {
                "club": "Leicester City",
                "league": "Premier League",
                "years": "2015-16",
                "start": 2015,
                "end": 2016
            },
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "2016-23",
                "start": 2016,
                "end": 2023
            },
            {
                "club": "Al-Ittihad",
                "league": "Saudi Pro League",
                "years": "2023-",
                "start": 2023,
                "end": None
            }
        ],
        "trophies": [
            "FIFA World Cup 2018",
            "Premier League x2",
            "UEFA Champions League 2021",
            "FA Cup 2018"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Frenkie de Jong",
        "nationality": "Netherlands",
        "position": "CM/CDM",
        "position_group": "Midfielder",
        "birth_year": 1997,
        "current_club": "Barcelona",
        "career": [
            {
                "club": "Ajax",
                "league": "Eredivisie",
                "years": "2015-19",
                "start": 2015,
                "end": 2019
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2019-",
                "start": 2019,
                "end": None
            }
        ],
        "trophies": [
            "Eredivisie x3",
            "Copa del Rey 2021"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Patrick Vieira",
        "nationality": "France",
        "position": "CM/CDM",
        "position_group": "Midfielder",
        "birth_year": 1976,
        "current_club": "Retired",
        "career": [
            {
                "club": "Cannes",
                "league": "Ligue 2",
                "years": "1993-95",
                "start": 1993,
                "end": 1995
            },
            {
                "club": "AC Milan",
                "league": "Serie A",
                "years": "1995-96",
                "start": 1995,
                "end": 1996
            },
            {
                "club": "Arsenal",
                "league": "Premier League",
                "years": "1996-05",
                "start": 1996,
                "end": 2005
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2005-06",
                "start": 2005,
                "end": 2006
            },
            {
                "club": "Inter Milan",
                "league": "Serie A",
                "years": "2006-10",
                "start": 2006,
                "end": 2010
            },
            {
                "club": "Manchester City",
                "league": "Premier League",
                "years": "2010-11",
                "start": 2010,
                "end": 2011
            },
            {
                "club": "New York Red Bulls",
                "league": "MLS",
                "years": "2010-11",
                "start": 2010,
                "end": 2011
            }
        ],
        "trophies": [
            "FIFA World Cup 1998",
            "UEFA Euro 2000",
            "Premier League x3",
            "FA Cup x4"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Toni Kroos",
        "nationality": "Germany",
        "position": "CM",
        "position_group": "Midfielder",
        "birth_year": 1990,
        "current_club": "Retired",
        "career": [
            {
                "club": "Bayern Munich",
                "league": "Bundesliga",
                "years": "2007-14",
                "start": 2007,
                "end": 2014
            },
            {
                "club": "Bayer Leverkusen (loan)",
                "league": "Bundesliga",
                "years": "2009-10",
                "start": 2009,
                "end": 2010
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2014-24",
                "start": 2014,
                "end": 2024
            }
        ],
        "trophies": [
            "FIFA World Cup 2014",
            "UEFA Champions League x5",
            "Bundesliga x3",
            "La Liga x4"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Mesut Ozil",
        "nationality": "Germany",
        "position": "CAM",
        "position_group": "Midfielder",
        "birth_year": 1988,
        "current_club": "Retired",
        "career": [
            {
                "club": "Schalke 04",
                "league": "Bundesliga",
                "years": "2006-08",
                "start": 2006,
                "end": 2008
            },
            {
                "club": "Werder Bremen",
                "league": "Bundesliga",
                "years": "2008-10",
                "start": 2008,
                "end": 2010
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2010-13",
                "start": 2010,
                "end": 2013
            },
            {
                "club": "Arsenal",
                "league": "Premier League",
                "years": "2013-21",
                "start": 2013,
                "end": 2021
            },
            {
                "club": "Fenerbahce",
                "league": "Super Lig",
                "years": "2021-22",
                "start": 2021,
                "end": 2022
            }
        ],
        "trophies": [
            "FIFA World Cup 2014",
            "La Liga 2012",
            "FA Cup 2020"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Andrea Pirlo",
        "nationality": "Italy",
        "position": "CDM/CM",
        "position_group": "Midfielder",
        "birth_year": 1979,
        "current_club": "Retired",
        "career": [
            {
                "club": "Brescia",
                "league": "Serie A",
                "years": "1995-01",
                "start": 1995,
                "end": 2001
            },
            {
                "club": "Internazionale",
                "league": "Serie A",
                "years": "2001-01",
                "start": 2001,
                "end": 2001
            },
            {
                "club": "AC Milan",
                "league": "Serie A",
                "years": "2001-11",
                "start": 2001,
                "end": 2011
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2011-15",
                "start": 2011,
                "end": 2015
            },
            {
                "club": "New York City FC",
                "league": "MLS",
                "years": "2015-17",
                "start": 2015,
                "end": 2017
            }
        ],
        "trophies": [
            "FIFA World Cup 2006",
            "UEFA Champions League x2",
            "Serie A x6"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Virgil van Dijk",
        "nationality": "Netherlands",
        "position": "CB",
        "position_group": "Defender",
        "birth_year": 1991,
        "current_club": "Liverpool",
        "career": [
            {
                "club": "Groningen",
                "league": "Eredivisie",
                "years": "2010-13",
                "start": 2010,
                "end": 2013
            },
            {
                "club": "Celtic",
                "league": "Scottish Premiership",
                "years": "2013-15",
                "start": 2013,
                "end": 2015
            },
            {
                "club": "Southampton",
                "league": "Premier League",
                "years": "2015-18",
                "start": 2015,
                "end": 2018
            },
            {
                "club": "Liverpool",
                "league": "Premier League",
                "years": "2018-",
                "start": 2018,
                "end": None
            }
        ],
        "trophies": [
            "Premier League 2020",
            "UEFA Champions League 2019",
            "FA Cup 2022"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Sergio Ramos",
        "nationality": "Spain",
        "position": "CB",
        "position_group": "Defender",
        "birth_year": 1986,
        "current_club": "Sevilla",
        "career": [
            {
                "club": "Sevilla",
                "league": "La Liga",
                "years": "2003-05",
                "start": 2003,
                "end": 2005
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2005-21",
                "start": 2005,
                "end": 2021
            },
            {
                "club": "Paris Saint-Germain",
                "league": "Ligue 1",
                "years": "2021-23",
                "start": 2021,
                "end": 2023
            },
            {
                "club": "Sevilla",
                "league": "La Liga",
                "years": "2023-",
                "start": 2023,
                "end": None
            }
        ],
        "trophies": [
            "FIFA World Cup 2010",
            "UEFA Euro x2",
            "UEFA Champions League x4",
            "La Liga x5"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "John Terry",
        "nationality": "England",
        "position": "CB",
        "position_group": "Defender",
        "birth_year": 1980,
        "current_club": "Retired",
        "career": [
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "1998-17",
                "start": 1998,
                "end": 2017
            },
            {
                "club": "Nottingham Forest",
                "league": "Championship",
                "years": "2017-18",
                "start": 2017,
                "end": 2018
            },
            {
                "club": "Aston Villa",
                "league": "Championship",
                "years": "2018",
                "start": 2018,
                "end": 2018
            }
        ],
        "trophies": [
            "Premier League x5",
            "FA Cup x5",
            "UEFA Champions League 2012"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Rio Ferdinand",
        "nationality": "England",
        "position": "CB",
        "position_group": "Defender",
        "birth_year": 1978,
        "current_club": "Retired",
        "career": [
            {
                "club": "West Ham United",
                "league": "Premier League",
                "years": "1995-00",
                "start": 1995,
                "end": 2000
            },
            {
                "club": "Bournemouth (loan)",
                "league": "Third Division",
                "years": "1996-97",
                "start": 1996,
                "end": 1997
            },
            {
                "club": "Leeds United",
                "league": "Premier League",
                "years": "2000-02",
                "start": 2000,
                "end": 2002
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "2002-14",
                "start": 2002,
                "end": 2014
            },
            {
                "club": "Queens Park Rangers",
                "league": "Championship",
                "years": "2014-15",
                "start": 2014,
                "end": 2015
            }
        ],
        "trophies": [
            "Premier League x6",
            "FA Cup 2004",
            "UEFA Champions League 2008"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Carles Puyol",
        "nationality": "Spain",
        "position": "CB",
        "position_group": "Defender",
        "birth_year": 1978,
        "current_club": "Retired",
        "career": [
            {
                "club": "Barcelona B",
                "league": "Segunda Division B",
                "years": "1995-99",
                "start": 1995,
                "end": 1999
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "1999-14",
                "start": 1999,
                "end": 2014
            }
        ],
        "trophies": [
            "FIFA World Cup 2010",
            "UEFA Euro x2",
            "UEFA Champions League x2",
            "La Liga x6"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Trent Alexander-Arnold",
        "nationality": "England",
        "position": "RB",
        "position_group": "Defender",
        "birth_year": 1998,
        "current_club": "Liverpool",
        "career": [
            {
                "club": "Liverpool",
                "league": "Premier League",
                "years": "2016-",
                "start": 2016,
                "end": None
            }
        ],
        "trophies": [
            "Premier League 2020",
            "UEFA Champions League 2019",
            "FA Cup 2022"
        ],
        "ballon_dor": 0,
        "difficulty": "Easy"
    },
    {
        "name": "Dani Alves",
        "nationality": "Brazil",
        "position": "RB",
        "position_group": "Defender",
        "birth_year": 1983,
        "current_club": "Retired",
        "career": [
            {
                "club": "Bahia",
                "league": "Brasileirao",
                "years": "2001-02",
                "start": 2001,
                "end": 2002
            },
            {
                "club": "Sevilla",
                "league": "La Liga",
                "years": "2002-08",
                "start": 2002,
                "end": 2008
            },
            {
                "club": "Barcelona",
                "league": "La Liga",
                "years": "2008-16",
                "start": 2008,
                "end": 2016
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2016-17",
                "start": 2016,
                "end": 2017
            },
            {
                "club": "Paris Saint-Germain",
                "league": "Ligue 1",
                "years": "2017-18",
                "start": 2017,
                "end": 2018
            },
            {
                "club": "Manchester City",
                "league": "Premier League",
                "years": "2017-18",
                "start": 2017,
                "end": 2018
            },
            {
                "club": "Sao Paulo",
                "league": "Brasileirao",
                "years": "2019-22",
                "start": 2019,
                "end": 2022
            }
        ],
        "trophies": [
            "Copa America x2",
            "UEFA Champions League x3",
            "La Liga x6"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Paolo Maldini",
        "nationality": "Italy",
        "position": "LB/CB",
        "position_group": "Defender",
        "birth_year": 1968,
        "current_club": "Retired",
        "career": [
            {
                "club": "AC Milan",
                "league": "Serie A",
                "years": "1985-09",
                "start": 1985,
                "end": 2009
            }
        ],
        "trophies": [
            "Serie A x7",
            "UEFA Champions League x5",
            "Intercontinental Cup x2"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Roberto Carlos",
        "nationality": "Brazil",
        "position": "LB",
        "position_group": "Defender",
        "birth_year": 1973,
        "current_club": "Retired",
        "career": [
            {
                "club": "Palmeiras",
                "league": "Brasileirao",
                "years": "1993-95",
                "start": 1993,
                "end": 1995
            },
            {
                "club": "Inter Milan",
                "league": "Serie A",
                "years": "1995-96",
                "start": 1995,
                "end": 1996
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "1996-07",
                "start": 1996,
                "end": 2007
            },
            {
                "club": "Fenerbahce",
                "league": "Super Lig",
                "years": "2007-09",
                "start": 2007,
                "end": 2009
            },
            {
                "club": "Corinthians",
                "league": "Brasileirao",
                "years": "2009-11",
                "start": 2009,
                "end": 2011
            },
            {
                "club": "Anzhi Makhachkala",
                "league": "Russian Premier League",
                "years": "2011-12",
                "start": 2011,
                "end": 2012
            }
        ],
        "trophies": [
            "FIFA World Cup 1994 & 2002",
            "UEFA Champions League x3",
            "La Liga x4"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Raphael Varane",
        "nationality": "France",
        "position": "CB",
        "position_group": "Defender",
        "birth_year": 1993,
        "current_club": "Como",
        "career": [
            {
                "club": "Lens",
                "league": "Ligue 2",
                "years": "2010-11",
                "start": 2010,
                "end": 2011
            },
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "2011-21",
                "start": 2011,
                "end": 2021
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "2021-23",
                "start": 2021,
                "end": 2023
            },
            {
                "club": "Como",
                "league": "Serie A",
                "years": "2024-",
                "start": 2024,
                "end": None
            }
        ],
        "trophies": [
            "FIFA World Cup 2018",
            "UEFA Champions League x4",
            "La Liga x3"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Ashley Cole",
        "nationality": "England",
        "position": "LB",
        "position_group": "Defender",
        "birth_year": 1980,
        "current_club": "Retired",
        "career": [
            {
                "club": "Arsenal",
                "league": "Premier League",
                "years": "1999-06",
                "start": 1999,
                "end": 2006
            },
            {
                "club": "Crystal Palace (loan)",
                "league": "Second Division",
                "years": "2000",
                "start": 2000,
                "end": 2000
            },
            {
                "club": "Chelsea",
                "league": "Premier League",
                "years": "2006-14",
                "start": 2006,
                "end": 2014
            },
            {
                "club": "Roma",
                "league": "Serie A",
                "years": "2014-16",
                "start": 2014,
                "end": 2016
            },
            {
                "club": "LA Galaxy",
                "league": "MLS",
                "years": "2016-17",
                "start": 2016,
                "end": 2017
            }
        ],
        "trophies": [
            "Premier League x3",
            "FA Cup x7",
            "UEFA Champions League 2012"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Manuel Neuer",
        "nationality": "Germany",
        "position": "GK",
        "position_group": "Goalkeeper",
        "birth_year": 1986,
        "current_club": "Bayern Munich",
        "career": [
            {
                "club": "Schalke 04",
                "league": "Bundesliga",
                "years": "2005-11",
                "start": 2005,
                "end": 2011
            },
            {
                "club": "Bayern Munich",
                "league": "Bundesliga",
                "years": "2011-",
                "start": 2011,
                "end": None
            }
        ],
        "trophies": [
            "FIFA World Cup 2014",
            "UEFA Champions League 2013 & 2020",
            "Bundesliga x11"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Gianluigi Buffon",
        "nationality": "Italy",
        "position": "GK",
        "position_group": "Goalkeeper",
        "birth_year": 1978,
        "current_club": "Retired",
        "career": [
            {
                "club": "Parma",
                "league": "Serie A",
                "years": "1995-01",
                "start": 1995,
                "end": 2001
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2001-18",
                "start": 2001,
                "end": 2018
            },
            {
                "club": "Paris Saint-Germain",
                "league": "Ligue 1",
                "years": "2018-19",
                "start": 2018,
                "end": 2019
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2019-21",
                "start": 2019,
                "end": 2021
            },
            {
                "club": "Parma",
                "league": "Serie B",
                "years": "2021-23",
                "start": 2021,
                "end": 2023
            }
        ],
        "trophies": [
            "FIFA World Cup 2006",
            "Serie A x10",
            "Coppa Italia x6"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Peter Schmeichel",
        "nationality": "Denmark",
        "position": "GK",
        "position_group": "Goalkeeper",
        "birth_year": 1963,
        "current_club": "Retired",
        "career": [
            {
                "club": "Brondby IF",
                "league": "Danish Superliga",
                "years": "1987-91",
                "start": 1987,
                "end": 1991
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "1991-99",
                "start": 1991,
                "end": 1999
            },
            {
                "club": "Sporting CP",
                "league": "Primeira Liga",
                "years": "1999-01",
                "start": 1999,
                "end": 2001
            },
            {
                "club": "Aston Villa",
                "league": "Premier League",
                "years": "2001-02",
                "start": 2001,
                "end": 2002
            },
            {
                "club": "Manchester City",
                "league": "Premier League",
                "years": "2002-03",
                "start": 2002,
                "end": 2003
            }
        ],
        "trophies": [
            "Premier League x5",
            "FA Cup x3",
            "UEFA Champions League 1999"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    },
    {
        "name": "Alisson Becker",
        "nationality": "Brazil",
        "position": "GK",
        "position_group": "Goalkeeper",
        "birth_year": 1992,
        "current_club": "Liverpool",
        "career": [
            {
                "club": "Internacional",
                "league": "Brasileirao",
                "years": "2012-16",
                "start": 2012,
                "end": 2016
            },
            {
                "club": "Roma",
                "league": "Serie A",
                "years": "2016-18",
                "start": 2016,
                "end": 2018
            },
            {
                "club": "Liverpool",
                "league": "Premier League",
                "years": "2018-",
                "start": 2018,
                "end": None
            }
        ],
        "trophies": [
            "Premier League 2020",
            "UEFA Champions League 2019",
            "Copa America 2019"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Iker Casillas",
        "nationality": "Spain",
        "position": "GK",
        "position_group": "Goalkeeper",
        "birth_year": 1981,
        "current_club": "Retired",
        "career": [
            {
                "club": "Real Madrid",
                "league": "La Liga",
                "years": "1999-15",
                "start": 1999,
                "end": 2015
            },
            {
                "club": "Porto",
                "league": "Primeira Liga",
                "years": "2015-19",
                "start": 2015,
                "end": 2019
            }
        ],
        "trophies": [
            "FIFA World Cup 2010",
            "UEFA Euro x2",
            "UEFA Champions League x3",
            "La Liga x5"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "David de Gea",
        "nationality": "Spain",
        "position": "GK",
        "position_group": "Goalkeeper",
        "birth_year": 1990,
        "current_club": "Juventus",
        "career": [
            {
                "club": "Atletico Madrid",
                "league": "La Liga",
                "years": "2009-11",
                "start": 2009,
                "end": 2011
            },
            {
                "club": "Manchester United",
                "league": "Premier League",
                "years": "2011-23",
                "start": 2011,
                "end": 2023
            },
            {
                "club": "Juventus",
                "league": "Serie A",
                "years": "2024-",
                "start": 2024,
                "end": None
            }
        ],
        "trophies": [
            "Premier League 2013",
            "FA Cup 2016",
            "Europa League 2017",
            "League Cup x5"
        ],
        "ballon_dor": 0,
        "difficulty": "Medium"
    },
    {
        "name": "Oliver Kahn",
        "nationality": "Germany",
        "position": "GK",
        "position_group": "Goalkeeper",
        "birth_year": 1969,
        "current_club": "Retired",
        "career": [
            {
                "club": "Karlsruher SC",
                "league": "Bundesliga",
                "years": "1987-94",
                "start": 1987,
                "end": 1994
            },
            {
                "club": "Bayern Munich",
                "league": "Bundesliga",
                "years": "1994-08",
                "start": 1994,
                "end": 2008
            }
        ],
        "trophies": [
            "Bundesliga x8",
            "UEFA Champions League 2001",
            "UEFA Cup 1996"
        ],
        "ballon_dor": 0,
        "difficulty": "Hard"
    }
]


# ---------------------------------------------------------------------------
# Game-logic helpers
# ---------------------------------------------------------------------------

def get_top_league(player: dict) -> str:
    top_leagues = ["Premier League","La Liga","Serie A","Bundesliga","Ligue 1",
                   "Eredivisie","Primeira Liga","MLS","Saudi Pro League"]
    league_years: dict = {}
    for e in player["career"]:
        lg = e["league"]
        duration = (e["end"] or 2025) - e["start"]
        league_years[lg] = league_years.get(lg, 0) + duration
    for lg in top_leagues:
        if lg in league_years:
            return lg
    if league_years:
        return max(league_years, key=lambda k: league_years[k])
    return "Other"


def filter_players(
    position_group: str = "All Positions",
    league_filter: str = "All Leagues",
    era_filter: str = "All Eras",
    difficulty: str = "All",
) -> list:
    era_start, era_end = ERAS.get(era_filter, (1900, 2100))
    results = []
    for p in PLAYERS:
        if position_group != "All Positions" and p["position_group"] != position_group:
            continue
        if league_filter != "All Leagues":
            leagues_in = [e["league"] for e in p["career"]]
            if league_filter not in leagues_in:
                continue
        career_start = min(e["start"] for e in p["career"])
        career_end   = max((e["end"] or 2025) for e in p["career"])
        if career_end < era_start or career_start > era_end:
            continue
        if difficulty != "All" and p.get("difficulty") != difficulty:
            continue
        results.append(p)
    return results


def pick_random_player(filtered: list) -> dict:
    if not filtered:
        return None
    return random.choice(filtered)


def score_for_guess(clubs_revealed: int, total_clubs: int) -> int:
    if total_clubs == 0:
        return 0
    frac = clubs_revealed / total_clubs
    if frac <= 0.25:   return 1000
    elif frac <= 0.50: return 700
    elif frac <= 0.75: return 400
    else:              return 200


def all_player_names() -> list:
    return sorted(p["name"] for p in PLAYERS)


def _age_bucket(birth_year: int) -> str:
    age = 2025 - birth_year
    if age < 23:   return "Under 23"
    elif age < 28: return "23-27"
    elif age < 33: return "28-32"
    elif age < 38: return "33-37"
    else:          return "38+"


def compare_players(guess: dict, target: dict) -> dict:
    result = {}
    result["nationality"] = (
        "correct" if guess["nationality"] == target["nationality"] else "wrong"
    )
    result["position_group"] = (
        "correct" if guess["position_group"] == target["position_group"] else "wrong"
    )
    guess_lg  = get_top_league(guess)
    target_lg = get_top_league(target)
    result["league"] = "correct" if guess_lg == target_lg else "wrong"
    guess_age  = _age_bucket(guess["birth_year"])
    target_age = _age_bucket(target["birth_year"])
    if guess_age == target_age:
        result["age"] = "correct"
    else:
        result["age"] = (
            "close" if abs(guess["birth_year"] - target["birth_year"]) <= 6
            else "wrong"
        )
    result["current_club"] = (
        "correct" if guess.get("current_club") == target.get("current_club")
        else "wrong"
    )
    guess_bd  = (guess.get("ballon_dor", 0) or 0) > 0
    target_bd = (target.get("ballon_dor", 0) or 0) > 0
    result["ballon_dor_winner"] = "correct" if guess_bd == target_bd else "wrong"
    return result
