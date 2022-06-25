class Board: 
	def __init__(self, m, n, k):
		self.rows = m 
		self.columns = n
		# initialize empty gameboard 
		self.gameboard = [[' ']*m for _ in range(n)]

	def update_board(self, move, character):
		self.gameboard[move[0]][move[1]] = character
 

	# only works for two players right now 
	def display_board(self):
		for i in range(self.rows):
			for j in range(self.columns):
				if self.gameboard[i][j] == 'X':
					tile = 'X'
				elif self.gameboard[i][j] == 'O':
					tile = 'O'
				else:
					tile = ' '
				print("|", tile, " |", sep ='', end ='')
			print('\n', end='')

