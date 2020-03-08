class NPC():
	def __init__(self, arg):
		self.count = 0
	def trigger(self):
		
		key = self.conversation_control.print_word("商人","你想買點什麼嗎？", 'god')
