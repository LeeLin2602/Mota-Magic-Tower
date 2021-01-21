class NPC():
	def __init__(self, arg):
		self.count = 0
	def trigger(self):
		sword = self.parameter['sword']
 		
		if "artisan_2f_talk" not in self.parameter['variables']:
			self.parameter['variables']["artisan_2f_talk"] = 1
			self.conversation_control.print_word("工匠","感謝你救了我，我以前是一名鐵匠，如果有需要，我可以打折幫你看看武器。" , 'npc_2')
		if sword == -1:
			self.conversation_control.print_word("工匠","你手上一把武器都沒有，真不明白你怎麼會願意赤手空拳摸那些令人反胃的怪物！" , 'npc_2')
			return

		if sword == 48 and "artisan_48" not in self.parameter['variables']:
			key = self.conversation_control.print_word("工匠","一把生鏽的鐵劍？給我 15 塊，我就幫你打磨。", 'npc_2', prompt = "（Ｙ／Ｎ）", keys = [ord('y'), ord('n')])
			
			if key == ord('y') and self.cost("money", 15):
				self.status.cost("attack", 3)
				self.parameter['variables']["artisan_48"] = 1
				self.conversation_control.print_word("工匠","鋒利無比，你再用用看吧。", 'npc_2')
			elif key == ord('y'):
				self.conversation_control.print_word("工匠","你沒有足夠的錢！" , 'npc_2')

		elif sword == 49 and "artisan_49" not in self.parameter['variables']:
			
			key = self.conversation_control.print_word("工匠","一把騎士用的長劍？給我 35 塊，我就幫你拋光，這將對於吸血族有額外的傷害。", 'npc_2', prompt = "（Ｙ／Ｎ）", keys = [ord('y'), ord('n')])
			
			if key == ord('y') and self.cost("money", 35):
				self.parameter['variables']["artisan_49"] = 1
				self.conversation_control.print_word("工匠","金光閃閃。", 'npc_2')
			elif key == ord('y'):
				self.conversation_control.print_word("工匠","你沒有足夠的錢！" , 'npc_2')

		else:
			self.conversation_control.print_word("工匠","有需要我打磨的武器嗎？", 'npc_2')


		"""
		if 'trader_f1_buy' not in self.parameter['variables']:

			key = self.conversation_control.print_word("寶石商人","我這有一顆紅寶石，就賣你 15 塊錢", 'npc_2', prompt = "（Ｙ／Ｎ）", keys = [ord('y'), ord('n')])

			if key == ord('y') and self.cost("money", 15):
				self.status.cost("attack", -3)
				self.parameter['variables']["trader_f1_buy"] = True
			elif key == ord('y'):
				self.conversation_control.print_word("寶石商人","你沒有足夠的錢！" , 'npc_2')
		else:

			key = self.conversation_control.print_word("寶石商人","謝謝惠顧！我就祝你可以活久一點吧！哈哈哈～", 'npc_2')
		"""