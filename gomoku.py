from vidstream import *
import tkinter as tk 
import socket
import threading
import requests 
import random 

# m rows 
# n columns

# cell [i,j] will contain either 
# player A's tile or player B's tile 

# very simple version:
# ask for input of user A's move, user enters coordinate [i,j],
# then do the same for B

# make sure they are not equal, keep track of all moves
# (maybe in a hash table?)
# after every turn, we check if there is a row of k for one player
# ie after player A goes, the array of A's moves will look like
# [(3,5), (2, 6), (5,2), (0, 3), ...]
# we have to iterate through this structure and check for 
# diagonal wins, horizontal wins, and vertical wins

# vertical occurs when we have (c, n), (c, n+1), ... , (c, n + k -1)
# horizontal occurs when we have (n, c), (n + 1, c), ... , (n + k - 1, c)
# diagonal occurs when we have (i, j), (i + 1, j + 1), ... (i + k - 1, j + k - 1)

# what is the most efficient way to search for these patterns? 
# naive approach///
# check if next entry is consecutive to last, do this until its false
# have a counter of how many times its true 




""" 
current issues / missing features

the game does not end when a full row is created 
the symbol does not change from turn to turn 
we only have two symbols now, should be pulled from random character set 
win checks not tested yet 
when bad input is entered, we need to catch the exception instead of quitting the program 
need to determine best design choices and optimize code

"""



# important architectural decision:
# do we want to track the evolution of a Board object to check wins
# or do we want each player to keep track of their own moves so we can just iterate through array ? 

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


class Player:

	def __init__(self, st):
		self.name = st
		x = random.randint(0, 1)
		if x == 1:
			self.char = 'X'
		else:
			self.char = 'O'
		self.moves = [] 

	def record_move(self, move):
		self.moves += [move]


