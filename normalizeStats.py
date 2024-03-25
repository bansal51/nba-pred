# normalizeStats.py - Get a normalized mean, standard deviation, and z-score based on the rest of the league

from nba_api.stats.endpoints import leaguedashteamstats
from getStatsPerTeam import getStatsForTeam
import statistics

# Finds the league mean for the basic or advanced stat (statType = 'Base'/'Advanced')
def normalizedMeanForStatistic(season, stat, statType='Base'):
    # Get dictionaries with stats for every team
    completeTeamInfo = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions', measure_type_detailed_defense=statType, season=season)
    completeTeamDict = completeTeamInfo.get_normalized_dict()
    completeTeamList = completeTeamDict['LeagueDashTeamStats']

    # Get the specified stat for all teams and place it in a list
    specifiedStatAllTeams = []
    for i in range(len(completeTeamList)):
        specifiedStatAllTeams.append(completeTeamList[i][stat])

    # Calculate the mean of specified stats over the whole league
    mean = statistics.mean(specifiedStatAllTeams)
    return mean


# Finds the standard deviation for the basic or advanced stat (statType = 'Base'/'Advanced')
def normalizedStdDevForStatistic(season, stat, statType='Base'):
    # Get dictionaries with stats for every team
    completeTeamInfo = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions', measure_type_detailed_defense=statType, season=season)
    completeTeamDict = completeTeamInfo.get_normalized_dict()
    completeTeamList = completeTeamDict['LeagueDashTeamStats']

    # Get the specified stat for all teams and place it in a list
    specifiedStatAllTeams = []
    for i in range(len(completeTeamList)):
        specifiedStatAllTeams.append(completeTeamList[i][stat])

    # Calculate the standard deviation of specified stat over the whole league
    stddev = statistics.stdev(specifiedStatAllTeams)
    return stddev

# Calculate the Z-score based on the mean and stdev
# The z-score is important because it allows us to gauge the probability of a score happening within the normal distribution
def calculateZScore(stat, mean, stdev):
    # Positive means that the stat is higher than the average, negative means that the stat is lower
    return (stat - mean)/stdev