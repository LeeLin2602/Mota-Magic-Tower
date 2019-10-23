class trigger():
	def __init__(self, arg):
		pass

	def trigger(self):
		self.conversation_control.print_word("怪物","遇過此關，沒門！", 'resources/怪物/8,0.png')
		self.status.valid = False