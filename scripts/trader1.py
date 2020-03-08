class NPC():
	def __init__(self, arg):
		self.count = 0
	def trigger(self):
		key = self.conversation_control.print_word("商人","又有人來送死了啊！哈哈！", 'npc_2')
		key = self.conversation_control.print_word("商人","你想要兩顆紅寶石嗎？就賣你 40 塊錢", 'npc_2', prompt = "（Ｙ／Ｎ）", keys = [ord('y'), ord('n')])

		if key == ord('y') and self.status.cost("money", 40):
			self.status.cost("attack", -4)
			self.status.expire()
		elif key == ord('y'):
			self.conversation_control.print_word("商人","你沒有足夠的錢！" , 'npc_2')