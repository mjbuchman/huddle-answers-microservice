from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import date
import json,random

app = Flask(__name__)
CORS(app)

def determineAnswer():
	dateSeed = date.today()
	random.seed(dateSeed)
	with open('./data/players.json') as json_data:
		players = json.load(json_data)
		index = random.randint(0,len(players)-1)
		return players[index]
  
def rolloverDay():
	with open('./data/todaysAnswer.json', "r") as json_data:
		todaysAnswer = json.load(json_data)
		jsonString = {"answer": determineAnswer(), "puzzleId": todaysAnswer["puzzleId"] + 1}
	with open('./data/todaysAnswer.json', "w") as json_data:
		json_data.write(json.dumps(jsonString, indent=3))
    
@app.route('/', methods=['GET', 'POST'])
def index():
	with open('./data/todaysAnswer.json') as json_data:
		todaysAnswer = json.load(json_data)
	return render_template("index.html", answer=todaysAnswer["answer"], puzzleId=todaysAnswer["puzzleId"])

@app.route('/dailyAnswer')
def answer():
	with open('./data/todaysAnswer.json', "r") as json_data:
		todaysAnswer = json.load(json_data)
		response = jsonify({"answer": todaysAnswer["answer"]})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

@app.route('/dailyPuzzleId')
def puzzleId():
	with open('./data/todaysAnswer.json', "r") as json_data:
		todaysAnswer = json.load(json_data)
		response = jsonify({"answer": todaysAnswer["puzzleId"]})
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

if __name__ == '__main__':
    app.run(debug=True)