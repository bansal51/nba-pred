# teams.py - Function that allows to get the list of all teams and ids associated

def getTeamDict(input):
    teams = {}
    for entry in input:
        teams[entry["full_name"]] = entry["id"]
    return teams
