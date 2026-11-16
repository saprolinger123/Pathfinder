class Board:

	def __init__(self):
		self.turn = 0

		self.vertical_fence_slots = []
		self.horizontal_fence_slots = []

		self.player_1_pos = [4, 8]
		self.player_2_pos = [4, 0]
		self.player_1_fences = 10
		self.player_2_fences = 10

		for i in range(8):
			vertical_fence_slots.append([])
			horizontal_fence_slots.append([])
			for j in range(9):
				vertical_fence_slots[i].append(0)
				horizontal_fence_slots[i].append(0)
