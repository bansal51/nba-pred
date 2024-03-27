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


# Creates logistic regression model and tests accuracy
def performLogisticRegression(data):
    featureColumns = ['W_PCT', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'BLK', 'STL', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

    # Get the features and result of the games
    X = data[featureColumns]
    y = data.Result

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True)
    logreg = LogisticRegression()

    # Fit the model with the train data
    logreg.fit(X_train, y_train) 

    # Predict the result of the test set and compare it to the actual results
    y_pred = logreg.predict(X_test)
    confmatrix = metrics.confusion_matrix(y_test, y_pred)

    # Print out the model information, as well as accuarcy
    print('Coefficient Information:')
    for i in range(len(featureColumns)):
        logregCoefficients = logreg.coef_

        currentFeature = featureColumns[i]
        currentCoefficient = logregCoefficients[0][i]

        print(currentFeature + ": " + str(currentCoefficient))
    
    print('----------------------------------')

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Precision:", metrics.precision_score(y_test, y_pred))
    print("Recall:", metrics.recall_score(y_test, y_pred))

    print('----------------------------------')

    print('Confusion Matrix:')
    print(confmatrix)

    return logreg

# Saves the model in a folder
# filename should end in '.pkl'
def saveModel(model, filename):
    with open('C:/Users/Yash/Documents/projects/nba-app/Saved Models/' + filename, 'wb') as file:
        pickle.dump(model, file)

# Used to generate new logistic regression models
# Can import the statistics and predictions for each game from a csv file or can be created on their own
def createModel(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startOfSeason, filename):
    allGames = createTrainingSet(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startOfSeason)

    logRegModel = performLogisticRegression(allGames)

    if filename:
        saveModel(logRegModel, filename)
