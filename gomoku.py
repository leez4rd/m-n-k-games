from vidstream import *
import tkinter as tk 
import socket
import threading
import requests 
import random 
import pygame 

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

	def __init__(self, st, charr):
		self.name = st
		self.char = charr
		self.moves = [] 

	def record_move(self, move):
		self.moves += [move]


class Game:

	def __init__(self, rows, columns, k, *args):

		SYMBOLS = ['X', 'O', 'Z'] # and so on
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
			self.player_dict['P1'] = Player('Mario', 'X')
			self.player_dict['P2'] = Player('Luigi', 'O')
		else:
			# initialize players with names 
			for i, name in enumerate(self.names):
				pnum = 'P' + str(i + 1) 
				# setattr(self, pnum, Player(name))
				self.player_dict[pnum] = Player(name, SYMBOLS[i])

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
				if self.find_wins():
					game_over = True 
					winner = self.current_player
				elif self.turn_count == self.m * self.n - 1: # careful of off by one errors here 
					game_over = True 
					winner = None 

				# efficiency note: this should only check after min possible # of turns for win 
				# additionally, we should track the number of k-1 rows to optimize 
				# however, premature optimization is the root of all evil, so just gonna get it working first
				
				print(self.current_player.name)
				self.next_turn() # need a way to update player 

			else:
				print("That space already contains a pebble") # don't change player, just return to loop

		if winner == None:
			print("It's a tie")
		else:
			print("The winner is ", winner.name)
			self.gameboard.display_board()
			# erase board in case player wants a rematch 


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

	# issue: this only checks one diagonal direction 
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
		'''
		return False 
		# return False # temporary escape until I fix this function 
		possible_wins = [] # maybe keep track of all groups of k - 1 to expedite this instead of checking each time
		# then we only need to check which ones were previously one away from victory
		# this will be unique for each player, so may be memory-intensive 

		possible_win_num = int(len(self.current_player.moves) / self.victory_length)

		# this should create a bunch of lists of possible win rows 
		# this is in the order that the moves are made -- it should be sorted instead 
		possible_win_rows = []
		for i in range(possible_win_num):
			possible_win_rows += sorted(self.current_player.moves[i:i+self.victory_length])
		start = 0
		consecutive = 1  # start this at 1
		# inefficient because of overlap between possible win rows, maybe just check discrete chunks and merge? 
		# need to think about algorithm here 

		# forward diagonals 
		while consecutive <= self.victory_length and start < len(possible_win_rows) - 1:
			if possible_win_rows[start + 1][0] == possible_win_rows[start][0] + 1:
				if possible_win_rows[start + 1][1] == possible_win_rows[start][1] + 1:
					consecutive += 1
				else:
					consecutive = 0
			start += 1
		
		if consecutive >= self.victory_length:
			return True # should I just set self.win = True or do that using return value from function ? 
		
		# backward diagonals -- we can eliminate impossible ones if sorted (has to be enough space for one)

		consecutive = 1
		start = 0
		print(possible_win_rows)
		if possible_win_rows[start][1] < self.victory_length - 1:
			start += 1 # insufficient space in this row 
		while consecutive <= self.victory_length and start < len(possible_win_rows) - 1:
			if possible_win_rows[start + 1][0] == possible_win_rows[start][0] + 1: # we are going L2R in rows -> addition 
				if possible_win_rows[start + 1][1] == possible_win_rows[start][1] - 1: # we are moving up in columns -> subtraction 
					consecutive += 1
				else:
					consecutive = 0
			start += 1
		
		if consecutive >= self.victory_length:
			return True # should I just set self.win = True or do that using return value from function ? 
		return False
		'''

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

		if len(self.current_player.moves) < self.victory_length:
			return False 
		# much better algorithm, but probably still not optimal since we are not using information from last check 
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
		'''
		possible_wins = [] # maybe keep track of all groups of k - 1 to expedite this instead of checking each time
		# then we only need to check which ones were previously one away from victory
		# this will be unique for each player, so may be memory-intensive 
		possible_win_rows = []
		possible_win_num = int(len(self.current_player.moves) // self.victory_length)

		# this should create a bunch of lists of possible win rows 
		for i in range(possible_win_num):
			possible_win_rows += sorted(self.current_player.moves[i:i+self.victory_length])

		start = 0
		consecutive = 1
		while consecutive < self.victory_length and start < len(possible_win_rows) - 1:
			if start == possible_win_num:
				break
			if possible_win_rows[start][1] + 1 == possible_win_rows[start + 1][1]:
				if possible_win_rows[start][0] == possible_win_rows[start + 1][0]:
					consecutive += 1
			else:
				consecutive = 0
			start += 1
		if consecutive >= self.victory_length:
			return True # should I just set self.win = True or do that using return value from function ? 
		else:
			return False 
		'''

