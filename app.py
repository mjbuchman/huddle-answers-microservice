from flask import Flask, jsonify, render_template, request
from datetime import date
import json,random

app = Flask(__name__)

def determineAnswer(advance):
	if advance:
		dateSeed = random.randint(0,1000)
	else:
		dateSeed = date.today().strftime("%m%d%Y")
	random.seed(int(dateSeed))
	with open('./data/players.json') as json_data:
		players = json.load(json_data)
		index = random.randint(0,len(players)-1)
		return players[index]

def getPuzzleId(advance):
	if advance:
		startDate = date(2021,random.randint(1,11),random.randint(1,20))
	else:
		startDate = date(2022,4,4) #YYYY-mm-dd
	id = date.today() - startDate
	return id.days

@app.route('/', methods=['GET', 'POST'])
def index():
	global counter
	if request.method == 'POST':
		if request.form.get('advance') == 'Advance Day':
			advance = True
		else:
			advance = False
	elif request.method == 'GET':
		return render_template("index.html", answer=determineAnswer(False), puzzleId=getPuzzleId(False))

	return render_template("index.html", answer=determineAnswer(advance), puzzleId=getPuzzleId(advance))

@app.route('/dailyAnswer')
def answer():
    return determineAnswer(False)

@app.route('/dailyPuzzleId')
def puzzleId():
	return jsonify({"puzzleId": getPuzzleId(False)})

if __name__ == '__main__':
    app.run(debug=True)