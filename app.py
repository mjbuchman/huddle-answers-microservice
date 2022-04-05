from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv 
import json, requests, os

app = Flask(__name__)
CORS(app)
load_dotenv()
    
answerBin = os.environ.get("answerBin")
masterKey = os.environ.get("masterKey")

def getFile():
	url = f'https://api.jsonbin.io/v3/b/{answerBin}'
	headers = {
		'X-Master-Key': masterKey
	}
	return requests.get(url, json=None, headers=headers)

@app.route('/', methods=['GET', 'POST'])
def index():
	json_data = getFile()
	print(json_data)
	todaysAnswer = json.loads(json_data.text)
	return render_template("index.html", answer=todaysAnswer["record"]["answer"], puzzleId=todaysAnswer["record"]["puzzleId"])

@app.route('/dailyAnswer')
def answer():
	json_data = getFile()
	todaysAnswer = json.loads(json_data.text)
	response = jsonify({"answer": todaysAnswer["record"]})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == '__main__':
    app.run()