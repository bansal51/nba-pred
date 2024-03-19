# getStatsPerTeam.py - Get a dataframe output of a teams stats for a season

from teams import getTeamDict
from nba_api.stats.endpoints import teamdashboardbygeneralsplits
from nba_api.stats.static import teams

teams_dict = getTeamDict(teams.get_teams())

def getStatsForTeam(team, start, end, season):
    # Use the NBA API to access a dictionary for a team's season which includes basic stats for every team per 100 possessions
    # Allows to nullify 'pace' of different teams for more standardized stats
    teamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams_dict[team], per_mode_detailed='Per100Possessions', date_from_nullable=start, date_to_nullable=end, season=season)
    team_data = teamInfo.get_normalized_dict()['OverallTeamDashboard'][0]

    # Get basic team stats
    w_pct = team_data['W_PCT']
    fg_pct = team_data['FG_PCT']
    fg3_pct = team_data['FG3_PCT']
    ft_pct = team_data['FT_PCT']
    blocks = team_data['BLK']
    steals = team_data['STL']
    turnovers = team_data['TOV']
    plus_minus = team_data['PLUS_MINUS']

    # Use the NBA API to access a dictionary for a team's season which includes advanced stats for every team per 100 possessions
    advancedTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams_dict[team], measure_type_detailed_defense='Advanced', date_from_nullable=start, date_to_nullable=end, season=season)
    advanced_team_data = advancedTeamInfo.get_normalized_dict()['OverallTeamDashboard'][0]
    
    # Get advanced team stats
    off_rating = advanced_team_data['OFF_RATING']
    def_rating = advanced_team_data['DEF_RATING']
    ast_to_ratio = advanced_team_data['AST_TO']
    dreb_pct = advanced_team_data['DREB_PCT']
    oreb_pct = advanced_team_data['OREB_PCT']
    true_shooting = advanced_team_data['TS_PCT']

    # Parse all the data into a single dict
    {
        'w_pct': w_pct,
        'fg_pct': fg_pct,
        'fg3_pct': fg3_pct,
        'ft_pct': ft_pct,
        'blocks': blocks,
        'steals': steals,
        'turnovers': turnovers,
        'plus_minus': plus_minus,
        'off_rating': off_rating,
        'def_rating': def_rating,
        'ast_to_ratio': ast_to_ratio,
        'dreb_pct': dreb_pct,
        'oreb_pct': oreb_pct,
        'true_shooting': true_shooting
    }



getStatsForTeam("Milwaukee Bucks", "10/18/2022", "06/12/2023", "2022-23")