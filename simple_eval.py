def simple_eval(board, player):
	# Checks the distance from the first player, subtracts the distance fromm the second player, and divides by 8.
	return board.player_1_pos[1]/8 - (8-board.player_2_pos[1])/8
