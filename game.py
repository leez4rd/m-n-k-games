from player import Player
from board import Board 

class Game:

	def __init__(self, rows, columns, k, *args):

		SYMBOLS = ['X', 'O', 'Z'] # and so on-- will make these colored pebbles once I have GUI
		self.m = rows
		self.n = columns
		self.victory_length = k
		self.gameboard = Board(rows, columns, k)
		self.moves = {}

		# list of names
		self.number_of_players = len(args)
		self.names = [args[i] for i in range(len(args))]
		self.player_dict = {}
		self.turn_count = 0 # keep track of turn number for player cycle 

		if (len(args) == 0):
			# default to two player 
			self.player_dict['P1'] = Player('Mario', 'X')
			self.player_dict['P2'] = Player('Luigi', 'O')
		else:
			# initialize players with names 
			for i, name in enumerate(self.names):
				pnum = 'P' + str(i + 1) 
				self.player_dict[pnum] = Player(name, SYMBOLS[i])

		self.current_player = self.player_dict['P1'] 

	def run_game(self):
		game_over = False 

		while not game_over:
			# ask current player for a move 
			self.gameboard.display_board()
			move = list(map(int, input("Enter a set of coordinates separated by a comma: ").split(',')))

			if self.gameboard.gameboard[move[0]][move[1]] == ' ':
				self.current_player.record_move(move)
				self.gameboard.update_board(move, self.current_player.char)
				if self.find_wins():
					game_over = True 
					winner = self.current_player
				elif self.turn_count == self.m * self.n - 1:  # if the board is full, the game is over 
					game_over = True 
					winner = None 

				# efficiency note: this should only check after min possible # of turns for win 
				# additionally, we should track the number of k-1 rows (ie "almost wins" or rows of 4 in gomoku) to optimize runtime
				# however, premature optimization is the root of all evil, so just gonna get everything working first
				
				print(self.current_player.name)
				self.next_turn() # need a way to update player 

			else:
				print("That space already contains a pebble") # don't change player, just return to loop

		if winner == None:
			print("It's a tie")
		else:
			print("The winner is ", winner.name)
			self.gameboard.display_board()
			# needs feature: erase board in case player wants a rematch...


	def next_turn(self):
		self.turn_count += 1 # increment the turn count 
		self.current_player = self.player_dict['P' + str(self.turn_count % self.number_of_players + 1)]
		# how do we change players when the list of variable names for players is created dynamically?
		# can we create a dynamic dictionary as well or instead? 	
		# get key for value of current player, then add 1 to integer part of key to get new key
		return 


	def find_wins(self):
		if self.diagonals() or self.rows() or self.columns():
			return True
		else:
			return False

	# suboptimal to do this loop every time, might combine these functions -- risks negating clarity of separate win checkers though
	

	# assuming each player has a list of moves that they have made 
	def rows(self): # pass a Player object, or rely on internal referencing from game 
		
		if len(self.current_player.moves) < self.victory_length:
			return False 
		# much better algorithm, but probably still not optimal since we are not using information from last check 
		mvs = sorted(self.current_player.moves)
		count = 1
		for i in range(len(mvs) - 1):
			if mvs[i][1] + 1 == mvs[i + 1][1]:
				if mvs[i][0] == mvs[i + 1][0]:
					count += 1
					if count >= self.victory_length:
						return True 
				else:
					count = 0 
			else:
				count = 0
		return False 



	def columns(self):

		# check if win possible (redundant if we do this before entering function)
		if len(self.current_player.moves) < self.victory_length:
			return False 

		# probably not optimal since we are not using information from last check 
		mvs = sorted(self.current_player.moves)
		count = 1
		for i in range(len(mvs) - 1):
			if mvs[i][0] + 1 == mvs[i + 1][0]:
				if mvs[i][1] == mvs[i + 1][1]:
					count += 1
					if count >= self.victory_length:
						return True 
				else:
					count = 0 
			else:
				count = 0
		return False 

	def diagonals(self):
		if len(self.current_player.moves) < self.victory_length:
			return False 

		mvs = sorted(self.current_player.moves)

		# forward diagonals 
		count = 1
		for i in range(len(mvs) - 1):
			if mvs[i][1] + 1 == mvs[i + 1][1]:
				if mvs[i][0] + 1 == mvs[i + 1][0]:
					count += 1
					if count >= self.victory_length:
						return True 
				else:
					count = 0 
			else:
				count = 0
		
		# backwards diagonals 

		count = 1
		for i in range(len(mvs) - 1):
			if mvs[i][1] - 1 == mvs[i + 1][1]:
				if mvs[i][0] + 1 == mvs[i + 1][0]:
					count += 1
					if count >= self.victory_length:
						return True 
				else:
					count = 0 
			else:
				count = 0
		return False  
