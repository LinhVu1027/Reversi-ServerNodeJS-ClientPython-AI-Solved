from socketIO_client import SocketIO, BaseNamespace
from copy import deepcopy

class Reversi:
	def __init__(self, board=None, player=None):
		if not board:
			self.board = []
		else:
			self.board = board
			self.__updateValueBoard()
		if player:
			self.player = player

	def __initValueBoard(self):
		self.valueBoardFor1 = \
			[[48,   6,  6,  6,  6,  6,   6, 48],
			 [ 6, -24, -4, -4, -4,- 4, -24,  6],
			 [ 6,  -4,  1,  1,  1,  1,  -4,  6],
			 [ 6,  -4,  1,  1,  1,  1,  -4,  6],
			 [ 6,  -4,  1,  1,  1,  1,  -4,  6],
			 [ 6,  -4,  1,  1,  1,  1,  -4,  6],
			 [ 6, -24, -4, -4, -4,- 4, -24,  6],
			 [48,   6,  6,  6,  6,  6,   6, 48]]
		self.valueBoardFor2 = deepcopy(self.valueBoardFor1)

	def __update4Corners(self):
		# up left corner: HUMAN(2) ticks
		if self.board[0][0] == 2:
			if self.board[0][2] in [-1, 1]: self.valueBoardFor1[0][1] = -4
			if self.board[2][0] in [-1, 1]: self.valueBoardFor1[1][0] = -4
			self.valueBoardFor1[1][1] = -4
			self.valueBoardFor2[1][1] = 3
		# up right corner: HUMAN(2) ticks
		if self.board[0][7] == 2:
			if self.board[0][5] in [-1, 1]: self.valueBoardFor1[0][6] = -4
			if self.board[2][7] in [-1, 1]: self.valueBoardFor1[1][7] = -4
			self.valueBoardFor1[1][6] = -4
			self.valueBoardFor2[1][6] = 3
		# down left corner: HUMAN(2) ticks
		if self.board[7][0] == 2:
			if self.board[5][0] in [-1, 1]: self.valueBoardFor1[6][0] = -4
			if self.board[7][2] in [-1, 1]: self.valueBoardFor1[7][1] = -4
			self.valueBoardFor1[6][1] = -4
			self.valueBoardFor2[6][1] = 3
		# down right corner: HUMAN(2) ticks
		if self.board[7][7] == 2:
			if self.board[7][5] in [-1, 1]: self.valueBoardFor1[7][6] = -4
			if self.board[5][7] in [-1, 1]: self.valueBoardFor1[6][7] = -4
			self.valueBoardFor1[6][6] = -4
			self.valueBoardFor2[6][6] = 3

		#---------------------------------------------------------------

		# up left corner: AI(1) ticks
		if self.board[0][0] == 1:
			if self.board[0][2] in [-1, 2]: self.valueBoardFor2[0][1] = -4
			if self.board[2][0] in [-1, 2]: self.valueBoardFor2[1][0] = -4
			self.valueBoardFor2[1][1] = -4
			self.valueBoardFor1[1][1] = 3
		# up right corner: AI(1) ticks
		if self.board[0][7] == 2:
			if self.board[0][5] in [-1, 2]: self.valueBoardFor2[0][6] = -4
			if self.board[2][7] in [-1, 2]: self.valueBoardFor2[1][7] = -4
			self.valueBoardFor2[1][6] = -4
			self.valueBoardFor1[1][6] = 3
		# down left corner: AI(1) ticks
		if self.board[7][0] == 2:
			if self.board[5][0] in [-1, 2]: self.valueBoardFor2[6][0] = -4
			if self.board[7][2] in [-1, 2]: self.valueBoardFor2[7][1] = -4
			self.valueBoardFor2[6][1] = -4
			self.valueBoardFor1[6][1] = 3
		# down right corner: AI(1) ticks
		if self.board[7][7] == 2:
			if self.board[7][5] in [-1, 2]: self.valueBoardFor2[7][6] = -4
			if self.board[5][7] in [-1, 2]: self.valueBoardFor2[6][7] = -4
			self.valueBoardFor2[6][6] = -4
			self.valueBoardFor1[6][6] = 3

		#------------------------------------------------------------------

	def __update4Edges(self):
		for n in range(2, 6):
			# up edge: HUMAN(2) ticks
			if self.board[0][n] == 2:
				self.valueBoardFor1[1][n] = -1
				self.valueBoardFor2[1][n] = 2
			# down edge: HUMAN(2) ticks
			if self.board[7][n] == 2:
				self.valueBoardFor1[6][n] = -1
				self.valueBoardFor2[6][n] = 2
			# left edge: HUMAN(2) ticks
			if self.board[n][0] == 2:
				self.valueBoardFor1[n][1] = -1
				self.valueBoardFor2[n][1] = 2
			# right edge: HUMAN(2) ticks
			if self.board[n][7] == 2:
				self.valueBoardFor1[n][6] = -1
				self.valueBoardFor2[n][6] = 2

			#-------------------------------

			# up edge: AI(1) ticks
			if self.board[0][n] == 1:
				self.valueBoardFor1[1][n] = 2
				self.valueBoardFor2[1][n] = -1
			# down edge: AI(1) ticks
			if self.board[7][n] == 1:
				self.valueBoardFor1[6][n] = 2
				self.valueBoardFor2[6][n] = -1
			# left edge: AI(1) ticks
			if self.board[n][0] == 1:
				self.valueBoardFor1[n][1] = 2
				self.valueBoardFor2[n][1] = -1
			# right edge: AI(1) ticks
			if self.board[n][7] == 1:
				self.valueBoardFor1[n][6] = 2
				self.valueBoardFor2[n][6] = -1

			#--------------------------------

	def __updateValueBoard(self):
		self.__initValueBoard()
		self.__update4Corners()
		self.__update4Edges()


	def updateBoard(self, board, player):
		self.board = board
		self.player = player
		self.__updateValueBoard()
		print "-----------------------------------"
		print '\n'.join([str(row) for row in self.board])
		print "-----------------------------------"

	# Check is at (rowm col) is enemy of player
	def __oppose(self, row, col):
		enemy = 2 if self.player == 1 else 1
		return self.board[row][col] == enemy

	# Check player put down at (row, col) is valid
	def __validMove(self, row, col):
		if self.board[row][col] != -1:
			return False

		direct = {}

		# Check left of this position
		if col > 1 and self.__oppose(row, col - 1):
			surround = False
			for j in range(col - 2, -1, -1):     
				if self.board[row][j] == -1:
					break
				if self.board[row][j] == self.player:
					surround = True
					break
			if surround:
				# Can go this position to eat left enemy
				direct['left'] = True

	    # Check right of this position
		if col < 6 and self.__oppose(row, col + 1):
			surround = False
			for j in range(col + 2, 8):     
				if self.board[row][j] == -1:
					break
				if self.board[row][j] == self.player:
					surround = True
					break
			if surround:
	            # Can go this position to eat right enemy
				direct['right'] = True

	    # Check up of this position
		if row > 1 and self.__oppose(row - 1, col):
			surround = False
			for i in range(row - 2, -1, -1):     
				if self.board[i][col] == -1:
					break
				if self.board[i][col] == self.player:
					surround = True
					break
			if surround:
	            # Can go this position to eat up enemy
				direct['up'] = True

	    # Check down of this position
		if row < 6 and self.__oppose(row + 1, col):
			surround = False
			for i in range(row + 2, 8):     
				if self.board[i][col] == -1:
					break
				if self.board[i][col] == self.player:
					surround = True
					break
			if surround:
	            # Can go this position to eat down enemy
				direct['down'] = True

	    # Check up left of this position
		if row > 1 and col > 1 and self.__oppose(row - 1, col - 1):
			surround = False
			i, j = row - 2, col - 2
			while i > -1 and j > -1:
				if self.board[i][j] == -1:
					break
				if self.board[i][j] == self.player:
					surround = True
					break
				i -= 1
				j -= 1
			if surround:
	            # Can go this position to eat up left enemy
				direct['upleft'] = True

	    # Check up right of this position
		if row > 1 and col < 6 and self.__oppose(row - 1, col + 1):
			surround = False
			i, j = row - 2, col + 2
			while i > -1 and j < 8:
				if self.board[i][j] == -1:
					break
				if self.board[i][j] == self.player:
					surround = True
					break
				i -= 1
				j += 1
			if surround:
	            # Can go this position to eat up right enemy
				direct['upright'] = True

	    # Check down right of this position
		if row < 6 and col < 6 and self.__oppose(row + 1, col + 1):
			surround = False
			i, j = row + 2, col + 2
			while i < 8 and j < 8:
				if self.board[i][j] == -1:
					break
				if self.board[i][j] == self.player:
					surround = True
					break
				i += 1
				j += 1
			if surround:
	            # Can go this position to eat down right enemy
				direct['downright'] = True

	    # Check down left of this position
		if row < 6 and col > 1 and self.__oppose(row + 1, col - 1):
			surround = False
			i, j = row + 2, col - 2
			while i < 8 and j > -1:
				if self.board[i][j] == -1:
					break
				if self.board[i][j] == self.player:
					surround = True
					break
				i += 1
				j -= 1
			if surround:
	            # Can go this position to eat down left enemy
				direct['downleft'] = True

		return direct

	# Return all valid move for player
	def getValidMoves(self):
		moves = []
		for i in range(0, 8):
			for j in range(0, 8):
				if self.__validMove(i, j):
					moves.append((i, j))
		return moves

	# Cannot continue for player
	def isLeaf(self):
		return [] == self.getValidMoves()

	# Return a Reversi instance after do a move at (row, col)
	def doMove(self, row, col):
		board = deepcopy(self.board)
		direct = self.__validMove(row, col)

		if not direct:
			return False

		if 'left' in direct:
			j = col - 1
			while board[row][j] != self.player and j > -1:
				board[row][j] = self.player
				j -= 1

		if 'right' in direct:
			j = col + 1
			while board[row][j] != self.player and j < 8:
				board[row][j] = self.player
				j += 1

		if 'up' in direct:
			i = row - 1
			while board[i][col] != self.player and i > -1:
				board[i][col] = self.player
				i -= 1

		if 'down' in direct:
			i = row + 1
			while board[i][col] != self.player and i < 8:
				board[i][col] = self.player
				i += 1

		if 'upleft' in direct:
			i = row - 1
			j = col - 1
			while board[i][j] != self.player and i > -1 and j > -1:
				board[i][j] = self.player
				i -= 1
				j -= 1

		if 'upright' in direct:
			i = row - 1
			j = col + 1
			while board[i][j] != self.player and i > -1 and j < 8:
				board[i][j] = self.player
				i -= 1
				j += 1

		if 'downright' in direct:
			i = row + 1
			j = col + 1
			while board[i][j] != self.player and i < 8 and j < 8:
				board[i][j] = self.player
				i += 1
				j += 1

		if 'downleft' in direct:
			i = row + 1
			j = col - 1
			while board[i][j] != self.player and i < 8 and j > -1:
				board[i][j] = self.player
				i += 1
				j -= 1

		board[row][col] = self.player

		#print "-----------------TADA------------------"
		#print '\n'.join([str(row) for row in board])
		#print "-----------------TADA------------------"

		oppent = 2 if self.player == 1 else 1

		return Reversi(board, oppent)

	# High score is self.player better
	def heuristicScore(self):
		score = 0
		for i in range(0, 8):
			for j in range(0, 8):
				if self.board[i][j] == 1:
					score += 1
				if self.board[j][j] == 2:
					score -= 1
		return score

	def judgeBoardValue(self):
		ai1Score = 0
		ai2Score = 0
		for i in range(0, 8):
			for j in range(0, 8):
				if self.board[i][j] == 1:
					ai1Score += self.valueBoardFor1[i][j]
				if self.board[i][j] == 2:
					ai2Score += self.valueBoardFor2[i][j]
		return ai1Score - ai2Score