#issue: setting every array at same time



# REMAINING TASKS:
# 1 write functions to check each win condition
# 2 make rudimentary GUI which displays gameboard tic-tac-toe style
# 3 clean code and make project-grade
# 4 make an AI to play
# 5 if i really wanna go wild... add gravity so it can also simulate connect four 




def show_option_menu():

	window = tk.Tk()
	window.title("Customize your game")
	window.geometry('500x400')

	row_count_label = tk.Label(window, text="Rows: ")
	row_count_label.pack()


	# text box for row count 
	row_count = tk.Text(window, height=1)
	row_count.pack()
	m = int(row_count.get("1.0","end"))

	column_count_label = tk.Label(window, text="Columns: ")
	column_count_label.pack()

	# text box for column count
	column_count = tk.Text(window, height=1)
	column_count.pack()
	n = int(column_count.get("1.0","end"))

	vic_length_label = tk.Label(window, text="Length of winning row: ")
	vic_length_label.pack()

	# text box for victory length
	vic_length = tk.Text(window, height=1)
	vic_length.pack()
	k = int(vic_length.get("1.0","end"))

	num_players_label = tk.Label(window, text="Players: ")
	num_players_label.pack()

	# text box for number of players 
	num_players = tk.Text(window, height=1)
	num_players.pack()
	p = int(num_players.get("1.0","end"))

	'''
	not quite sure how to escape this menu 
	def end_customization(flg):
		flg = False

	flag = True
	while flag == True:
		finish_customizing = tk.Button(window, text = "Finish customizing", width=50, command = end_customization(flag))
		finish_customizing.pack(anchor = tk.CENTER, expand = True)
	'''

	return m, n, k, p



	
def new_game():


	m, n, k, p = show_option_menu()
	# add way to list player names according to value of p 

	mrgame = Game(m, n, k, "player", "names") # etc ...
	btn_listen = tk.Button(window, text = "Start Game", width=50, command = mrgame.run_game)
	btn_listen.pack(anchor = tk.CENTER, expand = True)



def main():


	tictactoe = Game(3, 3, 3, "me", "you")
	gomoku = Game(10, 10, 5, "me", "you")
	pente = Game(10, 10, 5, "1", "2", "3", "4", "5")

	#GUI

	# opens the application window
	window = tk.Tk()
	window.title("Tic Tac Toe (Engorged)")
	window.geometry('500x400')

	new_game_btn = tk.Button(window, text = "New Game (work in progress)", width=50, command = new_game)
	start_game_btn = tk.Button(window, text = "Start Game", width=50, command = gomoku.run_game)
	
	new_game_btn.pack(anchor = tk.CENTER, expand = True)
	start_game_btn.pack(anchor = tk.CENTER, expand = True)

	window.mainloop()


if __name__ == '__main__':
	main()


# for GUI later 
'''
screen = pygame.display.set_mode(size)

def draw_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
     
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS) 
            pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
draw_board()
 

# repurposed from connect four tutorial 
pygame.init()
#define our screen size
SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
 
ROW_COUNT = 6
COLUMN_COUNT = 7
 
#define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
 
size = (width, height)
 
RADIUS = int(SQUARESIZE/2 - 5)
	


'''

# label for the text box
'''
# for multiplayer  

label_target_ip = tk.Label(window, text="Target IP:")
label_target_ip.pack()


# text box for target IP
text_target_ip = tk.Text(window, height=1)
text_target_ip.pack()
'''