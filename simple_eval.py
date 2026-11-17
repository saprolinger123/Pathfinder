def simple_eval(board, player):
	# Checks the distance from the player to the other side, and divides by 8.
	if player == 1:
		return board.player_1_pos[1]/8
	else:
		return -(8-board.player_2_pos[1])/8
