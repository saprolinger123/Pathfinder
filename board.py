class Board:

	def __init__(self):
		self.turn = 1
		
		self.TOP = 1
		self.RIGHT = 2
		self.BOTTOM = 3
		self.LEFT = 4

		self.fence_parts = [] # fence_part format: [x, y, side] ### IMPORTANT: side cannot be LEFT or BOTTOM. Instead, use the right of square to the left, or the top of the square to the bottom. ###
		self.fences = [] # fence format: [part_1, part_2]

		self.player_1_pos = [4, 8]
		self.player_2_pos = [4, 0]
		self.player_1_fences = 10
		self.player_2_fences = 10

	def check_win(self):
		if self.player_1_pos[1] == 0:
			return 1

		elif self.player_2_pos[1] == 8:
			return 2

		return 0

	def get_legal_moves(self):
		pass

	
	def make_move(self, move):
		pass

	
	def undo_move(self, move):
		pass


	def get_neighbors(self, square):

		deltas = [
			self.RIGHT,
			self.TOP,
			self.LEFT,
			self.BOTTOM
		]

		candidates = [
			(square[0] + 1, square[1]),
			(square[0], square[1] + 1),
			(square[0] - 1, square[1]),
			(square[0], square[1] - 1)
		]

		neighbors = []

		width = 9
		height = 9

		for i in range(len(candidates)):
			x = candidates[i][0]
			y = candidates[i][1]



			if 0 <= x < width and 0 <= y < height:
				
				if deltas[i] == self.RIGHT:
					if [square[0], square[1], self.RIGHT] in self.fence_parts:
						continue

				elif deltas[i] == self.TOP:
					if [square[0], square[1], self.TOP] in self.fence_parts:
						continue

				elif deltas[i] == self.LEFT:
					if [square[0] - 1, square[1], self.RIGHT] in self.fence_parts:
						continue

				else:
					if [square[0], square[1] + 1, self.TOP] in self.fence_parts:
						continue

				if candidates[i] == tuple(self.player_1_pos if self.turn == 2 else self.player_2_pos):
					continue

				neighbors.append((x, y))

		return neighbors
