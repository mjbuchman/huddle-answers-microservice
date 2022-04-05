from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import date
import json,random

app = Flask(__name__)
CORS(app)

def determineAnswer():
	f = open("./data/todaysAnswer.json", "w")
	dateSeed = date.today()
	random.seed(dateSeed)
	with open('./data/players.json') as json_data:
		players = json.load(json_data)
		index = random.randint(0,len(players)-1)
		f.write(json.dumps(players[index]))
	f.close()

def getPuzzleId():
    startDate = date(2022,4,4) #YYYY-mm-dd
    id = date.today() - startDate
    return id.days

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("index.html", answer=determineAnswer(), puzzleId=getPuzzleId())

@app.route('/dailyAnswer')
def answer():
	response = jsonify({"answer": determineAnswer()})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route('/dailyPuzzleId')
def puzzleId():
	response = jsonify({"puzzleId": getPuzzleId()})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == '__main__':
    app.run(debug=True)