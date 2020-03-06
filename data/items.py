class items:
	def __init__(self, parameter, play_audio, conversation_control):
		self.parameter = parameter
		self.play_audio = play_audio
		self.conversation_control = conversation_control

	def trigger(self, i_type):
		self.i_type = i_type
		conversation_control = self.conversation_control
		play_audio = self.play_audio
		parameter = self.parameter

		if self.i_type == 0:
			parameter['attack'] += 2
			play_audio("error")
		if self.i_type == 1:
			parameter['defence'] += 2
			play_audio("error")
		if self.i_type == 2:
			parameter['agility'] += 1
			play_audio("error")
		if self.i_type == 4:
			parameter['health'] += 200
			play_audio("get")
		if self.i_type == 5:
			parameter['health'] += 400
			play_audio("get")
		if self.i_type == 15: 
			parameter['health'] *= 2
			play_audio("get")
		if self.i_type == 16:
			parameter['0_key'] += 1
			play_audio("error")
		if self.i_type == 17:
			parameter['1_key'] += 1
			play_audio("error")
		if self.i_type == 18:
			parameter['2_key'] += 1
			play_audio("error")
		if self.i_type == 19:
			parameter['0_key'] += 1
			parameter['1_key'] += 1
			parameter['2_key'] += 1
			play_audio("error")
		if self.i_type == 28:
			parameter['tools'].add("monsterPedia")
			play_audio("get")
			conversation_control.print_word("","- 得到怪物圖鑑，按下 <D> 查詢怪物訊息 -")
		if self.i_type == 31:
			parameter['money'] += 300
			play_audio("money")
		if self.i_type == 34:
			parameter['tools'].add("teleportation")
			play_audio("get")
			conversation_control.print_word("","- 得到飛天羅盤，按下 <F> 進行樓層跳躍 -")
			conversation_control.print_word("","- （W 上樓/S 下樓/Q（或F）） 放棄/Space 傳送） -")
		if self.i_type == 36:
			parameter['level'] += 1
			parameter['attack'] += 5
			parameter['defence'] += 3
			play_audio("get")
		if self.i_type == 48:
			parameter['attack'] += 10
			parameter['sword'] = max(48, parameter['sword'])
			play_audio("error")
		if self.i_type == 49:
			parameter['attack'] += 28
			parameter['sword'] = max(49, parameter['sword'])
			play_audio("error")
		if self.i_type == 50:
			parameter['attack'] += 40
			parameter['sword'] = max(50, parameter['sword'])
			play_audio("error")
		if self.i_type == 51:
			parameter['attack'] += 65
			parameter['sword'] = max(51, parameter['sword'])
			play_audio("error")
		if self.i_type == 52:
			parameter['attack'] += 80
			parameter['sword'] = max(52, parameter['sword'])
			play_audio("error")
		if self.i_type == 56:
			parameter['defence'] += 12
			parameter['shield'] = max(56, parameter['shield'])
			play_audio("error")
		if self.i_type == 57:
			parameter['defence'] += 30
			parameter['shield'] = max(57, parameter['shield'])
			play_audio("error")
		if self.i_type == 58:
			parameter['defence'] += 42
			parameter['shield'] = max(58, parameter['shield'])
			play_audio("error")
		if self.i_type == 59:
			parameter['defence'] += 68
			parameter['shield'] = max(59, parameter['shield'])
			play_audio("error")
		if self.i_type == 60:
			parameter['defence'] += 85
			parameter['shield'] = max(60, parameter['shield'])
			play_audio("error")
