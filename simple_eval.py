MAX_PATH_LENGTH = 80


def _distance_to_goal(board, start, goal_row):
	player = 1 if goal_row == 0 else 2
	path = board.get_path_to_goal(start, player)
	return len(path) - 1 if path is not None else MAX_PATH_LENGTH



def simple_eval(board):
	player_1_distance = _distance_to_goal(board, board.player_1_pos, 0)
	player_2_distance = _distance_to_goal(board, board.player_2_pos, 8)
	return (player_2_distance - player_1_distance) / MAX_PATH_LENGTH
