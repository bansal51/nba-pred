# getStatsPerTeam.py - Get a dataframe output of a teams basic and advanced stats for a season

from teams import getTeamDict
from nba_api.stats.endpoints import teamdashboardbygeneralsplits
from nba_api.stats.static import teams

teams_dict = getTeamDict(teams.get_teams())

def getStatsForTeam(team, season):
    # Use the NBA API to access a dictionary for a team's season which includes basic stats for every team per 100 possessions
    # Allows to nullify 'pace' of different teams for more standardized stats
    teamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams_dict[team], per_mode_detailed='Per100Possessions', season=season)
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
    advancedTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams_dict[team], measure_type_detailed_defense='Advanced', season=season)
    advanced_team_data = advancedTeamInfo.get_normalized_dict()['OverallTeamDashboard'][0]
    
    # Get advanced team stats
    off_rating = advanced_team_data['OFF_RATING']
    def_rating = advanced_team_data['DEF_RATING']
    true_shooting = advanced_team_data['TS_PCT']

    # Parse all the data into a single dict
    full_data = {
        'team_id': teams_dict[team],
        'w_pct': w_pct,
        'fg_pct': fg_pct,
        'fg3_pct': fg3_pct,
        'ft_pct': ft_pct,
        'rebounds': rebounds,
        'assists': assists,
        'blocks': blocks,
        'steals': steals,
        'turnovers': turnovers,
        'plus_minus': plus_minus,
        'off_rating': off_rating,
        'def_rating': def_rating,
        'true_shooting': true_shooting
    }

    return full_data