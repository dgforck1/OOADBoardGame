import copy



killable_pieces = {'r' : ['b','B'],
				   'R' : ['b','B'],
				   'b' : ['r','R'],
				   'B' : ['r','R']}



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



def check_move(board, x, y, dx, dy, turn):
	if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
		return None

	king = turn.capitalize()

	if board[y + dy][x + dx] is '':
		return [x + dx, y + dy]
	elif not (board[y + dy][x + dx] is turn or board[y + dy][x + dx] is king):
		return check_jump(copy.deepcopy(board), x, y, dx * 2, dy * 2, turn)
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
				result = check_move(copy.deepcopy(board), x, y, 1, 1, turn)

				if not result is None:
					possibles.append([x, y] + result)

				result = check_move(board, x, y, -1, 1, turn)

				if not result is None:
					possibles.append([x, y] + result)

	return possibles



def endgame_check(board, pieces, state):
	return state



def create_results_html(board, state):
	return "THIS IS A TEST"



def create_ingame_html(board, possibles, state):
    if state == 1:
        statement = 'Black\'s Turn'
    elif state == 2:
        statement = 'Red\'s Turn'
    elif state == 3:
        statement = 'Black Wins'
    elif state == 4:
        statement = 'Red Wins'
    elif state == 5:
        statement = 'Draw'
        
    html_str = '\
    <h1>Welcome!</h1> \
    <h2>Checkers</h2> \
    '

    html_str += '<table border=1>'

    for y in range(8):
        html_str += '<tr> '

        for x in range(8):
        	html_str += '<th>{0}</th>'.format(board[y][x])

        html_str += ' </tr>'

    html_str += '</table> \
    <p>%s</p>' % (statement)

    return html_str



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

	possibles = get_possible_moves(board, [], turn)

	exec('from scripts.{0} import get_move as move_d'.format(ai.location.split('/')[-1].rstrip('.py'))) in globals(), locals()
    
	if player is None:
		if ai is None:
			state = 5
			time_left = 0
		else:
	        if state is 1 or state is 2:
	            def get_move(board, current_time, state_flag, result, timer):
	                t = time.time()

	                result.value = move_d(board, current_time, 'b' if state_flag else 'r')

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



	if state is 1 or state is 2:
		return create_ingame_html(board, possibles, state)
	else:
		return create_results_html(board, state)



def play_game(request):
    gid = -1
    
    if request.method == 'POST':
        form = PlayGame(request.POST)

        if form.is_valid():
            move = form.cleaned_data['move']

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

    return render(request, 'human_game.html', {'form': PlayGame(request.POST), 'gid': gid, 'html_string': results})