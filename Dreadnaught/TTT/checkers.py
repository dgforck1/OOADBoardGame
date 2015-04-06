from multiprocessing import Process, Manager, Value
from ctypes import c_char_p
from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from settings import SCRIPTS_FOLDER
from TTT.models import game, turns
from forms import SelectGame
from copy import deepcopy
from StringIO import StringIO
import json
import time



killable_pieces = {u'r' : [u'b',u'B'],
                   u'R' : [u'b',u'B'],
                   u'b' : [u'r',u'R'],
                   u'B' : [u'r',u'R']}



begin_state = '[[" ", "b", " ", "b", " ", "b", " ", "b"],["b", " ", "b", " ", "b", " ", "b", " "],[" ", "b", " ", "b", " ", "b", " ", "b"],[" ", " ", " ", " ", " ", " ", " ", " "],[" ", " ", " ", " ", " ", " ", " ", " "],["r", " ", "r", " ", "r", " ", "r", " "],[" ", "r", " ", "r", " ", "r", " ", "r"],["r", " ", "r", " ", "r", " ", "r", " "]]'



def check_move(board, x, y, dx, dy, turn, l):
    if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
        return

    if board[y + dy][x + dx] == u' ':
        l.append([[x, y], [x + dx, y + dy]])



def check_jump(board, x, y, dx, dy, piece, l, path, possibilities):
    if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
        if len(path) > 2:
            possibilities += 1
            l.append(path)
            return
        else:
            return

    mx = dx / 2
    my = dy / 2

    #Check to see if jump is valid, otherwise append what you have and return
    if board[my][mx] in killable_pieces[board[y][x]]:
        #Remove jumped piece from board
        board[my][mx] = u' '

        #Add current jump to the path
        path.append([x + dx, y + dy])

        ty = []
        
        if piece != u'b':
            ty.append(-2)
        elif piece != u'r':
            ty.append(2)

        for i in [-2, 2]:
            for j in ty:
                check_jump(deepcopy(board), x, y, i, j, piece, l, deepcopy(path), possibilities)
    else:
        if len(path) > 2:
            possibilities += 1
            l.append(path)
            return
        else:
            return



def get_possible_moves(board, piece):
    possibles = []

    king = piece.capitalize()
    
    for y, row in enumerate(board):
        for x, pos in enumerate(row):
            if pos == piece:
                possibilities = 0
                dy = 0

                if pos == u'r':
                    dy = -2
                elif pos == u'b':
                    dy = 2

                for i in [-2, 2]:
                    check_jump(deepcopy(board), x, y, i, dy, pos, possibles, [[x, y]], possibilities)

                dy /= 2

                if possibilities < 1:
                    for i in [-1, 1]:
                        check_move(deepcopy(board), x, y, i, dy, pos, possibles)
            if pos == king:
                possibilities = 0

                for i in [-2, 2]:
                    for j in [-2, 2]:
                        check_jump(deepcopy(board), x, y, i, j, pos, possibles, [[x, y]], possibilities)

                if possibilities < 1:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            check_move(deepcopy(board), x, y, i, j, pos, possibles)

    return possibles



def king_pieces(board):
    top_row = board[0]
    bottom_row = board[-1]

    for pos in top_row:
        if pos == u'r':
            pos = u'R'

    for pos in bottom_row:
        if pos == u'b':
            pos = u'B'

    return board



def endgame_check(board, state):
    black_count = 0
    red_count = 0

    for row in board:
        for pos in row:
            if pos == u'r' or pos == u'R':
                red_count += 1
            if pos == u'b' or pos == u'B':
                black_count += 1

    if red_count <= 0:
        return 3

    if black_count <= 0:
        return 4

    return state



def ai_error(state, error):
    print('AI Terminated: ' + error)

    if state == 1:
        return 4
    elif state == 2:
        return 3
    else:
        return state




def play_turn(game, turn_count):
    state = game.state
    move_val = None
    time_left = game.time_left
    t = turns.objects.get(game = game, turn_num = turn_count)
    board = json.load(StringIO(t.begin_state))

    turn_count += 1

    if state == 1:
        turn = 'b'
        player = game.player1
        ai = game.ai1script
    elif state == 2:
        turn = 'r'
        player = game.player2
        ai = game.ai2script
    else:
        return create_results_html(history, state)

    possibles = get_possible_moves(board, turn)
    
    if player == None:
        if ai == None:
            state = 5
            time_left = 0
        else:
            if state == 1 or state == 2:
                def get_move(board, ai, current_time, state_flag, result, timer):
                    t = time.time()

                    exec('from scripts.{0} import get_move as move_f'.format(ai.location.split('/')[-1].rstrip('.py'))) in globals(), locals()
                    result.value = move_f(json.dumps(board), current_time, 'b' if state_flag else 'r')

                    t = (time.time() - t) * 1000
                    timer.value = t



                start = time.time()

                result = Manager().Value(c_char_p, '')
                timer = Value('d', 0.0)

                ai_process = Process(target = get_move, args = (board, ai, time_left, state == 1, result, timer))
                ai_process.start()
                ai_process.join(time_left)

                if ai_process.is_alive():
                    ai_process.terminate()

                    state = ai_error(state, 'Timeout')
                else:
                    time_left -= timer.value
                    move_val = json.load(StringIO(result.value))

            if move_val in possibles:
                start = move_val[0]
                dest = move_val[1]

                temp = board[start[1]][start[0]]
                board[start[1]][start[0]] = ' '
                board[dest[1]][dest[0]] = temp

                if start[1] - dest[1] > 1 or start[1] - dest[1] < -1:
                    mid_x = (start[0] + dest[0]) / 2
                    mid_y = (start[1] + dest[1]) / 2

                    board[mid_y][mid_x] = ' '

                board = king_pieces(board)
                state = endgame_check(board, state)
            else:
                state = ai_error(state, 'Invalid Move')
    else:
        return

    game.time_left = time_left
    game.state = state
    turn = turns(game=game, turn_num=turn_count, begin_state=json.dumps(board))
    turn.save()
    game.save()

def select_game(request):
    if request.method == 'POST':
        form = SelectGame(request.POST)

        if form.is_valid():
            ai1 = form.cleaned_data['player1']
            ai2 = form.cleaned_data['player2']
            time_limit = form.cleaned_data['timelimit']

            if time_limit == None:
                time_limit = 900000

            g = game(ai1script = ai1, ai2script  = ai2, state = 1, time_left = time_limit)
            g.save()

            if not ai1 == "None" and not ai2 == "None":
                board = begin_state
                t = 0

                turn = turns(game=g, turn_num=t, begin_state=begin_state)
                turn.save()

                play_turn(g, t)

                while g.state == 1 or g.state == 2:
                    g.state = ((g.state % 2) + 1)
                    play_turn(g, t)

                turnsobj = turns.objects.filter(game_id = g.id)
                d = {'game' : g}

                turns1 = []


                for t in turnsobj:
                    turns1.append(t.begin_state)

                import json
                
                for a in range(len(turns1)):
                    turns1[a] = json.loads(turns1[a])
                    turns1[a] = json.dumps(turns1[a])
                    print turns1[a]
                
                d['turns'] = turns1

                return render(request, 'game_results.html', d)
                #return render(request, 'select_game.html', {'form': form})
    else:
        form = SelectGame()

    return render(request, 'select_game.html', {'form': form})



def play_game(request):
    return "BROKEN"