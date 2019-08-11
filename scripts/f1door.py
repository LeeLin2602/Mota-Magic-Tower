class monster():
	def __init__(self, arg):
		pass

	def trigger(self):
		this_floor = self.status.floor
		this_floor.tags[0].is_open = True