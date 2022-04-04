from flask import Flask, jsonify, render_template, request
from datetime import date
import json,random

app = Flask(__name__)
counter = 0

def determineAnswer():
	global counter
	dateSeed = date.today().strftime("%m%d%Y")
	random.seed(int(dateSeed)+counter)
	with open('./data/players.json') as json_data:
		players = json.load(json_data)
		index = random.randint(0,len(players)-1)
		return players[index]

def getPuzzleId():
    global counter
    startDate = date(2022,4,4) #YYYY-mm-dd
    id = date.today() - startDate
    return id.days + counter

@app.route('/', methods=['GET', 'POST'])
def index():
	global counter
	if request.method == 'POST':
		if request.form.get('advance') == 'Advance Day':
			counter += 1
		elif request.form.get('reset') == 'Reset Day':
			counter = 0
		else:
			pass # unknown behavior
	elif request.method == 'GET':
		return render_template("index.html", answer=determineAnswer(), puzzleId=getPuzzleId())

	return render_template("index.html", answer=determineAnswer(), puzzleId=getPuzzleId())

@app.route('/dailyAnswer')
def answer():
	response = determineAnswer()
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route('/dailyPuzzleId')
def puzzleId():
	response = jsonify({"puzzleId": getPuzzleId()})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == '__main__':
    app.run(debug=True)