class Game:

	def __init__(self, rows, columns, k, *args):

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
		# maybe add input checking to generate default names if none provided? 
		# something like

		if (len(args) == 0):
			# default to two player 
			# P1 = Player('Mario')
			# P2 = Player('Luigi')
			# may need to do it this way...
			self.player_dict['P1'] = Player('Mario')
			self.player_dict['P2'] = Player('Luigi')
		else:
			# initialize players with names 
			for i, name in enumerate(self.names):
				pnum = 'P' + str(i + 1) 
				# setattr(self, pnum, Player(name))
				self.player_dict[pnum] = Player(name)

		self.current_player = self.player_dict['P1'] # might be problematic

	def run_game(self):
		game_over = False 

		while not game_over:
			# ask current player for a move 
			self.gameboard.display_board()
			move = list(map(int, input("Enter a set of coordinates separated by a comma: ").split(',')))

			if self.gameboard.gameboard[move[0]][move[1]] == ' ':
				self.current_player.record_move(move)
				self.gameboard.update_board(move, self.current_player.char)
				if self.turn_count == self.m * self.n: # careful of off by one errors here 
					game_over = True 
					winner = None 
				if self.find_wins():
					game_over = True 
					winner = self.current_player
				
				self.next_turn() # need a way to update player 

			else:
				print("That space already contains a pebble") # don't change player, just return to loop

			'''
			#if space is open...
			if (gameboard[move[0]][move[1]] == ' '):
				if (Asturn):
					Amoves += move 
					gameboard[move[0]][move[1]] = 'X' 
					Asturn = False
					#search over Amoves for win
				else:
					Bmoves += move 
					gameboard[move[0]][move[1]] = 'O' 
					Asturn = True
					#search over Bmoves for win 
					#if found, set game to Flase
					
				#space on gameboard is now filled 
				
				print(Bmoves)
				print(Amoves)
				#now it is B's turn
			else:
				print("that space already contains a pebble")
			'''
		if winner == None:
			print("It's a tie")
		else:
			print("The winner is ", winner.name)

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

	def diagonals(self):
		return False # temporary escape until I fix this function 
		possible_wins = [] # maybe keep track of all groups of k - 1 to expedite this instead of checking each time
		# then we only need to check which ones were previously one away from victory
		# this will be unique for each player, so may be memory-intensive 

		possible_win_num = int(len(self.current_player.moves) / self.victory_length)

		# this should create a bunch of lists of possible win rows 
		possible_win_rows = []
		for i in range(possible_win_num):
			possible_win_rows += self.current_player.moves[i:i+self.victory_length]

		start = 0
		consecutive = 0
		# inefficient because of overlap between possible win rows, maybe just check discrete chunks and merge? 
		# need to think about algorithm here 
		while consecutive < self.victory_length and start < len(possible_win_rows):
			print(start)
			print(possible_win_rows)

			# WHY DOES CHANGING THE INDEXING MAKE IT ONLY DISPLAY ONE SYMBOL !???
			# does not work at edges... 
			if start == possible_win_num:
				return False # check this logic 
			else:
				if possible_win_rows[start + 1][0] + 1 == possible_win_rows[start + 1][0]:
					if possible_win_rows[start + 1][1] + 1 == possible_win_rows[start + 1][1]:
						consecutive += 1
					else:
						consecutive = 0
			start += 1

		if consecutive >= self.victory_length:

			return True # should I just set self.win = True or do that using return value from function ? 
		else:
			return False 
		return True

	'''
	def rows(moves_list):
		for el1, el2, el3 in moves_list:
			return True
	'''

	# assuming each player has a list of moves that they have made 
	def rows(self): # pass a Player object, or rely on internal referencing from game 
		'''
		for i, move in enumerate(player.moves):
				moves[i] 
		'''
		possible_wins = [] # maybe keep track of all groups of k - 1 to expedite this instead of checking each time
		# then we only need to check which ones were previously one away from victory
		# this will be unique for each player, so may be memory-intensive 
		possible_win_rows = []
		possible_win_num = int(len(self.current_player.moves) / self.victory_length)

		# this should create a bunch of lists of possible win rows 
		for i in range(possible_win_num):
			possible_win_rows += self.current_player.moves[i:i+self.victory_length][0]

		start = 0
		consecutive = 0
		# PROBLEM: NEED TO CHECK EQUALITY IE THAT WE ARE IN SAME ROW OR WE WILL GET SPURIOUS WINS 
		while consecutive < self.victory_length and start < len(possible_win_rows):
			if possible_win_rows[start] + 1 == possible_win_rows[start + 1]:
				consecutive += 1
			else:
				consecutive = 0
			start += 1
		if consecutive >= self.victory_length:
			return True # should I just set self.win = True or do that using return value from function ? 
		else:
			return False 

	def columns(self):
		# exact same thing as rows except for one character -- maybe combine functions 
		'''
		for i, move in enumerate(player.moves):
				moves[i] 
		'''
		possible_wins = [] # maybe keep track of all groups of k - 1 to expedite this instead of checking each time
		# then we only need to check which ones were previously one away from victory
		# this will be unique for each player, so may be memory-intensive 
		possible_win_rows = []
		possible_win_num = int(len(self.current_player.moves) / self.victory_length)

		# this should create a bunch of lists of possible win rows 
		for i in range(possible_win_num):
			possible_win_rows += self.current_player.moves[i:i+self.victory_length][1]

		start = 0
		consecutive = 0
		while consecutive < self.victory_length and start < len(possible_win_rows):
			if possible_win_rows[start] + 1 == possible_win_rows[start + 1]:
				consecutive += 1
			else:
				consecutive = 0
			start += 1
		if consecutive >= self.victory_length:
			return True # should I just set self.win = True or do that using return value from function ? 
		else:
			return False 


#issue: setting every array at same time



# REMAINING TASKS:
# 1 write functions to check each win condition
# 2 make rudimentary GUI which displays gameboard tic-tac-toe style
# 3 clean code and make project-grade
# 4 make an AI to play
# 5 if i really wanna go wild... add gravity so it can also simulate connect four 









def main():
	tictactoe = Game(3, 3, 3, "me", "you")
	gomoku = Game(10, 10, 5, "me", "you")

	#GUI

	# opens the application window
	window = tk.Tk()
	window.title("Tic Tac Toe (Engorged)")
	window.geometry('500x400')

	# label for the text box
	label_target_ip = tk.Label(window, text="Target IP:")
	label_target_ip.pack()

	# text box for target IP
	text_target_ip = tk.Text(window, height=1)
	text_target_ip.pack()

	# buttons
	btn_listen = tk.Button(window, text = "Start Game", width=50, command = gomoku.run_game())
	btn_listen.pack(anchor = tk.CENTER, expand = True)

	window.mainloop()


if __name__ == '__main__':
	main()