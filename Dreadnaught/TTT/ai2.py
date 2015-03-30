def get_move(state, time_left, piece):
    from StringIO import StringIO
    from copy import deepcopy
    import random, json
    random.seed(None)

    possibles = []
    board = json.load(StringIO(state))
    killable_pieces = {u'r' : [u'b',u'B'],
                       u'R' : [u'b',u'B'],
                       u'b' : [u'r',u'R'],
                       u'B' : [u'r',u'R'],
                       u' ' : []}

    king_pieces = { u'r' : [u'R'],
                    u'R' : [u'R'],
                    u'b' : [u'B'],
                    u'B' : [u'B'],
                    u' ' : []}

    def check_move(board, x, y, dx, dy, turn, l):
        if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
            return

        if board[y + dy][x + dx] == u' ':
            l.append([[[x, y], [x + dx, y + dy]]])



    def check_jump(board, x, y, dx, dy, piece, l, path, depth=0):
        if  x + dx >= len(board[0]) or y + dy >= len(board) or x + dx < 0 or y + dy < 0:
            if len(path) > 0:
                #print path, dx, dy
                l.append(path)
                return
            else:
                return

        mx = dx / 2
        my = dy / 2

        #Check to see if jump is valid, otherwise append what you have and return
        if board[y + my][x + mx] in killable_pieces[board[y][x]] and board[y + dy][x + dx] == u' ':
            #Remove jumped piece from board
            board[y + my][x + mx] = u' '
            board[y + dy][x + dx] = board[y][x]
            board[y][x] = u' '

            #Add current jump to the path
            path.append([[x, y], [x + dx, y + dy]])

            ty = []
            
            if piece != u'b':
                ty.append(-2)
            elif piece != u'r':
                ty.append(2)

            for i in [-2, 2]:
                for j in ty:
                    check_jump(deepcopy(board), x + dx, y + dy, i, j, piece, l, deepcopy(path), depth + 1)
        else:
            if len(path) > 0:
                #print path, mx, my, dx, dy
                l.append(path)
                return
            else:
                return



    def get_possible_moves(board, piece):
        possibles = []

        king = king_pieces[piece]
        
        for y, row in enumerate(board):
            for x, pos in enumerate(row):
                if pos == piece:
                    dy = 0

                    if pos == u'r':
                        dy = -2
                    elif pos == u'b':
                        dy = 2

                    for i in [-2, 2]:
                        check_jump(deepcopy(board), x, y, i, dy, pos, possibles, [])
                elif pos == king:
                    for i in [-2, 2]:
                        for j in [-2, 2]:
                            check_jump(deepcopy(board), x, y, i, j, pos, possibles, [])
        
        if len(possibles) <= 0:
            for y, row in enumerate(board):
                for x, pos in enumerate(row):
                    if pos == piece:
                        dy = 0

                        if pos == u'r':
                            dy = -1
                        elif pos == u'b':
                            dy = 1

                        for i in [-1, 1]:
                            check_move(board, x, y, i, dy, pos, possibles)
                    elif pos == king:
                        for i in [-1, 1]:
                            for j in [-1, 1]:
                                check_move(board, x, y, i, j, pos, possibles)
        return possibles

    possibles = get_possible_moves(board, piece)

    if len(possibles) > 0:
        return json.dumps(random.choice(possibles))
    else:
        return '[]'