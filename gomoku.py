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

m = 5
n = 5
Amoves = []
Bmoves = []
gameboard = [[' ']*m for _ in range(n)]
print(gameboard)


Asturn = True
game = True 

def display_board():
	for i in range(m):
		for j in range(n):
			if gameboard[i][j] == 'X':
				tile = 'X'
			elif gameboard[i][j] == 'O':
				tile = 'O'
			else:
				tile = ' '
			print("|", tile, " |", sep ='', end ='')
		print('\n', end='')
	

display_board()


#issue: setting every array at same time
while(game):

	move = list(map(int, input("Enter a set of coordinates separated by a comma: ").split(',')))
	print(gameboard)
	display_board()
	#if space is open...
	
	if (gameboard[move[0]][move[1]] == ' '):
		if (Asturn):
			Amoves += move 
			gameboard[move[0]][move[1]] = 'X' 
			#search over Amoves for win
		else:
			Bmoves += move 
			gameboard[move[0]][move[1]] = 'O' 
			#search over Bmoves for win 
			#if found, set game to Flase
		
		#space on gameboard is now filled 
		Asturn = False
		print(Bmoves)
		print(Amoves)
		#now it is B's turn
	else:
		print("that space already contains a pebble")



def Find_Wins():
	if Diagonals() or Rows() or Columns():
		return True
	else:
		return False


def Diagonals():
	return True

def Rows():
	return True

def Columns():
	return True


# REMAINING TASKS:
# 1 write functions to check each win condition
# 2 make rudimentary GUI which displays gameboard tic-tac-toe style
# 3 clean code and make project-grade
# 4 make an AI to play