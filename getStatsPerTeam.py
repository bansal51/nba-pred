# getStatsPerTeam.py - Get a dataframe output of a teams basic and advanced stats for a season

from teams import teams
from nba_api.stats.endpoints import teamdashboardbygeneralsplits

def getStatsForTeam(team, start, end, season):
    # Use the NBA API to access a dictionary for a team's season which includes basic stats for every team per 100 possessions
    # Allows to nullify 'pace' of different teams for more standardized stats
    teamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams[team], per_mode_detailed='Per100Possessions', season=season, date_from_nullable=start, date_to_nullable=end, timeout=120)
    team_data = teamInfo.get_normalized_dict()['OverallTeamDashboard'][0]

    # Get basic team stats
    w_pct = team_data['W_PCT']
    fg_pct = team_data['FG_PCT']
    fg3_pct = team_data['FG3_PCT']
    ft_pct = team_data['FT_PCT']
    rebounds = team_data['REB']
    assists = team_data['AST']
    blocks = team_data['BLK']
    steals = team_data['STL']
    turnovers = team_data['TOV']
    plus_minus = team_data['PLUS_MINUS']

    # Use the NBA API to access a dictionary for a team's season which includes advanced stats for every team per 100 possessions
    advancedTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams[team], measure_type_detailed_defense='Advanced', season=season, date_from_nullable=start, date_to_nullable=end, timeout=120)
    advanced_team_data = advancedTeamInfo.get_normalized_dict()['OverallTeamDashboard'][0]
    
    # Get advanced team stats
    off_rating = advanced_team_data['OFF_RATING']
    def_rating = advanced_team_data['DEF_RATING']
    true_shooting = advanced_team_data['TS_PCT']

    # Parse all the data into a single dict
    full_data = {
        'TEAM_ID': teams[team],
        'W_PCT': w_pct,
        'FG_PCT': fg_pct,
        'FG3_PCT': fg3_pct,
        'FT_PCT': ft_pct,
        'REB': rebounds,
        'AST': assists,
        'BLK': blocks,
        'STL': steals,
        'TOV': turnovers,
        'PLUS_MINUS': plus_minus,
        'OFF_RATING': off_rating,
        'DEF_RATING': def_rating,
        'TS_PCT': true_shooting
    }

    return full_data