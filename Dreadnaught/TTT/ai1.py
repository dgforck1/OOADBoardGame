import copy
class Node:
    def __init__(self, p, v, m, d, s, a = -100000, b = 100000):
        self.children = []
        self.parent = p
        self.value = v
        self.move = m
        self.depth = d
        self.state = s
        self.capture = 0



#global vars
max_d = 5
player = 'r'
opponent = 'b'
nodecnt = 0



def get_move(state, timeleft, player_):
    global player
    global opponent
    import json
    s = json.loads(state)

    
    if player_ == 'r':
        player = 'r'
        opponent = 'b'
    else:
        player = 'b'
        opponent = 'r'


    root = Node(None, -100000, [[0, 0], [0, 0]], 0, s)
    #parent, value, move, depth, state

    minimax('max', root)

    #print 'node cnt:', nodecnt
    #print_tree(root)
    #print 'root v:', root.value, 'root a:', root.alpha, 'root b:', root.beta, \
    #      'root child #', len(root.children)
          

    for i in root.children:
        if i.value == root.value:
            
            r = json.dumps([i.move])
            return r
    
    return '[[0, 0],[0, 0]]'


def print_tree(node):
    d = node.depth * 5
    padding = ''

    for i in range(d):
        padding += ' '

    print padding, 'd:', node.depth, 'v:', node.value, 'm:', node.move

    
    for c in node.children:
        if c.depth <= max_d - 0:
            print_tree(c)




#minimax recursive function
#operation to perform, node to perform on
def minimax(op, node):    
    
    if node.depth == max_d:
        h = get_h(node.state)
        node.value = h

        
    else:
        get_valid_moves(op, node) #generate child nodes
        
        
        

    
    return


def get_h(state):
    rp = 0 #red position
    bp = 0 #black position
    
    for i in range(len(state)):
            for j in range(len(state[i])):
                
                if state[i][j] == 'r': #we want to move across the board
                    rp += 2**(8 - i) #2^1 - 2^8
                    if i + 1 < 8:
                        if j - 1 >= 0:
                            if state[i + 1][j - 1].lower() == 'r': #strong position
                                rp += 10

                        if j + 1 < 8:
                            if state[i + 1][j + 1].lower() == 'r': #strong position
                                rp += 10
                    
                    
                elif state[i][j] == 'R':
                    rp += 25


                elif state[i][j] == 'b':
                    bp += 2**(i + 1)
                    

                    if i - 1 >= 0:
                        if j - 1 >= 0:
                            if state[i - 1][j - 1].lower() == 'b':
                                bp += 10

                        if j + 1 < 8:
                            if state[i - 1][j + 1].lower() == 'b':
                                bp += 10
                                                           
                    
                elif state[i][j] == 'B':
                    bp += 25
                    

    if player == 'r':        
        return (rp - bp)
    else:
        return (bp - rp)




