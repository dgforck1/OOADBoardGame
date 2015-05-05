

import time

class Game:
    def __init__(self):
        self.id = 0
        self.state = 1
        self.history = ""
        self.ai1script = "/home/nemesis/CISS438/OOADBoardGame/Dreadnaught/TTT/scripts/ai1.py"
        self.ai2script = "/home/nemesis/CISS438/OOADBoardGame/Dreadnaught/TTT/scripts/ai2.py"
        self.time_left = 900000.0




def select_game(request):
    if request.method == 'POST':
        form = SelectGame(request.POST)

        if form.is_valid():
            ai1 = form.cleaned_data['player1']
            ai2 = form.cleaned_data['player2']

            g = game(ai1script = ai1, ai2script  = ai2, state = 1)
            g.save()

            if ai1 is "None" and ai2 is "None":
                #That is all
                return render(request, 'select_game.html', {'form': form})
            elif ai1 is "None" or ai2 is "None":
                gid = g.id

                results = play_turn(g)

                #play_game view should actually handle any game involving humans
                return render(request, 'human_game.html', {'form': \
                       PlayGame(request.POST), 'gid': gid, 'html_string': results})
            else:
                results = play(g)
                return game_results(request, g.id)
    else:
        form = SelectGame()

    return render(request, 'select_game.html', {'form': form})


#@csrf_exempt
def play_game(request):
    gid = -1
    state = 0
    
    if request.method == 'POST':
        gid = request.POST['gameid']

        g = game.objects.get(id = gid)
        g.history += '%d' % (move)
        g.state = ((g.state % 2) + 1)
        g.save()

        results = play_turn(g)
    else:
        form = PlayGame()
        gid = -1
        results = 'Nope!'

    return render(request, 'human_game.html', \
        {'form': PlayGame(request.POST), 'gid': gid, 'html_string': results})



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



def create_ingame_html(history, state):
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



def create_results_html(history, state):
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
    '''
    IN DESPARATE NEED OF CLEANUP
    WILL HANDLE WHEN CONVERTING TO CHECKERS
    '''
    if not (game.state is 0 or game.state is 1):
        return 'Broken'

    board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
    hist = []
    state = 1

    ai1 = game.ai1script.location
    ai2 = game.ai2script.location
    ai1 = ai1.split('/')
    ai2 = ai2.split('/')    
    exec('from scripts.{0} import get_move as get_move1'.format(ai1[-1].rstrip('.py'))) in globals(), locals()         
    exec('from scripts.{0} import get_move as get_move2'.format(ai2[-1].rstrip('.py'))) in globals(), locals()
    move_d = {'1' : get_move1, '2' : get_move2}
    time_left = game.time_left


    while True:
        if state is 1 or state is 2:
            def get_move(board, current_time, state_flag, result, timer):
                t = time.time()

                if state_flag:
                    result.value = move_d['1'](board, current_time, 'x')
                else:
                    result.value = move_d['2'](board, current_time, 'o')

                t = (time.time() - t) * 1000
                timer.value = t



            start = time.time()

            result = Value('i', 0)
            timer = Value('d', 0.0)

            ai_process = Process(target = get_move, args = (board, time_left, state is 1, result, timer))
            ai_process.start()
            ai_process.join(time_left)

            if ai_process.is_alive():
                ai_process.terminate()

                print("AI Terminated")

                if state is 1:
                    state = 4
                elif state is 2:
                    state = 3
                break
            else:
                time_left -= timer.value
                hist.append(result.value)

        if state == 3 or state == 4:
            break

        if hist[-1] is None:
            hist.pop()
        else:
            board[hist[-1]] = 'x' if state is 1 else 'o'
            state = state_check(board, state)
            temp = ''

        if state != 1 and state != 2:
            break

    temp = ''

    for move in hist:
        temp += '{0}'.format(move)

    game.history = temp
    game.state = state
    game.time_left = time_left
    game.save()

    if state is 3:
        game.ai1script.wins +=1
    elif state is 4:
        game.ai1script.losses += 1
    elif state is 5:
        game.ai1script.draws += 1

    game.ai1script.save()

    if state is 3:
        game.ai2script.losses +=1
    elif state is 4:
        game.ai2script.wins += 1
    elif state is 5:
        game.ai2script.draws += 1

    game.ai2script.save()
    
    return create_results_html(hist, state)



def play_turn(game):
    '''
    IN DESPARATE NEED OF CLEANUP
    WILL HANDLE WHEN CONVERTING TO CHECKERS
    '''
    if game is None:
        return 'No Game Passed'
    if game.state == 0 or game.state == 3 or game.state == 4 or game.state == 5:
        return 'Wrong State'

    board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
    hist = []
    ai = None

    for i, l in enumerate(game.history):
        pos = int(l)

        if i % 2 == 0:
            board[pos] = 'x'
        else:
            board[pos] = 'o'

        hist.append(pos)

    piece = ''

    if game.state == 1:
        ai = game.ai1script

        if ai == None:
            return create_ingame_html(hist, game.state)

        ai = ai.location.split('/')
        exec('from scripts.{0} import get_move as get_move1'.format(ai[-1].rstrip('.py')))
        piece = 'x'

        hist.append(value)
    elif game.state == 2:
        ai = game.ai2script

        if ai == None:
            return create_ingame_html(hist, game.state)
        
        ai = ai.location.split('/')
        exec('from scripts.{0} import get_move as get_move2'.format(ai.location[-1].rstrip('.py')))
        piece = 'o'
        hist.append(get_move2(board, 0, piece))


    board[hist[-1]] = piece
    state = state_check(board, game.state)
    temp = ''

    for move in hist:
        temp += '{0}'.format(move)

    game.history = temp
    game.state = state
    game.save()

    return create_ingame_html(hist, state)
