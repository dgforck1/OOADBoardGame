from multiprocessing import Process, Value
'''
from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from settings import SCRIPTS_FOLDER
from TTT.models import game
from forms import SelectGame
'''
from copy import deepcopy
from StringIO import StringIO
import json
import time



killable_pieces = {u'r' : [u'b',u'B'],
                   u'R' : [u'b',u'B'],
                   u'b' : [u'r',u'R'],
                   u'B' : [u'r',u'R']}



start_state = '[[0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0]]'
begin_state = StringIO('[[" ", " ", " ", " ", " ", "b", " ", "b"],["b", " ", "b", " ", "b", " ", "b", " "],[" ", "b", " ", "b", " ", "b", " ", "b"],[" ", " ", " ", " ", " ", " ", " ", " "],[" ", " ", " ", " ", " ", " ", " ", " "],["r", " ", "r", " ", "r", " ", "r", " "],[" ", "r", " ", "r", " ", "r", " ", "r"],["r", " ", "r", " ", "r", " ", "r", " "]]')


class Game:
    def __init__(self):
        self.id = 0
        self.board = begin_state
        self.state = 1
        self.history = ""
        self.ai1script = "/home/nemesis/CISS438/OOADBoardGame/Dreadnaught/TTT/scripts/ai2.py"
        self.ai2script = "/home/nemesis/CISS438/OOADBoardGame/Dreadnaught/TTT/scripts/ai2.py"
        self.player1 = None
        self.player2 = None
        self.time_left = 60000.0




def create_board(size):
    board = []

    for y in range(size):
        board.append([])
        for x in range(size):
            board[y].append('')

    for i in range((size / 2) - 1):
        for x in range(size / 2):
            spacer = 0

            if i % 2 == 0:
                spacer += 1

            board[i][x * 2 + spacer] = 'b'

            spacer += 1
            spacer %= 2

            board[(size - 1) - i][x * 2 + spacer] = 'r'

    return board



def check_move(board, x, y, dx, dy, turn, l):
    if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
        return

    print x, y, dx, dy

    if board[y + dy][x + dx] == u' ':
        l.append([[x, y], [x + dx, y + dy]])



def check_jump(board, x, y, dx, dy, piece, l, path, possibilities):
    if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
        if len(path) > 2:
            possibilities += 1
            print x, y, dx, dy, piece, possibilities, path
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
            print x, y, dx, dy, piece, possibilities, path
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

                if possibilities < 1:
                    for i in [-1, 1]:
                        print x, y, i, j
                        check_move(deepcopy(board), x, y, i, dy, pos, possibles)
            if pos == king:
                possibilities = 0

                for i in [-2, 2]:
                    for j in [-2, 2]:
                        check_jump(deepcopy(board), x, y, i, j, pos, possibles, [[x, y]], possibilities)

                if possibilities < 1:
                    for i in [-1, 1]:
                        for j in [-1, 1]:
                            print x, y, i, j
                            check_move(deepcopy(board), x, y, i, j, pos, possibles)

    return possibles



def endgame_check(board, state):
    return 5



def ai_error(state, error):
    print('AI Terminated: ' + error)

    if state == 1:
        return 4
    elif state == 2:
        return 3
    else:
        return state




def play_turn(game):
    state = game.state
    move_val = None
    time_left = game.time_left
    board = json.load(game.board)

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
    print possibles

    
    if player == None:
        if ai == None:
            state = 5
            time_left = 0
        else:
            if state == 1 or state == 2:
                def get_move(board, ai, current_time, state_flag, result, timer):
                    t = time.time()

                    exec('from scripts.{0} import get_move as move_f'.format(ai.split('/')[-1].rstrip('.py'))) in globals(), locals()
                    result.value = move_f(json.dumps(board), current_time, 'b' if state_flag else 'r')

                    t = (time.time() - t) * 1000
                    timer.value = t



                start = time.time()

                result = Value('i', 0)
                timer = Value('d', 0.0)

                ai_process = Process(target = get_move, args = (board, ai, time_left, state == 1, result, timer))
                ai_process.start()
                ai_process.join(time_left)

                if ai_process.is_alive():
                    ai_process.terminate()

                    state = ai_error(state, 'Timeout')
                else:
                    time_left -= timer.value
                    move_val = result.value

            if move_val in possibles:
                state = endgame_check(board, state)
            else:
                state = ai_error(state, 'Invalid Move')
    else:
        if ai == None:
            #Human is playing without ai assistance
            pass
        else:
            #Human is playing with ai assistance
            pass



    game.time_left = time_left
    game.state = state
    game.board = json.dumps(board)
    #game.save()

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
                gid = -1
                board = start_state
                state = 1

                g = Game()
                play_turn(g)

                print(g.state)
                
                return render(request, 'checkers_temp.html', {'gid': gid, 'state' : state, 'board' : board})
    else:
        form = SelectGame()

    return render(request, 'select_game.html', {'form': form})



@csrf_exempt
def play_game(request):
    gid = -1
    board = start_state
    state = 1
    
    if request.method == 'POST':
        state = 2
        #gid = request.POST['gameid']

        #g = game.objects.get(id = gid)
        #g.state = ((g.state % 2) + 1)
        #g.save()

        #play_turn(g)

    return render(request, 'checkers_temp.html', {'gid': gid, 'state' : state, 'board' : board})
'''
g = Game()
play_turn(g)

print(g.state)
'''