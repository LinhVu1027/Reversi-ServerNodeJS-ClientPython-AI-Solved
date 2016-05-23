#!/usr/bin/env python2
from copy import deepcopy
from socketIO_client import SocketIO

my_board = []

socketIO = None


def updateBoard(data):
    """ Server inform me that board has been updated
    """
    global my_board
    my_board = data['board']
    print "**************************************"
    print '\n'.join([str(row) for row in my_board])
    print "**************************************"
    print data['message']
    

# check at postion(row, col) is a enemy of player
def oppose(player, row, col):
    foe = 2 if player == 1 else 1
    return my_board[row][col] == foe

# defaul player is 1 and enemy is 2
def checkGo(row, col, player):
    x = row
    y = col

    if my_board[x][y] != -1:
        return False
    state = {}

    # Check left of this position
    if y > 1 and oppose(player, x, y - 1):
        surround = False
        for j in range(y - 2, -1, -1):     
            if my_board[x][j] == -1:
                break
            if my_board[x][j] == player:
                surround = True
                break
        if surround:
            # Can go this position to eat left enemy
            state['left'] = True

    # Check right of this position
    if y < 6 and oppose(player, x, y + 1):
        surround = False
        for j in range(y + 2, 8):     
            if my_board[x][j] == -1:
                break
            if my_board[x][j] == player:
                surround = True
                break
        if surround:
            # Can go this position to eat right enemy
            state['right'] = True

    # Check up of this position
    if x > 1 and oppose(player, x - 1, y):
        surround = False
        for i in range(x - 2, -1, -1):     
            if my_board[i][y] == -1:
                break
            if my_board[i][y] == player:
                surround = True
                break
        if surround:
            # Can go this position to eat up enemy
            state['up'] = True

    # Check down of this position
    if x < 6 and oppose(player, x + 1, y):
        surround = False
        for i in range(x + 2, 8):     
            if my_board[i][y] == -1:
                break
            if my_board[i][y] == player:
                surround = True
                break
        if surround:
            # Can go this position to eat down enemy
            state['down'] = True

    # Check up left of this position
    if x > 1 and y > 1 and oppose(player, x - 1, y - 1):
        surround = False
        i, j = x - 2, y - 2
        while i > -1 and j > -1:
            if my_board[i][j] == -1:
                break
            if my_board[i][j] == player:
                surround = True
                break
            i -= 1
            j -= 1
        if surround:
            # Can go this position to eat up left enemy
            state['upleft'] = True

    # Check up right of this position
    if x > 1 and y < 6 and oppose(player, x - 1, y + 1):
        surround = False
        i, j = x - 2, y + 2
        while i > -1 and j < 8:
            if my_board[i][j] == -1:
                break
            if my_board[i][j] == player:
                surround = True
                break
            i -= 1
            j += 1
        if surround:
            # Can go this position to eat up right enemy
            state['upright'] = True

    # Check down right of this position
    if x < 6 and y < 6 and oppose(player, x + 1, y + 1):
        surround = False
        i, j = x + 2, y + 2
        while i < 8 and j < 8:
            if my_board[i][j] == -1:
                break
            if my_board[i][j] == player:
                surround = True
                break
            i += 1
            j += 1
        if surround:
            # Can go this position to eat down right enemy
            state['downright'] = True

    # Check down left of this position
    if x < 6 and y > 1 and oppose(player, x + 1, y - 1):
        surround = False
        i, j = x + 2, y - 2
        while i < 8 and j > -1:
            if my_board[i][j] == -1:
                break
            if my_board[i][j] == player:
                surround = True
                break
            i += 1
            j -= 1
        if surround:
            # Can go this position to eat down left enemy
            state['downleft'] = True


    return state

def go(row, col, player):
    global my_board
    x = row
    y = col
    status = checkGo(x, y, player)

    if not status:
        return False

    can_go = False

    if status['left']:
        can_go = True
        j = y - 1
        while my_board[x][j] != player and j > -1:
            my_board[x][j] = player
            j -= 1

    if status['right']:
        can_go = True
        j = y + 1
        while my_board[x][j] != player and j < 8:
            my_board[x][j] = player
            j += 1

    if status['up']:
        can_go = True
        i = x - 1
        while my_board[i][y] != player and i > -1:
            my_board[i][y] = player
            i -= 1

    if status['down']:
        can_go = True
        i = x + 1
        while my_board[i][y] != player and i < 8:
            my_board[i][y] = player;
            i += 1

    if status['upleft']:
        can_go = True
        i = x - 1
        j = y - 1
        while my_board[i][j] != player and i > -1 and j > -1:
            my_board[i][j] = player
            i -= 1
            j -= 1

    if status['upright']:
        can_go = True
        i = x - 1
        j = y + 1
        while my_board[i][j] != player and i > -1 and j < 8:
            my_board[i][j] = player
            i -= 1
            j += 1

    if status['downright']:
        can_go = True
        i = x + 1
        j = y + 1
        while my_board[i][j] != player and i < 8 and j < 8:
            my_board[i][j] = player
            i += 1
            j += 1

    if status['downleft']:
        can_go = True
        i = x + 1
        j = y - 1
        while my_board[i][j] != player and i < 8 and j > -1:
            my_board[i][j] = player
            i += 1
            j -= 1

    if can_go:
        my_board[x][y] = player

def makeAMove(data):
    """ Send to server my move
    """
    global my_board
    my_board = data['board']
    #my_board = board[:]
    print "**************************************"
    print '\n'.join([str(row) for row in my_board])
    print "**************************************"
    print(data['message'])

    move = []
    for i in range(0,8):
        for j in range(0,8):
            if checkGo(i, j):
                move.append((i,j))

    print move


    moveX = int(raw_input('X'))
    moveY = int(raw_input('Y'))
    my_move = {'X': moveX, 'Y': moveY}
    #my_move = makeACallTo('DeepMind', 'Show me the next move!')
    #my_move = {'X': 5, 'Y': 2}

    socketIO.emit('mymove', {'rowIdx': my_move['X'], 'colIdx': my_move['Y']})

def end(data):
    """ Game is over!
    """
    print('Game is over !')
    print('Winner is: ' + data['winner'])
    print('Player 1 number: ' + data['player1'])
    print('Player 2 number: ' + data['player2'])

def print_error(data):
    print('Error: ' + data)


token = raw_input('Enter your token: ')

socketIO = SocketIO('localhost', 8100, params={'token': token})

# Define callback to updated event
socketIO.on('updated', updateBoard)

# Define callback to yourturn event
socketIO.on('yourturn', makeAMove)

# Define callback to end event
socketIO.on('end', end)

# Define callback to errormessage event
socketIO.on('errormessage', print_error)

socketIO.wait()
