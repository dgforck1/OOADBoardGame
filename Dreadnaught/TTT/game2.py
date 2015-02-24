import time
from TTT.models import game



class Game:
    def __init__(self):
        self.id = 0
        self.state = 1
        self.history = ""
        self.ai1script = "/home/nemesis/CISS438/OOADBoardGame/Dreadnaught/TTT/scripts/ai1.py"
        self.ai2script = "/home/nemesis/CISS438/OOADBoardGame/Dreadnaught/TTT/scripts/ai2.py"



def state_translate(piece):
    if piece == 'x':
        return 3
    elif piece == 'o':
        return 4
    else:
        return 5



def state_check(board, state):
    if board[0] == board[1] == board[2] != ' ':
        return state_translate(board[0])
    elif board[0] == board[3] == board[6] != ' ':
        return state_translate(board[0])
    elif board[0] == board[4] == board[8] != ' ':
        return state_translate(board[0])
    elif board[1] == board[4] == board[7] != ' ':
        return state_translate(board[0])
    elif board[2] == board[4] == board[6] != ' ':
        return state_translate(board[0])
    elif board[2] == board[5] == board[8] != ' ':
        return state_translate(board[0])
    elif board[3] == board[4] == board[5] != ' ':
        return state_translate(board[0])
    elif board[6] == board[7] == board[8] != ' ':
        return state_translate(board[0])
    else:
        for i, pos in enumerate(board):
            if pos == ' ':
                return ((state % 2) + 1)
        return 5



def print_board(board):
    for i in range(3):
        for j in range(3):
            print board[i * 3 + j],
        print



def create_html(history, state):
    pieces = []
    #if winner == '':
        #winner = 'No one'
    for i in range(9):
        pieces.append(' ')
    l = len(history)
    for i in range(l):            
        if i % 2:
            pieces[history[i]] = 'O'            
        else:
            pieces[history[i]] = 'X'
    html_str = '<!DOCTYPE html> \
    <html> \
    <head> \
    <meta charset=UTF-8> \
    <title>Tic-Tac-Toe</title> \
    </head> \
    <body> \
    <h1>Welcome!</h1> \
    <h2>Tic-Tac-Toe</h2> \
    <table border=1> \
    <tr> \
    <th>%s</th> \
    <th>%s</th> \
    <th>%s</th> \
    </tr> \
    <tr> \
    <th>%s</th> \
    <th>%s</th> \
    <th>%s</th> \
    </tr> \
    <tr> \
    <th>%s</th> \
    <th>%s</th> \
    <th>%s</th> \
    </tr> \
    </table> \
    <p>%s Wins!</p> \
    </body> \
    </html>' % (pieces[0], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7], pieces[8], winner)
    
    return html_str



def play(game):
    if game.state == 0 or game.state == 3 or game.state == 4 or game.state == 5:
        return 'she can\'t take much more captain'
    board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
    hist = []
    state = 0
    ai = None
    for i, l in enumerate(game.history):
        pos = int(l)
        if i % 2 == 0:
            board[pos] = 'x'
        else:
            board[pos] = 'o'
        hist.append(pos)
    ai = game.ai1script.split('/')
    if game.state == 1:
        exec('from scripts.{0} import get_move as get_move1'.format(ai[-1].rstrip('.py')))
        piece = 'x'
        hist.append(get_move1(board, 0, piece))
    elif game.state == 2:
        exec('from scripts.{0} import get_move as get_move2'.format(ai[-1].rstrip('.py')))
        piece = 'o'
        hist.append(get_move2(board, 0, piece))
    board[hist[-1]] = piece
    state = state_check(board, state)
    temp = ''
    for move in hist:
        temp += '{0}'.format(move)
    game.history = temp
    game.state = state
    q.save()
    return create_html(hist, state)


'''
def main():
    while True:
        for game in pending_games.objects.all():
            play(game)
        time.sleep(1)



main()
'''