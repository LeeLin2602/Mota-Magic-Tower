class monster():
	def __init__(self, arg):
		pass

	def trigger(self):
		this_floor = self.status.floor
		if not (this_floor.tags[4].valid or this_floor.tags[5].valid):
			this_floor.tags[6].open()
			self.status.valid = False