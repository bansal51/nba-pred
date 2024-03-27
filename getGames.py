# getGames.py - Get games on a day from a past season or present season

from nba_api.stats.endpoints import leaguegamelog, scoreboardv2
from teams import teams

# This functions gets all games from a past specified date
# Return value is a list: index 0 is a dict that holds the matchup and index 1 holds the result of the games
# date format: mm/dd/yyyy; season format: yyyy-yy
def pastMatches(date, season):
    # get the list of the teams and their matchups on a specific date
    matches = leaguegamelog.LeagueGameLog(season=season, league_id='00', season_type_all_star='Regular Season', date_from_nullable=date, date_to_nullable=date, timeout=120)
    matchesDict = matches.get_normalized_dict()
    matchList = matchesDict["LeagueGameLog"]
    
    # Traverse the matchlist and get the matchup and victor of the match
    # We are stepping by 2 because the match appears twice
    victorList = []
    homeAwayDict = {}
    for i in range(0, len(matchList), 2):
        # determining whether or not the team is home or away
        # @ in matchup indicates that the current team is away
        if '@' in matchList[i]["MATCHUP"]:
            awayTeam = matchList[i]["TEAM_NAME"]
            homeTeam = matchList[i + 1]["TEAM_NAME"]
            
            victorList.append(matchList[i + 1]["WL"]) # Appends if the home team won or lost
        else:
            awayTeam = matchList[i + 1]["TEAM_NAME"]
            homeTeam = matchList[i]["TEAM_NAME"]

            victorList.append(matchList[i]["WL"])
        
        homeAwayDict.update({homeTeam: awayTeam}) # Adds the current game to the list of all games for the day

    # List is setup so that the victor is whether or not the key of the dict is the winner
    matchupResults = [homeAwayDict, victorList]
    return matchupResults

# This functions gets all games the current specified date
# Return value is a dict that holds the matchup
# date format: mm/dd/yyyy; season format: yyyy-yy
def presentMatches(date):
    # get the list of the teams and their matchups on a specific date
    matches = scoreboardv2.ScoreboardV2(league_id='00', game_date=date, timeout=120)
    matchesDict = matches.get_normalized_dict()
    matchList = matchesDict["GameHeader"]

    homeAwayDict = {}
    
    # Loop through all games
    for match in matchList:
        # Get the ID of the home and away teams from the matchList
        homeTeam = ''
        awayTeam = ''
        homeTeamID = match["HOME_TEAM_ID"]
        awayTeamID = match["VISITOR_TEAM_ID"]
        
        # Loop through the team dict and find the name of the team based on the team ID
        for team, teamID in teams.items():
            if homeTeamID == teamID:
                homeTeam = team
            if awayTeamID == teamID:
                awayTeam = team
        
        # Insert the pair into the homeAway dict where the key is the home team and the value is the away team
        homeAwayDict.update({homeTeam:awayTeam})
    
    return homeAwayDict
