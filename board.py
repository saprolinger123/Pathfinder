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
		# First, it gets any legal jump moves. Then, it gets legal pawn moves, using get_neighbors. Finally, it gets all the fence moves. The order is important, as it makes alpha-beta pruning more effective.

		legal_jump_moves = []

		legal_pawn_moves = []

		legal_fence_moves = []

		return legal_jump_moves + legal_pawn_moves + legal_fence_moves

	
	def make_move(self, move_type, move):
		# move_type: "move", "fence", or "jump"
		# player move format: self.TOP, self.RIGHT, self.BOTTOM, or self.LEFT. 
		# fence move format is the same as the fence format: [part_1, part_2], and the part format is [x, y, side].
		# jump move format: [move_1, move_2]

		if self.turn == 1:
			current_player_pos = self.player_1_pos
		else:
			current_player_pos = self.player_2_pos

		if move_type == "move":
			if move == self.TOP:
				current_player_pos[1] -= 1
			elif move == self.RIGHT:
				current_player_pos[0] += 1
			elif move == self.BOTTOM:
				current_player_pos[1] += 1
			else:
				current_player_pos[0] -= 1

		elif move_type == "fence":
			if self.turn == 1:
				self.player_1_fences -= 1
			else:
				self.player_2_fences -= 1
			self.fences.append(move)
			self.fence_parts.append(move[0])
			self.fence_parts.append(move[1])
		else:
			for movement in move:
				if movement == self.TOP:
					current_player_pos[1] -= 1
				elif movement == self.RIGHT:
					current_player_pos[0] += 1
				elif movement == self.BOTTOM:
					current_player_pos[1] += 1
				else:
					current_player_pos[0] -= 1

		self.turn = 3 - self.turn

	def undo_move(self, move_type, move):
		if self.turn == 1:
			current_player_pos = self.player_1_pos
		else:
			current_player_pos = self.player_2_pos

		if move_type == "move":
			if move == self.TOP:
				current_player_pos[1] += 1
			elif move == self.RIGHT:
				current_player_pos[0] -= 1
			elif move == self.BOTTOM:
				current_player_pos[1] -= 1
			else:
				current_player_pos[0] += 1

		elif move_type == "fence":
			if self.turn == 1:
				self.player_1_fences += 1
			else:
				self.player_2_fences += 1
			self.fences.remove(move)
			self.fence_parts.remove(move[0])
			self.fence_parts.remove(move[1])
		else:
			for movement in move:
				if movement == self.TOP:
					current_player_pos[1] += 1
				elif movement == self.RIGHT:
					current_player_pos[0] -= 1
				elif movement == self.BOTTOM:
					current_player_pos[1] -= 1
				else:
					current_player_pos[0] += 1

		self.turn = 3 - self.turn


	def get_neighbors(self, square):

		deltas = [
			self.RIGHT,
			self.TOP,
			self.LEFT,
			self.BOTTOM
		]

		candidates = [
			(square[0] + 1, square[1]),
			(square[0], square[1] - 1),
			(square[0] - 1, square[1]),
			(square[0], square[1] + 1)
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
