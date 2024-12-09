from flask import Flask, jsonify
import pandas
import string
import numpy



app = Flask(__name__)



battedBallData = pandas.read_excel('../BattedBallData.xlsx')
hitterNameMap = {}
pitcherNameMap = {}
exitVelos = []
AVGs = []
OPSs = []
exitVelosPitcher = []
AVGsPitcher = []
OPSsPitcher = []
hitterStatMap = {}
pitcherStatMap = {}

def calcPercentile(array, number):
    count = 0
    for i in range(len(array)):
        if array[i] <= number:
            count += 1
    return max(1, int((count/len(array)) * 100))

def calcStats():
    def calcAvg(arrayOfOutcomes):
        total = 0
        length = len(arrayOfOutcomes)
        for outcome in arrayOfOutcomes:
            if outcome == 'Single' or outcome == 'Double' or outcome == 'Triple' or outcome == 'Home Run':
                total += 1
            if outcome == 'Sacrifice' or outcome == 'Undefined':
                length -= 1
        if length == 0:
            return 0
        return round(total / length, 3)
        

    def calcOps(arrayOfOutcomes):
        total = 0
        length = len(arrayOfOutcomes)
        for outcome in arrayOfOutcomes:
            if outcome == 'Single':
                total +=1
            if outcome == 'Double':
                total += 2
            if outcome == 'Triple':
                total += 3
            if outcome == 'HomeRun':
                total += 4
            if outcome == 'Sacrifice' or outcome == 'Undefined':
                length -= 1
        if length == 0:
            return 0
        return round(total / length, 3)

    for data in battedBallData.iterrows():
        data = data[1]
        if data['BATTER_ID'] not in hitterStatMap:
            hitterStatMap[data['BATTER_ID']] = {
                "exitVelo": [],
                "OUTCOMES": [],
            }
        if data['PITCHER_ID'] not in pitcherStatMap:
            pitcherStatMap[data['PITCHER_ID']] = {
                "exitVelo": [],
                "OUTCOMES": [],
            }
        hitterStatMap[data['BATTER_ID']]["exitVelo"].append(data["EXIT_SPEED"])
        hitterStatMap[data['BATTER_ID']]["OUTCOMES"].append(data["PLAY_OUTCOME"])
        pitcherStatMap[data['PITCHER_ID']]["exitVelo"].append(data["EXIT_SPEED"])
        pitcherStatMap[data['PITCHER_ID']]["OUTCOMES"].append(data["PLAY_OUTCOME"])
    
    for hitter in hitterStatMap:
        exitVelos.append(sum(hitterStatMap[hitter]["exitVelo"]) / len(hitterStatMap[hitter]["exitVelo"]))
        AVGs.append(calcAvg(hitterStatMap[hitter]["OUTCOMES"]))
        OPSs.append(calcOps(hitterStatMap[hitter]["OUTCOMES"]))
    for pitcher in pitcherStatMap:
        exitVelosPitcher.append(sum(pitcherStatMap[pitcher]["exitVelo"]) / len(pitcherStatMap[pitcher]["exitVelo"]))
        AVGsPitcher.append(calcAvg(pitcherStatMap[pitcher]["OUTCOMES"]))
        OPSsPitcher.append(calcOps(pitcherStatMap[pitcher]["OUTCOMES"]))
calcStats()

        
for data in battedBallData.iterrows():
    data = data[1]
    hitter_name = data['BATTER'].lower()
    pitcher_name = data['PITCHER'].lower()
    last, first = hitter_name.split(',')
    hitter_name = first.lower() + " " + last.lower()
    last, first = pitcher_name.split(',')
    pitcher_name = first.lower() + " " + last.lower()
    hitterNameMap[hitter_name[1:]] = int(data['BATTER_ID'])
    pitcherNameMap[pitcher_name[1:]] = int(data['PITCHER_ID'])

@app.route('/')
def hello():
    return 'Welcome to Statcast!'

@app.route('/getData/playerList')
def playerList():
    players = set()

    for hitter in hitterNameMap:
        players.add(hitter)
    for pitcher in pitcherNameMap:
        players.add(pitcher)

    return list(players)

@app.route('/getData/<player_name>')
def getData(player_name):
    player_name = player_name.lower()
    if player_name in hitterNameMap:
        return jsonify(getDataForHitter(player_name))
    elif player_name in pitcherNameMap:
        return jsonify(getDataForPitcher(player_name))
    return jsonify({
            "error": "Internal server error, player not found",
        }), 500

def displayData(data, playerType):
    def isHit(outcome):
        if outcome == 'Single' or outcome == 'Double' or outcome == 'Triple' or outcome == 'Home Run':
            return 1
        return 0
    def hitValue(outcome):
        if outcome == 'Single':
            return 1
        if outcome == 'Double':
            return 3
        if outcome == 'Triple':
            return 3
        if outcome == 'Home Run':
            return 4
        return 0
    exitVelo = 0
    AVG = 0
    OPS = 0
    counter = 0
    for at_bat in data:
        counter += 1
        exitVelo += at_bat['EXIT_SPEED']
        AVG += isHit(at_bat['PLAY_OUTCOME'])
        OPS += (isHit(at_bat['PLAY_OUTCOME']) + hitValue(at_bat['PLAY_OUTCOME']))
    exitVelo = round((exitVelo / counter), 1)
    AVG = round(AVG / counter, 3)
    OPS = round(OPS / counter, 3)
    if playerType == "hitter":
        return [
            {
                "label": "Exit Velo (MPH)",
                "value": exitVelo,
                "percentile": calcPercentile(exitVelos, exitVelo)
            },
            {
                "label": "AVG",
                "value": float("%.3f" % AVG),
                "percentile": calcPercentile(AVGs, AVG)
            },
            {
                "label": "OPS",
                "value": float("%.3f" % OPS),
                "percentile": calcPercentile(OPSs, OPS)
            },
        ]
    return [
            {
                "label": "Opponent Exit Velo (MPH)",
                "value": exitVelo,
                "percentile": 100 - calcPercentile(exitVelosPitcher, exitVelo)
            },
            {
                "label": "Opponent AVG",
                "value": float("%.3f" % AVG),
                "percentile": 100 -calcPercentile(AVGsPitcher, AVG)
            },
            {
                "label": "Opponent OPS",
                "value":float("%.3f" % OPS),
                "percentile": 100 - calcPercentile(OPSsPitcher, OPS)
            },
        ]


def getDataForHitter(hitter_name):
    hitter_id = convertNameToPlayerID('hitter', hitter_name)
    if (hitter_id == -1):
        return "error - Player doesn't exist"
    returnData = []
    for data in battedBallData.iterrows():
        data = data[1]
        if data['BATTER_ID'] == int(hitter_id):
            returnData.append(data.to_dict())
    return displayData(returnData, "hitter")


def getDataForPitcher(pitcher_name):
    pitcher_id = convertNameToPlayerID('pitcher', pitcher_name)
    if (pitcher_id == -1):
        return "error - Player doesn't exist"
    returnData = {}
    returnData = []
    for data in battedBallData.iterrows():
        data = data[1]
        if data['PITCHER_ID'] == int(pitcher_id):
            returnData.append(data.to_dict())
    return displayData(returnData, "pitcher")

def convertNameToPlayerID(playerType, name):
    name = name.lower()
    if playerType == 'hitter':
        if not name in hitterNameMap:
            return -1
        return hitterNameMap[name]
    if not name in pitcherNameMap:
        return -1
    return pitcherNameMap[name]





    


if __name__ == '__main__':
    app.run(debug=True)