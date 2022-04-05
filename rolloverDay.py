from dotenv import load_dotenv 
from datetime import datetime
import json, random, requests, os

load_dotenv()

playersBin = os.environ.get("playersBin")
usedBin = os.environ.get("usedBin")
answerBin = os.environ.get("answerBin")
masterKey = os.environ.get("masterKey")

def getFile(bin):
	url = f'https://api.jsonbin.io/v3/b/{bin}'
	headers = {
		'X-Master-Key': masterKey
	}
	return requests.get(url, json=None, headers=headers)

def updateFile(bin, data):
	url = f'https://api.jsonbin.io/v3/b/{bin}'
	headers = {
		'Content-Type': 'application/json',
		'X-Master-Key': masterKey
	}
	return requests.put(url, json=data, headers=headers)

def addToUsedAndDelete(answer, players, index):
	json_data = getFile(usedBin)
	used = json.loads(json_data.text)
	used["record"].append(answer["Name"])
	updateFile(usedBin, used["record"])
 
	del players["record"][index]
	updateFile(playersBin, players["record"])

def determineAnswer():
	dateSeed = datetime.now().strftime("%m%d%Y%H%M%S")
	random.seed(int(dateSeed))
	json_data = getFile(playersBin)
	players = json.loads(json_data.text)
	index = random.randint(0,len(players["record"])-1)
	answer = players["record"][index]
	addToUsedAndDelete(answer, players, index)
	return answer
  
def rolloverDay():
	json_data = getFile(answerBin)
	todaysAnswer = json.loads(json_data.text)
	jsonString = {"answer": determineAnswer(), "puzzleId": todaysAnswer["record"]["puzzleId"] + 1}
	updateFile(answerBin, jsonString)
  
if __name__ == '__main__':
    rolloverDay()