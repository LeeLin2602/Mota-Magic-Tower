class trigger():
	def __init__(self, arg):
		pass

	def trigger(self):
		this_floor = self.status.floor
		this_floor.tags[10].valid = True
		this_floor.tags[10].visible = True
		this_floor.tags[11].valid = True
		this_floor.tags[11].visible = True
		this_floor.tags[12].valid = True
		this_floor.tags[12].visible = True
		self.status.valid = False
		self.play_audio("close_door")
		self.conversation_control.print_word("勇者", "糟糕！這是個陷阱。","player")