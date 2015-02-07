import random



random.seed(None)



def get_move(board, time_left, piece):
	possibles = []

	for i, pos in enumerate(board):
		if pos == ' ':
			possibles.append(i)

	return random.choice(possibles)