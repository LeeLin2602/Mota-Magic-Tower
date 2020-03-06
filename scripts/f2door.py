class monster():
	def __init__(self, arg):
		pass

	def trigger(self):
		this_floor = self.status.floor
		if not (this_floor.tags[0].valid or this_floor.tags[1].valid):
			this_floor.tags[2].is_open = True
			self.status.valid = False