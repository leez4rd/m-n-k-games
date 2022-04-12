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

m = 3
n = 3
Amoves = []
Bmoves = []
gameboard = [[False]*m]*n
print(gameboard)


Asturn = True
game = True 

#issue: setting every array at same time
while(game):
	move = list(map(int, input("Enter a set of coordinates separated by a comma: ").split(',')))
	print(gameboard)
	#if space is open...
	if (gameboard[move[0]][move[1]] == False):
		if (Asturn):
			Amoves += move 
			#search over Amoves for win
		else:
			Bmoves += move 
			#search over Bmoves for win 
			#if found, set game to Flase
		gameboard[move[0]][move[1]] = True 
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
