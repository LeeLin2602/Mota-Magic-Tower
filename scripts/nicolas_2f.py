class NPC():
	def __init__(self, arg):
		pass
	def trigger(self):
		this_floor = self.status.floor
		for i in range(10, 18):
			if self.status.floor.tags[i].valid:
				self.conversation_control.print_word("尼古拉", "（小聲）少年，先別攻擊我。\n請你幫我殺掉我周遭那群該死的騎士。","nicolas")
				return
		self.conversation_control.print_word("尼古拉", "謝謝你救了我，我叫做尼古拉，是這座塔的主人。","nicolas")
		self.conversation_control.print_word("勇者", "什麼？你是這座塔的主人？\n那你為什麼會被關在這裡？還有公主在哪裡？","player")

		self.parameter["variables"]["saving_nicolas"] = True
