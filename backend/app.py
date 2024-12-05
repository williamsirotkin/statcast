from flask import Flask
import pandas

app = Flask(__name__)

battedBallData = pandas.read_excel('../BattedBallData.xlsx')



@app.route('/')
def hello():
    return 'Welcome to Statcast!'

@app.route('/getDataForHitter/<hitter_id>')
def getDataForHitter(hitter_id):
    returnData = {}
    returnData[hitter_id] = []
    for data in battedBallData.iterrows():
        data = data[1]
        if data['BATTER_ID'] == int(hitter_id):
            returnData[hitter_id].append(data.to_dict())
    return returnData

@app.route('/getDataForPitcher/<pitcher_id>')
def getDataForPitcher(pitcher_id):
    returnData = {}
    returnData[pitcher_id] = []
    for data in battedBallData.iterrows():
        data = data[1]
        if data['PITCHER_ID'] == int(pitcher_id):
            returnData[pitcher_id].append(data.to_dict())
    return returnData


    


if __name__ == '__main__':
    app.run(debug=True)