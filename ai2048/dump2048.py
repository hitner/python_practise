import random
import copy
mark_over = -0x5FFFFFFF
class L2CannotAppend(Exception):
    pass
class L2NotClosedProbability(Exception):
    pass
class L2CannotMove(Exception):
    pass

def l2merge(board,direction):
    size = len(board)
    mlist = []
    for i in range(size):
        for j in range(size-1):#the last always do not need to handle
            (x,y) = reflect((i,j),size,direction)
            (x1,y1) = reflect((i,j+1),size,direction)
            if board[x][y] == board[x1][y1] and not board[x][y] == 0:
                mlist.append(board[x][y])
                board[x][y] *= 2
                board[x1][y1] = 0
    return mlist

def reflect(loc,size,direction):
    if direction == 'up':
        return (loc[1],loc[0])
    if direction == 'down':
        return (size - 1 - loc[1], loc[0])
    if direction == 'left':
        return (loc[0],loc[1])
    if direction == 'right':
        return (loc[0], size-1-loc[1])

def l2move(board,direction):
    size = len(board)
    for i in range(size):
        alist = []
        for j in range(size):
            (x,y) = reflect((i,j),size,direction)
            if board[x][y] != 0:
                alist.append(board[x][y])
        #modify
        alist += [0 for j in range(size-len(alist))]
        for j in range(size):
            (x,y) = reflect((i,j),size,direction)
            board[x][y] = alist[j]
                                     
def l2randomAppend(board, value):
    size = len(board)
    emptyLoc = []
    for i in range(size):
        for j  in range(size):
            if board[i][j] == 0:
                emptyLoc.append([i,j])

    if len(emptyLoc) == 0:
        raise L2CannotAppend

    loc = random.randint(0,len(emptyLoc) - 1)
    x = emptyLoc[loc][0]
    y = emptyLoc[loc][1]
    board[x][y] = value

def l2randomCreate(candidate, probality):
    check = 0.0
    for pro in probality:
        check = check + pro
    if not check == 1:
        raise L2NotClosedProbability
    x = random.uniform(0,1)
    cumulate = 0.0
    for cand,pro in zip(candidate,probality):
        cumulate += pro
        if x <= cumulate:
            break
    return cand

def l2isSame(b1,b2):
    size = len(b1)
    for i in range(size):
        for j in range(size):
            if not b1[i][j] == b2[i][j]:
                return False
    return True 

def l2getMax(board):
    listmax = [ max(i) for i in board]
    return max(listmax)
#utility-----------------------------------
def l2():
    return l2randomCreate([2,4], [0.5,0.5])
def l2print(board):
    #print('--------------------')
    for row in board:
        rowstr = ''
        for item in row:
            if item == 0:
                rowstr = rowstr + '.\t'
            else:
                rowstr = rowstr + str(item) + '\t'
        print(rowstr)

def l2do(board,act):
    l2move(board, act)
    l2merge(board, act)
    l2move(board, act)
    l2randomAppend(board, l2())
    l2print(board)

def main():
    #only debug
    #debug_b = [[256,128,64,32],
    #    [64,16,4,4],
    #    [8,4,2,2],
    #    [4,0,0,2]]
    #act = l2ai_template(debug_b,ai_s_neighbor)

    print('Hello World')
    board = [[0] * 4  for i in range(4)]
    l2randomAppend(board, l2())
    l2randomAppend(board, l2())
    l2print(board)
    act = l2ai_template(board,ai_s_neighbor)
    while not act == 'over':
        print(act)
        l2do(board, act)
        act = l2ai_template(board,ai_s_neighbor)
        

def l2ai_template(board, ai):
    result = []
    action = ['up','left','right','down'] 
    for act in action:
        result.append(ai(board,act))
    m = max(result)
    print('max weight value:%d' %m)
    if m == mark_over:
        return 'over'
    else:
        return action[result.index(m)]
#AI-----------------------------------

#
def ai_s_neighbor(b,action, l2flag = True):
    board = copy.deepcopy(b)
    l2move(board,action)
    l2merge(board,action)
    l2move(board,action)
    if l2isSame(board,b):
        return mark_over
    result = 0.0
    size = len(board)
    maxone = l2getMax(board)
    edge_board = getEdgeBorad(size,maxone)
    left2right = False
    for i in range(size):
        left2right = not left2right
        for k in range(size):
            if left2right:
                j = k
            else:
                j = size-1-k
            if board[i][j] > preOneInSRoute(board,i,j):
                return result
            else:
                result += board[i][j] * edge_board[i][j]
    if l2flag:
        l2result = ai_s_neighbor_l2(board)
    else:
        return result
    if l2result > result:
        print('in level 2.')
        return l2result
    else:
        return result

def ai_s_neighbor_l2(board):
    result = []
    action = ['up','left','right','down'] 
    for act in action:
        result.append(ai_s_neighbor(board,act, False))
    return max(result)

