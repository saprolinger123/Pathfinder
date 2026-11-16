class Board:

	def __init__(self):
		self.turn = 0
		
		self.TOP = 1
		self.RIGHT = 2
		self.BOTTOM = 3
		self.LEFT = 4

		self.fences = [] # fence format: [x1, y1, x2, y2, side]

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

	def 
