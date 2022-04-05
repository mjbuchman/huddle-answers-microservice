from datetime import date
import json,random

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
  
if __name__ == '__main__':
    rolloverDay()