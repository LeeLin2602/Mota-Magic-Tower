class NPC():
	def __init__(self, arg):
		pass

	def trigger(self):
		this_floor = self.status.floor

		for i in range(10, 18):
			if self.status.floor.tags[i].valid:
				self.conversation_control.print_word("尼古拉", "（小聲）少年，先別攻擊我。\n請你幫我殺掉我周遭那群該死的騎士。","nicolas")
				return

		if "saving_nicolas" not in self.parameter["variables"]:
			self.conversation_control.print_word("尼古拉", "謝謝你救了我，我叫做尼古拉，是這座塔的主人。","nicolas")
			self.conversation_control.print_word("勇者", "什麼？你是這座塔的主人？（警覺）\n那你為什麼會被關在這裡？還有公主在哪裡？","player")
			self.conversation_control.print_word("尼古拉", "我是被那群該死的亡靈族給背叛，才淪落至此。\n公主什麼的我可不知道，你要問那群亡靈族，哼！","nicolas")
			self.conversation_control.print_word("勇者", "亡靈族？那是什麼？","player")
			self.conversation_control.print_word("尼古拉", "你所看到的骷髏、殭屍，那些要死不死的玩意，就是亡靈族。\n那種最卑賤的魔族，居然敢謀反我吸血族。","nicolas")
			self.conversation_control.print_word("勇者", "你可以再說清楚一點嗎？什麼謀反，弄得我頭好暈。","player")
			self.conversation_control.print_word("尼古拉", "千百年前，我們魔族和你們人族本來是很和諧的生活著。\n但魔族的肉體對於人類很珍貴，於是他們開始獵殺魔族。","nicolas")
			self.conversation_control.print_word("尼古拉", "魔族們為了要躲避人族的獵人，在大陸一隅蓋起了一座塔。\n這座塔防備森嚴，無數想進入塔內的獵人都死無全屍。","nicolas")
			self.conversation_control.print_word("尼古拉", "但人類會為了權力、財富而沖昏了頭，魔族也會。\n說到底，我們其實也和人類一樣。","nicolas")
			self.conversation_control.print_word("尼古拉", "魔力強的就是高貴、差的就是卑賤，這就魔族世世代代的傳統。","nicolas")
			self.conversation_control.print_word("勇者", "亡靈族不是蠻強的嗎？為什麼會說是卑賤？","player")
			self.conversation_control.print_word("尼古拉", "不！他們完全沒有魔力，他們靠的只是強大的肉體。\n真正的魔力強大的可以摧毀一切。","nicolas")
			self.conversation_control.print_word("勇者", "那既然魔力那麼強大，為何你們會打不過我們的祖先？","player")
			self.conversation_control.print_word("尼古拉", "。。。","nicolas")
			self.conversation_control.print_word("尼古拉", "。。。。。。","nicolas")
			self.conversation_control.print_word("尼古拉", "唉！我們魔族只害怕一個東西，聖寶石。","nicolas") 
			self.conversation_control.print_word("勇者", "聖寶石？那是什麼？","player")
			self.conversation_control.print_word("尼古拉", "聖寶石能吸收掉魔力，讓我們陷入虛弱。\n而我的魔力就是因為被亡靈族偷襲，而被聖寶石吸收掉。","nicolas")
			self.conversation_control.print_word("勇者", "原來如此，那麼公主被綁架大概就是被亡靈族給綁走的。","player")
			self.conversation_control.print_word("尼古拉", "應該是！據我所知，亡靈族相當的好色、繁殖能力也極強。\n你可能要動作加快，如果你希望你們公主可以安然無事的話。","nicolas") 
			self.conversation_control.print_word("勇者", "什麼？居然這樣！那請問你知道公主在哪裡嗎？","player")
			self.conversation_control.print_word("尼古拉", "我身無魔力，已經無法感知到魔塔了！\n如果你可以幫我找回那我的魔力，我就可以幫你找到公主。","nicolas") 
			self.conversation_control.print_word("勇者", "好！那聖寶石長什麼樣？","player")
			self.conversation_control.print_word("尼古拉", "一個白色十字架，中間有顆紅色的石頭，那便是聖寶石。\n小心不要摸到他，否則你會被內部蘊含的魔力反噬。","nicolas") 

			self.parameter["variables"]["saving_nicolas"] = True
		else:
			self.conversation_control.print_word("尼古拉", "你找到聖寶石了嗎？","nicolas")
			if "power_of_nicolas" not in self.parameter["variables"]:
				self.conversation_control.print_word("勇者", "還沒。","player")
			else:
				key = self.conversation_control.print_word("勇者", "（是否交給他）","player", prompt = "（Ｙ／Ｎ）", keys = [ord('y'), ord('n')])
				if key == ord('y'):
					self.conversation_control.print_word("勇者", "是這個嗎？","player")
					self.conversation_control.print_word("尼古拉", "對，沒錯。（恢復魔力）","nicolas") 
					self.conversation_control.print_word("尼古拉", "太棒了！我的魔力都回來了！真是謝謝你，年輕的勇士。","nicolas") 
					self.conversation_control.print_word("勇者", "那你可以感知到公主了嗎？","player")
					self.conversation_control.print_word("尼古拉", "可以，不過你等我一下，我要先去和那些低賤的亡靈族算帳。\n你到魔塔的最頂層找我。","nicolas") 
					self.parameter["variables"]["nicolas_recover"] = True
					self.status.expire()
				else:
					self.conversation_control.print_word("勇者", "還沒。","player")


