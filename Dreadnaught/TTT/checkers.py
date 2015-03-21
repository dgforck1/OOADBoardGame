class Game:
    def __init__(self):
        self.id = 0
        self.state = 1
        self.history = ""
        self.ai1script = "/home/nemesis/CISS438/OOADBoardGame/Dreadnaught/TTT/scripts/ai1.py"
        self.ai2script = "/home/nemesis/CISS438/OOADBoardGame/Dreadnaught/TTT/scripts/ai2.py"
        self.time = 900000.0

class Piece:
	def __init__(self):
		x = 0
		y = 0
		is_king = False



killable_pieces = {}



def create_board(size):
	board = []

	for x in range(size):
		board.append([])
		for y in range(size):
			board[x].append('')

	for i in range((size / 2) - 1):
		for x in range(size / 2):
			spacer = 0

			if i % 2 is 0:
				spacer += 1

			board[i][x * 2 + spacer] = 'b'

			spacer += 1
			spacer %= 2

			board[(size - 1) - i][x * 2 + spacer] = 'r'

	return board

def check_move(board, x, y, dx, dy, turn):
	if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
		return None

	king = turn.capitalize()

	if board[y + dy][x + dx] is '':
		return [x + dx, y + dy]
	elif not (board[y + dy][x + dx] is turn or board[y + dy][x + dx] is king):
		return check_jump(board, x, y, dx * 2, dy * 2, turn)
	else:
		return None


def check_jump(board, x, y, dx, dy, turn):
	if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
		return None

	if board[y + dy][x + dx] is '':
		return [x + dx, y + dy]
	else:
		return None


def get_possible_moves(board, pieces, turn):
	possibles = []

	king = turn.capitalize()
	
	for y, row in enumerate(board):
		for x, pos in enumerate(row):
			if pos is turn:
				result = check_move(board, x, y, 1, 1, turn)

				if not result is None:
					possibles.append([x, y] + result)

				result = check_move(board, x, y, -1, 1, turn)

				if not result is None:
					possibles.append([x, y] + result)

	return possibles