MAX_PATH_LENGTH = 80


def _distance_to_goal(board, start, goal_row):
	start = tuple(start)
	queue = [(start, 0)]
	next_square = 0
	visited = {start}
	directions = (
		(board.TOP, (0, -1)),
		(board.RIGHT, (1, 0)),
		(board.BOTTOM, (0, 1)),
		(board.LEFT, (-1, 0))
	)

	while next_square < len(queue):
		square, distance = queue[next_square]
		next_square += 1
		if square[1] == goal_row:
			return distance

		for direction, (dx, dy) in directions:
			neighbor = (square[0] + dx, square[1] + dy)
			if (board.in_bounds(neighbor)
					and not board.is_blocked(square, direction, board.fence_parts)
					and neighbor not in visited):
				visited.add(neighbor)
				queue.append((neighbor, distance + 1))



def simple_eval(board):
	player_1_distance = _distance_to_goal(board, board.player_1_pos, 0)
	player_2_distance = _distance_to_goal(board, board.player_2_pos, 8)
	return (player_2_distance - player_1_distance) / MAX_PATH_LENGTH
