from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import teamdashboardbygeneralsplits
import pandas as pd

# Player ID 2544 is Lebron

# Stats:
# Win Percentage
# FG Percentage
# 3PT Percentage
# FT Percentage
# Rebounds
# Assists
# turnovers
# Steals
# Blocks
# Plus minus --> point differential
# Offensive rating
# Defensive Rating
# True shooting percentage

# Other factors
# Number of possessions (pace)
# PVP stats
# Injury --> Player value to the team



team = teams.find_team_by_abbreviation(abbreviation="LAL")
print(teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=team["id"]).get_data_frames())