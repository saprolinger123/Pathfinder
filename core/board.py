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

		self.path_cache = {}
		self.fence_crosses_path_cache = {}
		self._fence_part_set = frozenset()
		self.ply = 0

	def _mirror_fence_part(self, part):
		x, y, side = part
		mirrored_x = 7 - x if side == self.RIGHT else 8 - x
		return (mirrored_x, y, side)

	def _get_path_to_goal(self, start, player, fence_parts=None):
		if fence_parts is None:
			fence_part_set = self._fence_part_set
		else:
			fence_part_set = frozenset(tuple(part) for part in fence_parts)

		original_key = (
			tuple(start),
			player,
			tuple(sorted(fence_part_set)),
		)
		mirrored_start = (8 - start[0], start[1])
		mirrored_fences = frozenset(
			self._mirror_fence_part(part) for part in fence_part_set
		)
		mirrored_key = (
			mirrored_start,
			player,
			tuple(sorted(mirrored_fences)),
		)
		cache_key = min(original_key, mirrored_key)
		canonical_is_mirrored = original_key != mirrored_key and cache_key == mirrored_key

		if cache_key in self.path_cache:
			path = self.path_cache[cache_key]
			if canonical_is_mirrored and path is not None:
				path = tuple((8 - square[0], square[1]) for square in path)
			return path

		goal_row = 0 if player == 1 else 8
		if canonical_is_mirrored:
			search_start = mirrored_start
			search_fence_part_set = mirrored_fences
		else:
			search_start = tuple(start)
			search_fence_part_set = fence_part_set

		queue = [tuple(search_start)]
		visited = {tuple(search_start)}
		parents = {tuple(search_start): None}
		directions = [(self.TOP, 0, -1), (self.RIGHT, 1, 0),
					  (self.BOTTOM, 0, 1), (self.LEFT, -1, 0)]

		while queue:
			square = queue.pop(0)
			if square[1] == goal_row:
				break

			for direction, dx, dy in directions:
				neighbor = (square[0] + dx, square[1] + dy)
				if (neighbor not in visited
						and self.in_bounds(neighbor)
						and not self.is_blocked(square, direction, search_fence_part_set)):
					visited.add(neighbor)
					parents[neighbor] = square
					queue.append(neighbor)

		if square[1] != goal_row:
			path = None
		else:
			path = []
			while square is not None:
				path.append(square)
				square = parents[square]
			path.reverse()

		path = None if path is None else tuple(path)
		self.path_cache[cache_key] = path
		if canonical_is_mirrored and path is not None:
			return tuple((8 - square[0], square[1]) for square in path)
		return path

	def get_path_to_goal(self, start, player, fence_parts=None):
		path = self._get_path_to_goal(start, player, fence_parts)
		return None if path is None else [list(square) for square in path]

	def get_path_length_to_goal(self, start, player):
		path = self._get_path_to_goal(start, player)
		return None if path is None else len(path) - 1

	def check_win(self):
		if self.player_1_pos[1] == 0:
			return 1

		elif self.player_2_pos[1] == 8:
			return 2

		return 0

	def get_legal_moves(self):
		# First, it gets any legal jump moves. Then, it gets legal pawn moves, using get_neighbors. Finally, it gets all the fence moves. The order is important, as it makes alpha-beta pruning more effective.
		legal_jump_moves = []
		deltas = [
			(self.TOP, (0, -1)),
			(self.RIGHT, (1, 0)),
			(self.BOTTOM, (0, 1)),
			(self.LEFT, (-1, 0))
		]
		current_player_pos = self.player_1_pos if self.turn == 1 else self.player_2_pos
		opponent_pos = self.player_2_pos if self.turn == 1 else self.player_1_pos

		for direction, (dx, dy) in deltas:
			adjacent = [current_player_pos[0] + dx, current_player_pos[1] + dy]
			if not self.in_bounds(adjacent) or self.is_blocked(current_player_pos, direction):
				continue
			if adjacent != opponent_pos:
				continue

			behind = [adjacent[0] + dx, adjacent[1] + dy]
			if self.in_bounds(behind) and not self.is_blocked(adjacent, direction):
				legal_jump_moves.append(("jump", [direction, direction]))
				continue

			side_directions = (
				(self.RIGHT, self.LEFT) if direction in (self.TOP, self.BOTTOM)
				else (self.TOP, self.BOTTOM)
			)
			for side_direction in side_directions:
				side_delta = next(delta for move_direction, delta in deltas if move_direction == side_direction)
				side_square = [adjacent[0] + side_delta[0], adjacent[1] + side_delta[1]]
				if self.in_bounds(side_square) and not self.is_blocked(adjacent, side_direction):
					legal_jump_moves.append(("jump", [direction, side_direction]))

		legal_pawn_moves = []
		for neighbor in self.get_neighbors(current_player_pos):
			for direction, (dx, dy) in deltas:
				if neighbor == (current_player_pos[0] + dx, current_player_pos[1] + dy):
					legal_pawn_moves.append(("move", direction))
					break

		legal_fence_moves = []
		fence_count = self.player_1_fences if self.turn == 1 else self.player_2_fences
		if fence_count > 0:
			paths = (
				self._get_path_to_goal(self.player_1_pos, 1),
				self._get_path_to_goal(self.player_2_pos, 2),
			)
			for x in range(8):
				for y in range(1, 9):
					fence = [[x, y, self.TOP], [x + 1, y, self.TOP]]
					is_legal, priority = self.is_fence_legal(fence, paths)
					if is_legal:
						legal_fence_moves.append((priority, ("fence", fence)))

				for y in range(8):
					fence = [[x, y, self.RIGHT], [x, y + 1, self.RIGHT]]
					is_legal, priority = self.is_fence_legal(fence, paths)
					if is_legal:
						legal_fence_moves.append((priority, ("fence", fence)))

			legal_fence_moves.sort(key=lambda move: (
				move[0] != "priority",
				abs(move[1][1][0][0] + move[1][1][1][0] - 8)
				+ abs(move[1][1][0][1] + move[1][1][1][1] - 8)
			))

		return legal_jump_moves + legal_pawn_moves + [
			move for _, move in legal_fence_moves
		]


	def in_bounds(self, square):
		return 0 <= square[0] < 9 and 0 <= square[1] < 9


	def is_blocked(self, square, direction, fence_parts=None):
		if fence_parts is None:
			fence_parts = self._fence_part_set

		x, y = square
		if direction == self.RIGHT:
			part = [x, y, self.RIGHT]
		elif direction == self.TOP:
			part = [x, y, self.TOP]
		elif direction == self.LEFT:
			part = [x - 1, y, self.RIGHT]
		else:
			part = [x, y + 1, self.TOP]
		if isinstance(fence_parts, (set, frozenset)):
			return tuple(part) in fence_parts
		return part in fence_parts


	def fence_crosses_existing(self, fence):
		
		x, y, side = fence[0]
		for existing in self.fences:
			existing_x, existing_y, existing_side = existing[0]
			if side == existing_side:
				continue
			if side == self.TOP and x == existing_x and y == existing_y + 1:
				return True
			if side == self.RIGHT and x == existing_x and existing_y == y + 1:
				return True
		return False


	def has_path_to_goal(self, start, player, fence_parts):
		return self._get_path_to_goal(start, player, fence_parts) is not None


	def fence_crosses_path(self, fence, path):
		if path is None:
			return False

		original_key = (
			tuple(sorted(tuple(part) for part in fence)),
			tuple(tuple(square) for square in path),
		)
		cache_key = original_key
		if cache_key in self.fence_crosses_path_cache:
			return self.fence_crosses_path_cache[cache_key]

		for square, neighbor in zip(path, path[1:]):
			dx = neighbor[0] - square[0]
			dy = neighbor[1] - square[1]
			direction = ((0, -1, self.TOP), (1, 0, self.RIGHT),
						 (0, 1, self.BOTTOM), (-1, 0, self.LEFT))
			for ddx, ddy, move_direction in direction:
				if dx == ddx and dy == ddy:
					if self.is_blocked(square, move_direction, fence):
						self.fence_crosses_path_cache[cache_key] = True
						return True
					break
		self.fence_crosses_path_cache[cache_key] = False
		return False


	def is_fence_legal(self, fence, paths=None):
		if any(part in self.fence_parts for part in fence) or self.fence_crosses_existing(fence):
			return [False, "normal"]

		if paths is None:
			paths = (
				self._get_path_to_goal(self.player_1_pos, 1),
				self._get_path_to_goal(self.player_2_pos, 2),
			)
		path_1, path_2 = paths
		crosses_1 = self.fence_crosses_path(fence, path_1)
		crosses_2 = self.fence_crosses_path(fence, path_2)
		priority = "priority" if crosses_1 or crosses_2 else "normal"
		if self.ply < 3:
			return [True, priority]

		if not crosses_1 and not crosses_2:
			return [True, priority]

		fence_parts = self.fence_parts + fence
		if crosses_1 and not self.has_path_to_goal(self.player_1_pos, 1, fence_parts):
			return [False, priority]
		if crosses_2 and not self.has_path_to_goal(self.player_2_pos, 2, fence_parts):
			return [False, priority]
		return [True, priority]

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
			self._fence_part_set = self._fence_part_set.union(
				(tuple(move[0]), tuple(move[1]))
			)
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

		self.ply += 1

		self.turn = 3 - self.turn

	def undo_move(self, move_type, move):
		previous_turn = 3 - self.turn
		if previous_turn == 1:
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
			if previous_turn == 1:
				self.player_1_fences += 1
			else:
				self.player_2_fences += 1
			self.fences.remove(move)
			self.fence_parts.remove(move[0])
			self.fence_parts.remove(move[1])
			self._fence_part_set = self._fence_part_set.difference(
				(tuple(move[0]), tuple(move[1]))
			)
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

		self.ply -= 1

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
				if self.is_blocked(square, deltas[i]):
					continue

				if candidates[i] == tuple(self.player_1_pos if self.turn == 2 else self.player_2_pos):
					continue

				neighbors.append((x, y))

		return neighbors
