import time
from TTT.models import pending_games, game_results



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



def create_html(history, winner):
	'''
	history is just a list of indicies of the moves
	winner is one of three things, x, o, or empty (to denote a draw)
	needs to return the html string that David was talking about
	'''
	return None



def play(gid, path1, path2):
    board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
    piece = ''
    hist = []
    exec('from {0} import get_move as get_move1'.format(path1.rstrip('.py')))
    exec('from {0} import get_move as get_move2'.format(path2.rstrip('.py')))
    for i in range(9):
        if i % 2:
        	piece = 'o'
        	history.append(get_move2(board, 0, piece))
        else:
        	piece = 'x'
        	history.append(get_move1(board, 0, piece))
        board[history[-1]] = piece
        piece = endgame_check(board)
        if not piece == '':
            break
    temp = ''
    for move in hist:
        temp += '{0}'.format(move)
    q = game_results(id = gid, history = temp)
    q.save()
    return create_html(history, piece)



def main():    
    while True:
        for game in pending_games.objects.all():
        	#Database needs to be updated to store scripts even if they are dummies
            play(game.id, game.player1, game.player2)
        pending_games.objects.all().delete()
        time.sleep(5)




main()
