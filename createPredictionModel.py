# createPredictionModel.py - Used to train, test, validate, and create the model

from normalizeStats import normalizedMeanForStatistic, normalizedStdDevForStatistic, calculateZScore
from nba_api.stats.static import teams
from getGames import pastMatches
from getStatsPerTeam import getStatsForTeam
from availableStats import availableStats
from teams import teams

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from datetime import timedelta, date
import pandas as pd
import pickle

# Calculate the z-score differential between two teams for a specified statistic
def zScoreDiff(observedStatHome, observedStatAway, mean, stdev):
    homeZScore = calculateZScore(observedStatHome, mean, stdev)
    awayZScore = calculateZScore(observedStatAway, mean, stdev)

    difference = homeZScore - awayZScore
    return difference


# Helper function that allows iterating through a start date to the end date
def dateRange(startDate, endDate):
    for i in range(int((endDate - startDate).days)):
        yield startDate + timedelta(i)


# Create mean and standard deviations dicts 
# Returns a list where index 0 is a dict holding the mean for each stat, index 1 is a dict holding the stdev for each stat
def getMeanAndStDevDicts(startDate, endDate, season):
    meanDict = {}
    stDevDict = {}

    # Loops through the available stats and inputs the mean and stdev for each stat
    for stat, statType in availableStats.items():
        statMean = normalizedMeanForStatistic(startDate, endDate, season, stat, statType)
        meanDict.update({stat: statMean})

        statSD = normalizedStdDevForStatistic(startDate, endDate, season, stat, statType)
        stDevDict.update({stat: statSD})
    
    bothDicts = []
    bothDicts.append(meanDict)
    bothDicts.append(stDevDict)

    return bothDicts


# Insert all the data into a dataframe
# dailyGames is a list where index 0 is a dict holding the matchups and index 1 is a list holding the result
def infoToDF(dailyGames, meanDict, stDevDict, startDate, endDate, season):
    df = pd.DataFrame(columns=['Home', 'Away', 'W_PCT', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'BLK', 'STL', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT', 'Result', 'Date'])
    gameNumber = 0
    dailyResults = dailyGames[1]

    for homeTeam, awayTeam in dailyGames[0].items():
        homeStats = getStatsForTeam(homeTeam, startDate, endDate, season)
        awayStats = getStatsForTeam(awayTeam, startDate, endDate, season)

        currentGame = [homeTeam, awayTeam]

        for stat, statType in availableStats.items():
            zScore = zScoreDiff(homeStats[stat], awayStats[stat], meanDict[stat], stDevDict[stat])
            currentGame.append(zScore)

        if dailyResults[gameNumber] == 'W':
            result = 1
        else:
            result = 0
        
        currentGame.append(result)
        currentGame.append(endDate)
        gameNumber += 1

        df.loc[len(df)] = currentGame

    return df

# Loops through every date between start and end dates and appends each game to a singular dataframe to be returned
def createTrainingSet(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startOfSeason):
    startDate = date(startYear, startMonth, startDay)
    endDate = date(endYear, endMonth, endDay)

    allGames = pd.DataFrame(columns=['Home', 'Away', 'W_PCT', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'BLK', 'STL', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT', 'Result', 'Date'])
    startDateFormatted = startDate.strftime("%m/%d/%Y")

    for singleDate in dateRange(startDate, endDate):
        currentDate = singleDate.strftime("%m/%d/%Y")

        previousDay = singleDate - timedelta(days=1)
        previousDayFormatted = previousDay.strftime("%m/%d/%Y")
        
        meanAndStDevDict = getMeanAndStDevDicts(startOfSeason, previousDayFormatted, season)
        meanDict = meanAndStDevDict[0]
        sdDict = meanAndStDevDict[1]

        currentDayGames = pastMatches(currentDate, season)
        currentDayDF = infoToDF(currentDayGames, meanDict, sdDict, startOfSeason, previousDayFormatted, season)

        allGames = pd.concat([allGames, currentDayDF], axis=0)
    
    return allGames


print(createTrainingSet(2022, 11, 5, 2022, 11, 8, "2022-23", "10/18/2022"))

# both_dict = getMeanAndStDevDicts("10/18/2022", "12/25/2022", "2022-23")
# mean_dict = both_dict[0]
# sd_dict = both_dict[1]
# print(infoToDF(pastMatches("12/25/2022", "2022-23"), mean_dict, sd_dict, "10/18/2022", "12/25/2022", "2022-23"))