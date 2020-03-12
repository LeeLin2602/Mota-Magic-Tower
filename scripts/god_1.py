class NPC():
	def __init__(self, arg):
		self.count = 0
	def trigger(self):
		if "price_1" not in self.parameter['variables']:
			self.parameter['variables']['price_1'] = 20

		key = 0

		while True:
			key = self.conversation_control.choice("resources/NPC/blue_god.png", "勇敢的勇者啊！我是力量之神！\n如果你給我 %s 元我可以給你帶來：" % self.parameter['variables']['price_1'], ["生命 800 點", "攻擊力 4 點", "防禦力 4 點", "放棄"],"", key)
			
			if key == -1 or key == 3:
				return

			if self.cost("money", self.parameter['variables']['price_1']):

				if key == 0:
					self.cost("health", -800)
				elif key == 1:
					self.cost("attack", -4)
				elif key == 2:
					self.cost("defence", -4)

				self.parameter['variables']['price_1'] += 1

			else:
				self.conversation_control.print_word("力量之神","你並沒有足夠的錢。", 'blue_god')