#
def ai_neighbor(b,action):
    board = copy.deepcopy(b)
    l2move(board,action)
    l2merge(board,action)
    l2move(board,action)
    if l2isSame(board,b):
        return mark_over

    result = 0.0
    size = len(board)
    maxone = l2getMax(board)
    edge_board = getEdgeBorad(size,maxone)
    for i in range(size):
        for j in range(size):
            result += neighbor_w2(board,[i,j],edge_board)
    return result
def neighbor_weight(board,loc,edge_board):
    x = loc[0]
    y = loc[1]
    if board[x][y] == 0:
        return 0
    neighbors = getNeighbors(board,loc,edge_board)
    neighbors.sort(reverse=True)
    result = 0.0
    for i in range(2):
        if neighbors[i] >= board[x][y]:
            result += (board[x][y]/neighbors[0])
        #else:
        #    result += (neighbors[i]/board[x][y])
    #result = result/2
    result += 1
    return result*board[x][y]

def neighbor_w2(board, loc, edge_board):
    x = loc[0]
    y = loc[1]
    if edge_board[x][y] == 0:
        return 0

    preOne = preOneInSRoute(board,x,y)
    if board[x][y] > preOne:
        return - board[x][y] * edge_board[x][y]
    else:
        return board[x][y] * edge_board[x][y]

def getEdgeBorad(size, maxone):
    newb = [[0] * size  for i in range(size)]
    reverse = True
    for i in range(size):
        reverse = not reverse
        for j in range(size):
            if maxone == 1:
                return newb
            else:
                if reverse:
                    newb[i][size-1-j] = maxone
                else:
                    newb[i][j] = maxone
                maxone = maxone/2
    return newb
def getNeighbors(board,loc,edge_board):
    neighbors = []
    size = len(board)
    x,y = loc[0],loc[1]
    #left
    if x == 0:
        neighbors.append(edge_board[x][y])
    else:
        neighbors.append(board[x-1][y])
    #up
    if y == 0:
        neighbors.append(edge_board[x][y])
    else:
        neighbors.append(board[x][y-1])
    #right
    if y == size -1:
        neighbors.append(edge_board[x][y])
    else:
        neighbors.append(board[x][y+1])
    #down
    if x == size -1:
        neighbors.append(edge_board[x][y])
    else:
        neighbors.append(board[x+1][y])
    return neighbors

def preOneInSRoute(board,x,y):
    size = len(board)
    if x == 0 and y == 0:
        return 2**(size*size +1)

    if x%2 == 1:
        if y == size-1:
            return board[x-1][y]
        else:
            return board[x][y+1]
    else:
        if y == 0:
            return board[x-1][0]
        else:
            return board[x][y-1]

# another ==========================
def ai_max_sum(board,action):#
    result = []
    for act in action:
        b = copy.deepcopy(board)
        l2move(b,act)
        mlist = l2merge(b,act)
        if len(mlist) == 0:#none one merged,we are going to judge it can allowed?
            if l2isSame(board,b):
                result.append(-1)
            else:
                result.append(0)
        else:
            result.append(sum(mlist))
    m = max(result)
    print('max sum value:%d' %m)
    if m == -1:
        return 'over'
    else:
        return action[result.index(m)]

def ai_max_count(board,action):
    result = []
    for act in action:
        b = copy.deepcopy(board)
        l2move(b,act)
        mlist = l2merge(b,act)
        if len(mlist) == 0:#none one merged,we are going to judge it can allowed?
            if l2isSame(board,b):
                result.append(-1)
            else:
                result.append(0)
        else:
            result.append(len(mlist))
    m = max(result)
    print('max sum count:%d' %m)
    if m == -1:
        return 'over'
    else:
        return action[result.index(m)]


def ai_max_item(board,action):
    result = []
    for act in action:
        b = copy.deepcopy(board)
        l2move(b,act)
        mlist = l2merge(b,act)
        if len(mlist) == 0:#none one merged,we are going to judge it can allowed?
            if l2isSame(board,b):
                result.append(-1)
            else:
                result.append(0)
        else:
            result.append(max(mlist))
    m = max(result)
    print('max sum item:%d' %m)
    if m == -1:
        return 'over'
    else:
        return action[result.index(m)]


# ai_point

 # for input in commandline
gb = [[0] * 4  for i in range(4)]
def a():
    l2randomAppend(gb, l2())
    l2print(gb)
def u():
    l2move(gb, 'up')
    l2merge(gb, 'up')
    l2move(gb, 'up')
    l2randomAppend(gb, l2())
    l2print(gb)
def d():
    l2move(gb, 'down')
    l2merge(gb, 'down')
    l2move(gb, 'down')
    l2randomAppend(gb, l2())
    l2print(gb)
def l():
    l2move(gb, 'left')
    l2merge(gb, 'left')
    l2move(gb, 'left')
    l2randomAppend(gb, l2())
    l2print(gb)
def r():
    l2move(gb, 'right')
    l2merge(gb, 'right')
    l2move(gb, 'right')
    l2randomAppend(gb, l2())
    l2print(gb)


if __name__ == '__main__':
    main()