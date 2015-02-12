#imports



def move(board, time_left, type):
	for i, pos in enumerate(board):
		if pos == ' ':
			return i

	return 0



def endgame_check(board):
	if board[0] == board[1] == board[2] != ' ':
		return board[0]
	elif board[0] == board[3] == board[6] != ' ':
		return board[0]
	elif board[0] == board[4] == board[8] != ' ':
		return board[0]
	elif board[1] == board[4] == board[7] != ' ':
		return board[1]
	elif board[2] == board[4] == board[6] != ' ':
		return board[2]
	elif board[2] == board[5] == board[8] != ' ':
		return board[2]
	elif board[3] == board[4] == board[5] != ' ':
		return board[3]
	elif board[6] == board[7] == board[8] != ' ':
		return board[6]
	else:
		return ''



def print_board(board):
	for i in range(3):
		for j in range(3):
			print board[i * 3 + j],
		print



def play(game_id):
	board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
	piece = ''
	history = []

	for i in range(9):
		piece = 'x' if i % 2 else 'o'
		history.append(move(board, 0, piece))
		board[history[-1]] = piece

		piece = endgame_check(board)
		if not piece == '':
			break

	#upload results to database



def main():
	game_id = 0
	#setup database connection

	while True:
		pending_games = []
		#poll database for new game sessions

		for game in pending_games:
			play(game_id)
			game_id += 1

		continue

	#close database connection



#if main script, run main
