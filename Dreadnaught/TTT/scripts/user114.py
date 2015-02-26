def get_move(board, time_left, piece):
    for i in range(3):     #scan columns
	#add check that i + 3 <> ' '
	#check left col for wins or blocks
	if board[i + 3] == board[i + 6]:
	    if board[i] == ' ':
		return i
			
	#check middle col for wins or blocks
	if board[i] == board[i + 6]:
	    if board[i + 3] == ' ':
		return i + 3
		
	#check right col for wins or blocks
	if board[i] == board[i + 3]:
	    if board[i + 6] == ' ':				
		return i + 6
		
    n = 0
    o = 1
    p = 2

    #scan rows
    while n <= 6:		
	if board[n] == board[o]:
	    if board[p] == ' ':
		return p
	n += 3
	o += 3
	p += 3

    #check diags
    if board[0] != ' ':
	if board[4] == board[0]:
	    if board[8] == ' ':
		return 8
	elif board[8] == board[0]:
	    if board[4] == ' ':
		return 4

	elif board[4] != ' ':
	    if board[4] == board[8]:
		return 0


    if board[2] != ' ':
	if board[4] == board[2]:
	    if board[6] == ' ':
		return 6
	elif board[6] == board[2]:
	    if board[4] == ' ':
		return 4
	elif board[4] != ' ':
	    if board[4] == board[6]:
		return 2

    #found no wins or blocks
    if board[4] == ' ':
	return 4
    else:
	#place adjacent to apiece
	for i in range(len(board)):
	    if board[i] == piece:
		if i + 1 < 9:
		    if board[i + 1] == ' ':
			return i + 1

		if i - 1 >= 0:
		    if board[i - 1] == ' ':
			return i - 1

		if i + 3 < 9:
		    if board[i + 3] == ' ':
			return i + 3

		if i - 3 >= 0:
		    if board[i - 3] == ' ':
			return i - 3

		#place in first empty space
		
	for i in range(len(board)):
	    if board[i] == ' ':
		return i
		
