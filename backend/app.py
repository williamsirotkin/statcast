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

def displayData(data):
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
    return [
        {
            "label": "Exit Velo",
            "value": exitVelo,
            "percentile": "something"
        },
        {
            "label": "AVG",
            "value": AVG,
            "percentile": "something"
        },
        {
            "label": "OPS",
            "value": OPS,
            "percentile": "something"
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
    return displayData(returnData)


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
    return displayData(returnData)

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