class trigger():
	def __init__(self, arg):
		pass

	def trigger(self):
		this_floor = self.status.floor
		this_floor.tags[1].close()
		self.status.valid = False