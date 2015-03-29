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
                       u'B' : [u'r',u'R']}

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
                                print x, y, i, j
                                check_move(deepcopy(board), x, y, i, j, pos, possibles)

        return possibles

    possibles = get_possible_moves(board, piece)

    try:
        return json.dumps(random.choice(possibles))
    except:
        print 'Failed Choice'
        return ''  