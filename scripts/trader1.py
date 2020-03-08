class NPC():
	def __init__(self, arg):
		self.count = 0
	def trigger(self):

		if 'trader_f1_buy' not in self.parameter['variables']:

			key = self.conversation_control.print_word("商人","我這有一顆紅寶石，就賣你 15 塊錢", 'npc_2', prompt = "（Ｙ／Ｎ）", keys = [ord('y'), ord('n')])

			if key == ord('y') and self.status.cost("money", 15):
				self.status.cost("attack", -3)
				self.parameter['variables']["trader_f1_buy"] = True
			elif key == ord('y'):
				self.conversation_control.print_word("商人","你沒有足夠的錢！" , 'npc_2')
		else:

			key = self.conversation_control.print_word("商人","謝謝惠顧！我就祝你可以活久一點吧！哈哈哈～", 'npc_2')