class ReversiNamespace(BaseNamespace):
	global play_reversi

	def on_updated(self, data):
		""" Response to updated event
		"""
		print('updated triggered')
		board = data['board']
		player = data['player']
		play_reversi.updateBoard(board, player)

	def on_yourturn(self, data):
		""" Response to yourturn event
		"""
		print('yourturn triggered')
		board = data['board']
		player = data['player']
		play_reversi.updateBoard(board, player)
		if player == 1:
			value, move = alphabeta(play_reversi, 4, -10000, 10000, True)
		elif player == 2:
			value, move = alphabeta(play_reversi, 4, -10000, 10000, False)
		#value, move = minimax(play_reversi, 6, True)
		print "My player: ", player
		print "My move: ", move


		self.emit('mymove', {'rowIdx': move[0], 'colIdx': move[1]})

	def on_errormessage(self, data):
		""" Response to errormessage event
		"""
		print(data)

	def on_end(self, data):
		""" Response to end event
		"""
		print('The winner is ' + str(data['winner']))
		print('P1 count: ' + str(data['player1']))
		print('P2 count: ' + str(data['player2']))

play_reversi = Reversi()

def minimax(node, depth, maxPlayer):
	if depth == 0 or node.isLeaf():
		return (node.judgeBoardValue(), None)

	bestMove = None

	if maxPlayer:
		bestValue = -10000
		for move in node.getValidMoves():
			childNode = node.doMove(move[0], move[1])
			newValue, newMove = minimax(childNode, depth - 1, False)
			if newValue > bestValue:
				bestValue = newValue
				bestMove = move
		return bestValue, bestMove
	else:
		bestValue = 10000
		for move in node.getValidMoves():
			childNode = node.doMove(move[0], move[1])
			newValue, newMove = minimax(childNode, depth - 1, True)
			if newValue < bestValue:
				bestValue = newValue
				bestMove = move
		return bestValue, bestMove

def alphabeta(node, depth, a, b, maxPlayer):
	if depth == 0 or node.isLeaf():
		return (node.judgeBoardValue(), None)

	bestMove = None

	if maxPlayer:
		bestValue = -10000
		for move in node.getValidMoves():
			childNode = node.doMove(move[0], move[1])
			newValue, newMove = alphabeta(childNode, depth - 1, a, b, False)
			if newValue > a:
				a = newValue
				bestMove = move
			if newValue > bestValue:
				bestValue = newValue
			if a >= b: break
		return bestValue, bestMove
	else:
		bestValue = 10000
		for move in node.getValidMoves():
			childNode = node.doMove(move[0], move[1])
			newValue, newMove = alphabeta(childNode, depth - 1, a, b, True)
			if newValue < b:
				b = newValue
				bestMove = move
			if newValue < bestValue:
				bestValue = newValue
			if a >= b: break
		return bestValue, bestMove


token = raw_input('Enter your token: ')

# Use socketio with defined Namespace
socketIO = SocketIO('localhost', 8100, ReversiNamespace, params={'token': token})

socketIO.wait()