def get_valid_moves(op, node):
    #print '<<<< gm d:', node.depth, op
    global nodecnt
    
    #iterate through pieces, find valid moves
    #for each valid move, call min/max
    #add all children nodes to parent node (the node that called the function)


    

    if op == 'max':
        p_ = player
        o_ = opponent
        v = 100000 #child nodes are minimizers, so set v to max value
    else:
        p_ = opponent
        o_ = player
        v = -100000 #child nodes are maximizers, so set v to min value

    pieces = [] #the way the pieces can move
    #(piece source, move type)
    
    #move types:
    #    0 - capture south-west
    #    1 - capture south-east
    #    2 - capture north-west
    #    3 - capture north-east
    #    4 - move south-west
    #    5 - move south-east
    #    6 - move north-west
    #    7 - move norht-east
    
    capture = 0

    if p_ == 'b':
        for i in range(len(node.state)):
            for j in range(len(node.state[i])):
            
                if node.state[i][j].lower() == 'b': #normal piece movement

                    #check south-west
                    if i + 1 < 8 and j - 1 >= 0:
                        y = i + 1
                        x = j - 1

                        if node.state[y][x].lower() == o_:
                            if y + 1 < 8 and x - 1 >= 0:
                                capture = 1
                                pieces.append(([i, j], 0)) #capture south-west
                            
                        elif node.state[y][x] == ' ' and capture == 0:                            
                            pieces.append(([i, j], 4)) #move south-west

                    # check south-east
                    if i + 1 < 8 and j + 1 < 8:
                        y = i + 1
                        x = j + 1

                        if node.state[y][x].lower() == o_:
                            if y + 1 < 8 and x + 1 < 8:
                                capture = 1
                                pieces.append(([i, j], 1)) #capture south-east

                        elif node.state[y][x] == ' ' and capture == 0:
                            pieces.append(([i, j], 5)) #move south-east


                    if node.state[i][j] == 'B': #king piece movement

                        #check north-west
                        if i - 1 >= 0 and j - 1 >= 0:
                            y = i - 1
                            x = j - 1

                            if node.state[y][x].lower() == o_:
                                if y - 1 >= 0 and x - 1 >= 0:
                                    capture = 1
                                    pieces.append(([i, j], 2)) #capture north-west

                            elif node.state[y][x] == ' ' and capture == 0:
                                pieces.append(([i, j], 6)) #move north-west

                        #check north-east
                        if i - 1 >= 0 and j + 1 < 8:
                            y = i - 1
                            x = j + 1

                            if node.state[y][x].lower() == o_:
                                if y - 1 >= 0 and x + 1 < 8:
                                    capture = 1
                                    pieces.append(([i, j], 3)) #capture north-east

                            elif node.state[y][x] == ' ' and capture == 0:
                                pieces.append(([i, j], 7)) #move north-east

                            
        #remove non-captures
        if capture == 1:
            temp = []
            for a in pieces:
                if a[1] <= 3:
                    temp.append(a)

            pieces = temp





    if p_ == 'r':
        for i in range(len(node.state)):
            for j in range(len(node.state[i])):
            
                if node.state[i][j].lower() == 'r': #normal piece movement

                    #check north-west
                    if i - 1 >= 0 and j - 1 >= 0:
                        y = i - 1
                        x = j - 1

                        if node.state[y][x].lower() == o_:
                            if y - 1 >= 0 and x - 1 >= 0:
                                capture = 1
                                pieces.append(([i, j], 2)) #capture north-west

                        elif node.state[y][x] == ' ' and capture == 0:
                            pieces.append(([i, j], 6)) #move north-west

                    #check north-east
                    if i - 1 >= 0 and j + 1 < 8:
                        y = i - 1
                        x = j + 1

                        if node.state[y][x].lower() == o_:
                            if y - 1 >= 0 and x + 1 < 8:
                                capture = 1
                                pieces.append(([i, j], 3)) #capture north-east

                        elif node.state[y][x] == ' ' and capture == 0:
                            pieces.append(([i, j], 7)) #move north-east




                if node.state[i][j] == 'R': #king piece movement

                    #check south-west
                    if i + 1 < 8 and j - 1 >= 0:
                        y = i + 1
                        x = j - 1

                        if node.state[y][x].lower() == o_:
                            if y + 1 < 8 and x - 1 >= 0:
                                capture = 1
                                pieces.append(([i, j], 0)) #capture south-west
                            
                        elif node.state[y][x] == ' ' and capture == 0:                            
                            pieces.append(([i, j], 4)) #move south-west

                    # check south-east
                    if i + 1 < 8 and j + 1 < 8:
                        y = i + 1
                        x = j + 1

                        if node.state[y][x].lower() == o_:
                            if y + 1 < 8 and x + 1 < 8:
                                capture = 1
                                pieces.append(([i, j], 1)) #capture south-east

                        elif node.state[y][x] == ' ' and capture == 0:
                            pieces.append(([i, j], 5)) #move south-east
                

        #remove non-captures
        if capture == 1:
            temp = []
            for a in pieces:
                if a[1] <= 3:
                    temp.append(a)

            pieces = temp

        
    n = []


    
    for a in pieces:
        new = copy.deepcopy(node.state)
        i = a[0][0]
        j = a[0][1]
        m = []
            
        if a[1] <= 3: #captures
            cont = 1

            if a[1] == 0:
                y = i + 2
                x = j - 2
                new[y][x] = p_
                new[i][j] = ' '
                new[i + 1][j - 1] = ' '
                m.append( [[i, j], [y, x]] )

            if a[1] == 1:
                y = i + 2
                x = j + 2
                new[y][x] = p_
                new[i][j] = ' '
                new[i + 1][j + 1] = ' '
                m.append( [[i, j], [y, x]] )

            if a[1] == 2:
                y = i - 2
                x = j - 2
                new[y][x] = p_
                new[i][j] = ' '
                new[i - 1][j - 1] = ' '
                m.append( [[i, j], [y, x]])

            if a[1] == 3:
                y = i - 2
                x = j + 2
                new[y][x] = p_
                new[i][j] = ' '
                new[i - 1][j + 1] = ' '
                m.append( [[i, j], [y, x]])
                

            while cont: #check for further jumps
                cont = 0
                i = y
                j = x

                if node.state[y][x] == 'b' or node.state[y][x] == 'B' or node.state[y][x] == 'R':    
                    #sw
                    if i + 1 < 8 and j - 1 >= 0:
                        y = i + 1
                        x = j - 1
                        if node.state[y][x].lower() == o_:
                            if y + 1 < 8 and x - 1 >= 0:
                                y = y + 1
                                x = x - 1
                                if node.state[y][x] == ' ':
                                    new[y][x] = new[i][j]
                                    new[i + 1][j - 1] = ' '
                                    new[i][j] = ' '
                                    m.append([[i, j], [y, x]])
                                    
                                    cont = 1
                                    continue
                    
                    #se
                    if i + 1 < 8 and j + 1 < 8:
                        y = i + 1
                        x = j + 1
                        if node.state[y][x].lower() == o_:
                            if y + 1 < 8 and x + 1 < 8:
                                y = y + 1
                                x = x - 1
                                if node.state[y][x] == ' ':
                                    new[y][x] = new[i][j]
                                    new[i + 1][j + 1] = ' '
                                    new[i][j] = ' '
                                    m.append([[i, j], [y, x]])
                                    
                                    cont = 1
                                    continue
                                
                if node.state[y][x] == 'r' or node.state[y][x] == 'R' or node.state[y][x] == 'B':
                    #nw
                    if i - 1 >= 0 and j - 1 >= 0:
                        y = i - 1
                        x = j - 1
                        if node.state[y][x].lower() == o_:
                            if y - 1 >= 0 and x - 1 >= 0:
                                y = y - 1
                                x = x - 1
                                if node.state[y][x] == ' ':
                                    new[y][x] = new[i][j]
                                    new[i - 1][j - 1] = ' '
                                    new[i][j] = ' '
                                    m.append([[i, j], [y, x]])
                                    
                                    cont = 1
                                    continue
                    
                    #ne
                    if i - 1 >= 0 and j + 1 < 8:
                        y = i - 1
                        x = j + 1
                        if node.state[y][x].lower() == o_:
                            if y - 1 >= 0 and x + 1 < 8:
                                y = y - 1
                                x = x + 1
                                if node.state[y][x] == ' ':
                                    new[y][x] = new[i][j]
                                    new[i - 1][j + 1] = ' '
                                    new[i][j] = ' '
                                    m.append([[i, j], [y, x]])
                                    
                                    cont = 1
                                    continue
                
            
              
            n.append( Node(node, v, m, node.depth + 1, new) )
        else: #normal movements            
            

            if a[1] == 4:
                y = i + 1
                x = j - 1
                new[y][x] = p_
                new[i][j] = ' '
                m = [[i, j], [y, x]]

            if a[1] == 5:
                y = i + 1
                x = j + 1
                new[y][x] = p_
                new[i][j] = ' '
                m = [[i, j], [y, x]]

            if a[1] == 6:
                y = i - 1
                x = j - 1
                new[y][x] = p_
                new[i][j] = ' '
                m = [[i, j], [y, x]]

            if a[1] == 7:
                y = i - 1
                x = j + 1
                new[y][x] = p_
                new[i][j] = ' '
                m = [[i, j], [y, x]]


            n.append( Node(node, v, m, node.depth + 1, new) )

            



    
    if op == 'max':
        for n_ in n:
            
            minimax('min', n_)

            if (len(n_.children) > 0 and n_.depth < max_d) or n_.depth == max_d:
                if n_.value > node.value:
                    node.value = copy.copy(n_.value)



                node.children.append(n_)
                nodecnt += 1

                
                
            



    if op == 'min':
        for n_ in n:
            
            minimax('max', n_)

            if (len(n_.children) > 0 and n_.depth < max_d) or n_.depth == max_d:
                if n_.value < node.value:
                    node.value = copy.copy(n_.value)



                node.children.append(n_)
                nodecnt += 1

      
    
    return