class Player:

	def __init__(self, st, charr):
		self.name = st
		self.char = charr
		self.moves = [] 

	def record_move(self, move):
		self.moves += [move]
