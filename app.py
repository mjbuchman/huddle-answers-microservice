from flask import Flask, jsonify, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
    
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
    app.run()