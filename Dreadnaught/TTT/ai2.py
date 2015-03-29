def get_move(state, time_left, piece):
	import random, json
	random.seed(None)

	possibles = []
	board = json.load(state)

	#Get all possible moves

	#Randomly choose a possible move
	return json.dump(random.choice(possibles))