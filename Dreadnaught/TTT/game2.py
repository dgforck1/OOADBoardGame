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
        return state_translate(board[1])
    elif board[2] == board[4] == board[6] != ' ':
        return state_translate(board[2])
    elif board[2] == board[5] == board[8] != ' ':
        return state_translate(board[2])
    elif board[3] == board[4] == board[5] != ' ':
        return state_translate(board[3])
    elif board[6] == board[7] == board[8] != ' ':
        return state_translate(board[6])
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



def create_html2(history, state):
    pieces = []
    
    for i in range(9):
        pieces.append('&nbsp; &nbsp;')

    for i, move in enumerate(history):
        if i % 2 == 0:
            pieces[move] = 'X'
        else:
            pieces[move] = 'O'
    
    if state == 1:
        statement = 'X\'s Turn'
    elif state == 2:
        statement = 'O\'s Turn'
    elif state == 3:
        statement = 'X Wins'
    elif state == 4:
        statement = 'O Wins'
    elif state == 5:
        statement = 'Draw'
        
    html_str = '<h1>Welcome!</h1> \
    <h2>Tic-Tac-Toe</h2> \
    '

    html_str += '<table border=1>'

    for i in range(0, 9, 3):
        html_str += '<tr> \
        <th>%s</th> \
        <th>%s</th> \
        <th>%s</th> \
        </tr> \
        ' % (pieces[i], pieces[i + 1], pieces[i + 2])

    html_str += '</table> \
    <p>%s</p>' % (statement)

    return html_str



def create_html(history, state):
    pieces = []
    
    for i in range(9):
        pieces.append('&nbsp; &nbsp;')
        
    l = len(history)
    
    if state == 1:
        statement = 'X\'s Turn'
    elif state == 2:
        statement = 'O\'s Turn'
    elif state == 3:
        statement = 'X Wins'
    elif state == 4:
        statement = 'O Wins'
    elif state == 5:
        statement = 'Draw'
        
    html_str = '<!DOCTYPE html> \
    <html> \
    <head> \
    <meta charset=UTF-8> \
    <title>Tic-Tac-Toe</title> \
    </head> \
    <body> \
    <h1>Welcome!</h1> \
    <h2>Tic-Tac-Toe</h2> \
    '

    for i, move in enumerate(history):
        if i % 2 == 0:
            pieces[move] = 'X'
        else:
            pieces[move] = 'O'
        html_str += '\
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
        ' % (pieces[0], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7], pieces[8])

    html_str += '<p>%s</p> \
    </body> \
    </html>' % (statement)

    return html_str



def play(game):
    if game.state != 0:
        return 'Broken'

    board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
    hist = []
    state = 1

    ai1 = game.ai1script.location
    ai2 = game.ai2script.location
    ai1 = ai1.split('/')
    ai2 = ai2.split('/')    
    exec('from scripts.{0} import get_move as get_move1'.format(ai1[-1].rstrip('.py')))           
    exec('from scripts.{0} import get_move as get_move2'.format(ai2[-1].rstrip('.py')))


    while True:
        if state == 1:
            piece = 'x'
            hist.append(get_move1(board, 0, piece))
        elif state == 2:
            piece = 'o'
            hist.append(get_move2(board, 0, piece))

        board[hist[-1]] = piece
        state = state_check(board, state)
        temp = ''

        if state != 1 and state != 2:
            break

    for move in hist:
        temp += '{0}'.format(move)

    game.history = temp
    game.state = state
    game.save()

    if state == 3:
        game.ai1script.wins +=1
        game.ai2script.losses +=1
    elif state == 4:
        game.ai1script.losses +=1
        game.ai2script.wins +=1
    elif state == 5:
        game.ai1script.draws +=1
        game.ai2script.draws +=1

    game.ai1script.save()
    game.ai2script.save()
    return create_html(hist, state)



def play2(game):
    if game is None:
        return 'No Game Passed'
    if game.state == 0 or game.state == 3 or game.state == 4 or game.state == 5:
        return 'Wrong State'

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


    if game.state == 1:
        ai = game.ai1script.location

        if not ai is None:
            ai = ai.split('/')
            exec('from scripts.{0} import get_move as get_move1'.format(ai[-1].rstrip('.py')))
            piece = 'x'
            hist.append(get_move1(board, 0, piece))
    elif game.state == 2:
        ai = game.ai2script.location

        if not ai is None:
            ai = ai.split('/')
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