class NPC():
	def __init__(self, arg):
		self.count = 0
	def trigger(self):
		key = self.conversation_control.print_word("商人","你想要兩顆紅寶石嗎？賣你 200 塊錢", 'npc_2', prompt = "（Ｙ／Ｎ）", keys = [ord('y'), ord('n')])

		if key == ord('y') and self.status.cost("money", 200):
			self.status.cost("attack", -8)
			self.status.expire()
		elif key == ord('y'):
			self.conversation_control.print_word("商人","你沒有足夠的錢！" , 'npc_2')