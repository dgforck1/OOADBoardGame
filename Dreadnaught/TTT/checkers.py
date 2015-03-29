from multiprocessing import Process, Value
from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from settings import SCRIPTS_FOLDER
from TTT.models import game
from forms import SelectGame
from copy import deepcopy
import time



killable_pieces = {'r' : ['b','B'],
				   'R' : ['b','B'],
				   'b' : ['r','R'],
				   'B' : ['r','R']}



start_state = '[[0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0]]'




def create_board(size):
	board = []

	for y in range(size):
		board.append([])
		for x in range(size):
			board[y].append('')

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



def check_move(board, x, y, dx, dy, turn, l):
	if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
		return

	if board[y + dy][x + dx] is ' ':
		l.append([x + dx, y + dy])



def check_jump(board, x, y, dx, dy, piece, l, path, possibilities):
	if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
		if len(path) > 2:
			possibilities += 1
			l.append(path)
		else:
			return

	mx = dx / 2
	my = dy / 2

	#Check to see if jump is valid, otherwise append what you have and return
	if board[my][mx] is killable_pieces[board[x][y]]:
		#Remove jumped piece from board
		board[my][mx] = ' '

		#Add current jump to the path
		path.append(x + dx)
		path.append(y + dy)

		ty = []
		
		if piece is 'r' or piece is 'R':
			ty.append(-2)
		elif piece is 'b' or piece is 'B':
			ty.append(2)

		for i in [-2, 2]:
			for j in ty:
				check_jump(deepcopy(board), x, y, i, j, turn, possibles, [x, y], possibilities)

	else:
		if len(path) > 2:
			possibilities += 1
			l.append(path)
		else:
			return



def get_possible_moves(board, turn):
	possibles = []

	king = turn.capitalize()
	
	for y, row in enumerate(board):
		for x, pos in enumerate(row):
			if pos is turn:
				possibilities = 0
				dy = 0

				if turn is 'b':
					dy = -2
				elif turn is 'r':
					dy = 2

				for i in [-2, 2]:
					check_jump(deepcopy(board), x, y, i, dy, pos, possibles, [x, y], possibilities)

				if piece < 1:
					for i in [-1, 1]:
						check_move(deepcopy(board), x, y, i, dy, pos, possibles)
			if pos is king:
				possibilities = 0

				for i in [-2, 2]:
					for j in [-2, 2]:
						check_jump(deepcopy(board), x, y, i, j, pos, possibles, [x, y], possibilities)

				if possibilities < 1:
					for i in [-1, 1]:
						for j in [-1, 1]:
							check_move(deepcopy(board), x, y, i, j, pos, possibles)

	return possibles



def endgame_check(board, state):
	return 5



def ai_error(state, error):
    print('AI Terminated: ' + error)

    if state is 1:
        return 4
    elif state is 2:
        return 3
    else:
    	return state



def play_turn(game):
	state = game.state
	move_val = None
	time_left = game.time_left
	board = json.load(game.board)

	if state is 1:
		turn = 'b'
		player = game.player1
		ai = game.ai1script
	elif state is 2:
		turn = 'r'
		player = game.player2
		ai = game.ai2script
	else:
		return create_results_html(history, state)

	possibles = get_possible_moves(board, turn)

	exec('from scripts.{0} import get_move as move_d'.format(ai.location.split('/')[-1].rstrip('.py'))) in globals(), locals()
    
	if player is None:
		if ai is None:
			state = 5
			time_left = 0
		else:
	        if state is 1 or state is 2:
	            def get_move(board, current_time, state_flag, result, timer):
	                t = time.time()

	                result.value = move_d(json.dump(board), current_time, 'b' if state_flag else 'r')

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

	                state = ai_error(state, 'Timeout')
	            else:
	                time_left -= timer.value
	                move_val = result.value

	        if move_val in possibles:
	            state = endgame_check(board, state)
	        else:
				state = ai_error(state, 'Invalid Move')
	else:
		if ai is None:
			#Human is playing without ai assistance
			pass
		else:
			#Human is playing with ai assistance
			pass



	game.time_left = time_left
	game.state = state
	game.board = json.dump(board)
	game.save()


def select_game(request):
    if request.method == 'POST':
        form = SelectGame(request.POST)

        if form.is_valid():
            ai1 = form.cleaned_data['player1']
            ai2 = form.cleaned_data['player2']

            g = game(ai1script = ai1, ai2script  = ai2, state = 1)
            g.save()

            if not ai1 is "None" and not ai2 is "None":
				gid = -1
				board = start_state
				state = 1
				
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