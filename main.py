# -*- coding:utf-8 -*-

import sys
import pygame
import time
import json

from random import random as rnd
from enum import Enum

import data.items

class o_type(Enum):
	effect  = -2
	scene 	= -1
	ground 	= 0
	wall 	= 1
	monster = 2
	npc 	= 3

	floor 	= 4
	trigger = 5

	door = 6
	barrier = 7

	item = 8
class d_type(Enum):
	yellow = 0
	blue   = 1
	red    = 2
	magic  = 3
	fence  = 4
class atk_type(Enum):
	physic = 0
	magic  = 1
	poisonous = 2
	double = 3
	triple = 4
	bloodsuck = 5

class npc_type(Enum):
	fairy	 = 0
	trader   = 1
	old_man  = 2
	thief    = 3

icons = {
	"npc_0" : "resources/NPC/仙女 0.png",
	"npc_1" : "resources/NPC/老人 0.png",
	"npc_2" : "resources/NPC/商人 0.png",
	"npc_3" : "resources/NPC/盜賊 0.png",
	"player": "resources/勇者/down 0.png"}

monsters = {}
monster = json.load(open("data/monsters_data.json", encoding="utf-8"))
floors = {}

for i in monster['monster']:
	monsters[i['id']] = i

variables = {}
parameter = {'this_floor': 0}

parameter['teleport_points'] = set(); parameter['level'] = 1; parameter['health'] = 1000; parameter['attack_method'] = atk_type.physic;
parameter['attack'] = 10; parameter['defence'] = 10; parameter['agility'] = 1; parameter['money'] = 200; 
parameter['0_key']  = 1; parameter['1_key']  = 1; parameter['2_key']  = 1
parameter['sword']  = -1; parameter['shield']  = -1; parameter['is_poisoning'] = False
parameter['tools'] = set()


class text_object():
	def __init__(self, screen, text, location):
		self.text = text
		self.location = location
		self.screen = screen
	def blitme(self):
		self.screen.blit(self.text, (self.location[0] * 48 + 336, self.location[1] * 48 + 96))

class tools():
	def __init__(self, screen):
		self.screen = screen

	def showMonsterInfo(self):
		global this_floor, parameter, floors, scenes, information

		monsters = []

		for i in this_floor.objects:
			if i.o_type == o_type.monster and i.valid:
				monster = (i.property['name'], i.property['path'], i.property['hp'], i.property['atk'], i.property['dfs'], i.property['money'], i.property['atk_type'], i.property['info'])
				if not monster in monsters:
					monsters.append(monster)
		
		monsters.sort(key = lambda x: int(x[1]))

		# Drawing

		gauss = lambda x: int(x) if float(int(x)) == float(x) else int(x) + 1
		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 20)
		
		t = 0

		while True:
			this_scenes = []

			for i in range(min(len(monsters) - t, 2)):
				if i + t < len(monsters):
					damage = 99999 if parameter['attack'] <= monsters[t + i][4] else max(0,monsters[t + i][3] - parameter["defence"]) * (gauss(monsters[t + i][2] / (parameter['attack'] - monsters[t + i][4])) - 1)
					
					if monsters[t + i][6] == atk_type.double.value:
						damage *= 2
					elif monsters[t + i][6] == atk_type.double.triple:
						damage *= 3

					this_scenes.append(object(self.screen, "resources/怪物/" + monsters[t + i][1] + ",0.png" , 3, 5 * i + 3.5, dynamic = False, o_type = o_type.scene, multiple = 2))
					this_scenes.append(text_object(self.screen, font.render(monsters[t + i][0] , True , (255,255,255)), (3.5, 5.2 * i + 0.25)))
					this_scenes.append(text_object(self.screen, font.render("生命: " + str(monsters[t + i][2]) , True , (255,255,255)), (3.5, 5.2 * i + 1)))
					this_scenes.append(text_object(self.screen, font.render("攻擊: " + str(monsters[t + i][3]) , True , (255,255,255)), (6, 5.2 * i + 1)))
					this_scenes.append(text_object(self.screen, font.render("防禦: " + str(monsters[t + i][4]) , True , (255,255,255)), (8.5, 5.2 * i + 1)))
					this_scenes.append(text_object(self.screen, font.render("金錢: " + str(monsters[t + i][5]) , True , (255,255,255)), (3.5, 5.2 * i + 1.75)))
					this_scenes.append(text_object(self.screen, font.render("預估傷害: " + str(damage), True , (255,255,255)), (8.5, 5.2 * i + 1.75)))
					if len(monsters[t + i][-1]) >= 13:
						this_scenes.append(text_object(self.screen, font.render("介紹: ", True , (255,255,255)), (3.5, 5.2 * i + 2.5)))
						for j in range(len(monsters[t + i][-1]) // 16 + 1):
							this_scenes.append(text_object(self.screen, font.render(monsters[t + i][-1][j * 16: j * 16 + 16], True , (255,255,255)), (4.5, 5.2 * i + 0.6 * j + 3.3)))
					else:
						this_scenes.append(text_object(self.screen, font.render("介紹: " + monsters[t + i][-1], True , (255,255,255)), (3.5, 5.2 * i + 2.5)))

			this_scenes.append(text_object(self.screen, font.render("(Q（或D） 退出； 左右鍵 翻頁)", True , (255,255,255)), (5.8, 11.2)))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						t = max(t - 2, 0)
					elif event.key == pygame.K_RIGHT:
						if t + 2 < len(monsters):
							t += 2
					if event.key == ord('q') or event.key == ord("d"):
						return

			self.screen.fill((0,0,0))
			update_screen(self.screen, scenes + information + this_scenes)
			time.sleep(0.0015)


	def fly(self):
		global this_floor, parameter, conversation_control, floors

		now = this_floor.this_floor
		
		t = list(parameter['teleport_points'])
		m = t.index(parameter['this_floor'])

		while True:
			key = conversation_control.print_word("","你要去 " + str(t[m]) + " 樓",keys = [ord('w'), ord('s'),ord('q'),ord("f"), 32])
			
			if key == ord('w'):
				if m + 1 <= len(t) - 1:
					m += 1
			elif key == ord("s"):
				if m - 1 >= 0:
					m -= 1
			elif key == 32: # ASCII(SPACE) = 32
				if t[m] >= parameter['this_floor']:
					if "from_lower" in floors[t[m]].config:
						jump(self.screen, t[m], floors[t[m]].config["from_lower"])
					else:
						conversation_control.print_word("","無法找到著陸點")
				else:
					if "from_upper" in floors[t[m]].config:
						jump(self.screen, t[m], floors[t[m]].config["from_upper"])
					elif "from_lower" in floors[t[m]].config:
						jump(self.screen, t[m], floors[t[m]].config["from_lower"])
					else:
						conversation_control.print_word("","無法找到著陸點")
				return
			else:
				return
				
class fight():
	def __init__(self, screen):
		self.screen = screen
		self.objects = []
		self.in_fighting = False

	def fight_with(self, monster):
		global this_floor, grounds, information, scenes,warrior
		self.in_fighting = True

		path, hp, atk, dfs, agl, name, money, attack_type, sound, dexterity, img = monster.property['path'], monster.property['hp'], monster.property['atk'], monster.property['dfs'], monster.property['agility'], monster.property['name'], monster.property['money'], monster.property['atk_type'], monster.property['sound'], monster.property['dex'], monster.property['img']
		
		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 24)
		font2 = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 18)
		
		add_hp = 0

		i = 1
		if attack_type == atk_type.double.value:
			i = 2
		elif attack_type == atk_type.triple.value:
			i = 3

		_attack_times = 1
		if parameter['attack_method'] == atk_type.double: _attack_times = 2
		if parameter['attack_method'] == atk_type.triple: _attack_times = 3

		j = i; _attack_times_left = _attack_times

		counter = 3
		this_scenes = []
		this_scenes.append(object(self.screen, "resources/字/fgt_box.png", 13, 14, o_type = o_type.scene, multiple = 1))
		this_scenes.append(text_object(self.screen, font.render(str(name) , True , (255,255,255)), (2, 1.3)))
		this_scenes.append(text_object(self.screen, font.render(str("勇者") , True , (255,255,255)), (9.5, 1.3)))
		this_scenes.append(text_object(self.screen, font.render("ATK： " + str(atk) , True , (255,255,255)), (2, 5.2)))
		this_scenes.append(text_object(self.screen, font.render("ATK： " + str(parameter['attack']) , True , (255,255,255)), (9, 5.2)))
		this_scenes.append(text_object(self.screen, font.render("DFS： " + str(dfs) , True , (255,255,255)), (2, 5.9)))
		this_scenes.append(text_object(self.screen, font.render("DFS： " + str(parameter['defence']) , True , (255,255,255)), (9, 5.9)))
		this_scenes.append(text_object(self.screen, font2.render("按下(Q)逃離戰鬥" , True , (255,255,255)), (9, 6.7)))
		message_timer = 5

		effects = []

		offset_monster = offset_player = 0

		while self.in_fighting and ((hp > 0 and parameter['health'] > 0) or (counter < 4 or 4 < counter < 9)):

			objects = []

			objects.append(object(self.screen, monster.path , 4 + offset_monster, 6, dynamic = True, o_type = o_type.scene, multiple = 3))
			objects.append(object(self.screen, icons['player'], 11 + offset_player, 6, o_type = o_type.scene, multiple = 3))


					
			if offset_player > 0:
				offset_player -= 0.3
			else: offset_player = 0

			if offset_monster > 0:
				offset_monster -= 0.3
			else: offset_monster = 0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == ord("q"):
					parameter['health'] = max(parameter['health'] - add_hp, 1)
					self.quit()

			if counter == 4:
				if rnd() > (agl - parameter['agility'])/110:
					if rnd() < (parameter['agility'] - agl)/110:
						hpcost = max(parameter['attack'] - dfs, 0) * 2					
						if parameter['sword'] != -1:
							play_audio("critical_cut")
							effects.append(effect(self.screen, "resources/攻擊/sword" + str(parameter['sword']) + " %s.png", 4, 6, dynamic = True, o_type = o_type.effect, multiple = 1))
						else:
							play_audio("critical_hit")
							effects.append(effect(self.screen, "resources/攻擊/hit %s.png", 4, 6, dynamic = True, o_type = o_type.effect, multiple = 1))

					else:
						hpcost = max(parameter['attack'] - dfs, 0)			
						if parameter['sword'] != -1:
							play_audio("cut")
							effects.append(effect(self.screen, "resources/攻擊/sword" + str(parameter['sword']) + " %s.png", 4, 6, dynamic = True, o_type = o_type.effect, multiple = 1))
						else:
							play_audio("hit")
							effects.append(effect(self.screen, "resources/攻擊/hit %s.png", 4, 6, dynamic = True, o_type = o_type.effect, multiple = 1))
					
					hp -= hpcost
						
					if parameter["attack_method"] == atk_type.bloodsuck:
						suckedBlood_amount += min(int(rnd() * 0.2 * hpcost * parameter['level'] / 10), hpcost * 0.8)
						parameter['health'] += suckedBlood_amount
						add_hp += suckedBlood_amount 

					hp = max(hp, 0)

					if _attack_times_left != 1:
						counter = 0
						_attack_times_left -= 1
					else:
						_attack_times_left = _attack_times
				else:
					play_audio("miss")
					offset_monster = 1.5
					if parameter['sword'] != -1:
						effects.append(effect(self.screen, "resources/攻擊/sword" + str(parameter['sword']) + " %s.png", 4, 6, dynamic = True, o_type = o_type.effect, multiple = 1))			
			
			if counter == 9 and j >= 0:
				if j == 0:
					j = i
					counter = 0
					continue
				else:
					j -= 1
					counter = 5

				if attack_type == atk_type.poisonous.value:
					if rnd() < 0.2:
						parameter['is_poisoning'] = True
				if rnd() > (parameter['agility'] - agl)/110:
					if rnd() < (dexterity - parameter['agility'])/110:
						parameter['health'] -= max(atk - parameter['defence'], 0) * 2
						if attack_type == atk_type.bloodsuck.value:
							hp += int(max(atk - parameter['defence'], 0) * 0.4 * rnd())
						play_audio("critical_" + sound)
						effects.append(effect(self.screen, "resources/攻擊/" + img + " %s.png", 11, 6, dynamic = True, o_type = o_type.effect, multiple = 1))
					else:
						if attack_type == atk_type.bloodsuck.value:
							hp += int(max(atk - parameter['defence'], 0) * 0.2 * rnd())
						parameter['health'] -= max(atk - parameter['defence'], 0)
						play_audio(sound)
						effects.append(effect(self.screen, "resources/攻擊/" + img + " %s.png", 11, 6, dynamic = True, o_type = o_type.effect, multiple = 1))
					parameter['health'] = max(parameter['health'], 0)
				else:
					offset_player = 1.5
					play_audio("miss")
					effects.append(effect(self.screen, "resources/攻擊/" + img + " %s.png", 11, 6, dynamic = True, o_type = o_type.effect, multiple = 1))



			if message_timer >= 0:
				message_timer -= 1
				if message_timer == -1:
					del this_scenes[-1]
			objects.append(text_object(self.screen, font.render("HP： " + str(hp) , True , (255,255,255)), (2, 4.5)))
			objects.append(text_object(self.screen, font.render("HP： " + str(parameter['health']) , True , (255,255,255)), (9, 4.5)))

			update_screen(self.screen, grounds + scenes + information + [warrior] + this_floor.objects + this_scenes + objects + effects)

			time.sleep(0.075)
			counter += 1

		objects = []

		if not self.in_fighting:
			return

		self.in_fighting = False
		if hp == 0:
			parameter['money'] += money
			monster.valid = False
			monster.visible = False
			return

		t = time.time()
		while time.time() - t <= 3:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

		self.screen.fill((0,0,0))

		object(self.screen, "resources/字/loss.png", 8, 8, o_type = o_type.scene, multiple = 1).blitme()
		pygame.display.flip()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			counter += 1
			time.sleep(0.075)


	def quit(self):
		self.in_fighting = False
		self.objects = []

class key_event():
	def __init__(self, screen):
		self.screen = screen

	def check_events(self, objs):
		global warrior, tools_system, this_floor,parameter
		for event in pygame.event.get():
			if event.type == pygame.QUIT:			# exit game
				sys.exit()
			if event.type == pygame.KEYDOWN:		# move control
				if event.key == pygame.K_RIGHT:
					warrior.vector = [1, 0, 0]
				elif event.key == pygame.K_LEFT:
					warrior.vector = [-1,0, 1]
				if event.key == pygame.K_DOWN:
					warrior.vector = [0, 1, 2]
				elif event.key == pygame.K_UP:
					warrior.vector = [0,-1, 3]

				# tools control: 
				
				if event.key == ord("f") and 'teleportation' in parameter['tools'] and this_floor.config['allow_teleport_out']:
					tools_system.fly()
					pygame.event.clear()
				if event.key == ord("d") and 'monsterPedia' in parameter['tools']:
					tools_system.showMonsterInfo()
					pygame.event.clear()

			elif event.type == pygame.KEYUP:

				if event.key == pygame.K_RIGHT:
					warrior.vector = [0, warrior.vector[1], warrior.vector[2]]
				elif event.key == pygame.K_LEFT:
					warrior.vector = [0, warrior.vector[1], warrior.vector[2]]
				if event.key == pygame.K_DOWN:
					warrior.vector = [warrior.vector[0], 0, warrior.vector[2]]
				elif event.key == pygame.K_UP:
					warrior.vector = [warrior.vector[0], 0, warrior.vector[2]]
		
		warrior.move(objs)

	def in_conversation(self, keys):
		global this_floor, grounds, information, scenes, warrior
		global conversation_control
		while conversation_control.in_conversation:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if keys == []:
						conversation_control.end_conversation()
						pygame.event.clear()
						return event.key
					elif event.key in keys:
						conversation_control.end_conversation()
						pygame.event.clear()
						play_audio("error")
						return event.key
			update_screen(self.screen, grounds + scenes + information + this_floor.objects + [warrior] + conversation_control.objects)
			time.sleep(0.075)


class conversation():
	def __init__(self, screen):
		self.in_conversation = False
		self.screen = screen
		self.objects = []
		self.queue = []

	def print_word(self, name, text, path = "",prompt = "", keys = []):
		global key_system

		if self.in_conversation:
			self.queue.append((name, text, path))
			return

		self.in_conversation = True
		self.objects.append(object(self.screen, "resources/字/msg_box.png", 13, 15, o_type = o_type.scene, multiple = 1))

		if path != "":
			if path in icons:
				self.objects.append(object(self.screen, icons[path], 1.75, 11.25, o_type = o_type.scene, multiple = 1.5))
			else:
				self.objects.append(object(self.screen, path, 1.75, 11.25, o_type = o_type.scene, multiple = 1.5))

		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 32)
		self.objects.append(text_object(self.screen, font.render(name , True , (255,255,255)), (2, 9.5)))
		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 20)
		self.objects.append(text_object(self.screen, font.render(text , True , (255,255,255)), (1, 10.5)))

		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 14)

		if prompt == "":
			if keys == []:
				self.objects.append(text_object(self.screen, font.render("按任意鍵退出" , True , (255,255,255)), (11, 11.5)))
			else:
				self.objects.append(text_object(self.screen, font.render("（" + "，".join([str(chr(i)) for i in keys]) + "）" , True , (255,255,255)), (11, 11.5)))
		else:
			self.objects.append(text_object(self.screen, font.render(prompt , True , (255,255,255)), (11, 11.5)))

		return key_system.in_conversation(keys)

	def end_conversation(self, key = -1):
		self.in_conversation = False

		if self.queue != []:
			arg = self.queue[0]
			del self.queue[0]
			self.print_word(arg[0], arg[1], arg[2])
		else:
			self.objects = []

def cost(item, amount, voice = True):
	if parameter[item] >= amount:
		parameter[item] -= amount
		if voice and item == "money":
			play_audio("gold")
		else:
			if voice and amount > 0: 
				play_audio("yes")
		return True

	if voice: play_audio("error")
	return False

class object(): 
	def __init__(self, screen, path, x , y,dynamic = False, o_type = o_type.ground, multiple = 1.5, arg = {}, script = None, floor = None):
		# RPG system

		self.script = script

		if script != None:
			global conversation_control, variables

			self.script.conversation_control = conversation_control
			self.variables = variables
			self.script.status = self

		# Initialize on canvas and map
		self.screen = screen

		self.floor = floor
		if path != "":
			self.visible = True
			self.valid   = True
			self.dynamic = dynamic
			if dynamic:
				self.counter = 0
				self.path = path
				image = pygame.image.load(path % 0)
				rect = image.get_rect()
				image = pygame.transform.scale(image, (int(rect.width * multiple), int(rect.height * multiple)))
				self.rect = image.get_rect()
			else:
				self.image = pygame.image.load(path)
				self.rect = self.image.get_rect()
				self.image = pygame.transform.scale(self.image, (int(self.rect.width * multiple), int(self.rect.height * multiple)))
				self.rect = self.image.get_rect()
		else:
			self.visible = False
			self.valid   = True

		self.o_type = o_type
		self.location = [x,y]

		self.init2(arg)

	def init2(self, arg): # Overwrite
		pass

	def trigger(self):
		if self.o_type == o_type.wall: 
			return False
		return True

	def blitme(self):
		if self.visible:
			self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
			self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height
			if self.dynamic:
				image = pygame.transform.scale(pygame.image.load(self.path % self.counter),(self.rect.width, self.rect.height))

				self.screen.blit(image, self.rect)

				self.counter += 1
				if self.counter == 4:
					self.counter = 0
			else:
				self.screen.blit(self.image, self.rect)

	# RPG system

	def cost(self, item, amount):
		return cost(item, amount)


class effect(object):
	def blitme(self):
		if self.visible:
			self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
			self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height
			if self.dynamic:
				image = pygame.transform.scale(pygame.image.load(self.path % self.counter),(self.rect.width, self.rect.height))

				self.screen.blit(image, self.rect)

				self.counter += 1
				if self.counter == 4:
					self.visible = False
			else:

				self.screen.blit(self.image, self.rect)


class monster(object):
	def init2(self, arg):
		global monsters
		self.property = monsters[arg["m_type"]]

		if self.script != None:
			self.script.__init__(self.script, arg)

	def trigger(self):
		global fight_system, warrior
		warrior.vector = [0, 0, warrior.vector[2]]
		warrior.counter = 0

		fight_system.fight_with(self)

		if self.script != None:
			self.script.trigger(self.script)


class npc(object):
	def init2(self, arg):
		self.name = arg["name"]
		if self.script != None:
			self.script.__init__(self.script, arg)

	def trigger(self):
		if self.script != None:
			global warrior
			warrior.vector = [0, 0, warrior.vector[2]]
			warrior.counter = 0

			self.script.trigger(self.script)
			return False

class game_trigger(object):
	def trigger(self):
		if self.script != None:
			t = self.script.trigger(self.script)
			if t == False:
				return False
		return True

class door(object):
	def init2(self, parameter):
		self.d_type = parameter['d_type']
		self.parameter = parameter
		self.is_open = False
		self.count   = 0

	def close(self):
		self.is_open = False
		self.visible = True
		self.count   = 0

		path = "resources/地形/門/" + ["黃","藍","紅","魔法","柵欄"][self.d_type] + " 0.png"
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (int(self.rect.width * 1.5), int(self.rect.height * 1.5)))
		self.rect = self.image.get_rect()

		play_audio("close_door")

	def open(self):
		self.is_open = True
		if self.d_type <= 3:
			play_audio("open_door")
		elif self.d_type == 4:
			play_audio("open_door2")

	def trigger(self):
		if not self.is_open:
			if not self.d_type >= 3:
				if cost(str(self.d_type) + "_key", 1, False):
					self.is_open = True
					play_audio("open_door")
				return False
			else:
				if self.script!=None:
					if self.script.trigger():
						self.is_open = True
						if self.d_type == 3:
							play_audio("open_door")
						elif self.d_type == 4:
							play_audio("open_door2")
					return False
				else:
					return False
		else:
			return not self.visible

	def blitme(self):
		if self.visible and not self.is_open:
			self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
			self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height

			self.screen.blit(self.image, self.rect)
		elif self.visible:
			self.count += 1
			if self.count == 4:
				self.visible = False
				return
			path = "resources/地形/門/" + ["黃","藍","紅","魔法","柵欄"][self.d_type] + " %s.png" % self.count
			self.image = pygame.image.load(path)
			self.rect = self.image.get_rect()
			self.image = pygame.transform.scale(self.image, (int(self.rect.width * 1.5), int(self.rect.height * 1.5)))
			self.rect = self.image.get_rect()

			self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
			self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height

			self.screen.blit(self.image, self.rect)

class floor():
	def __init__(self, screen, data):
		self.scene = data["scene"]

		if 'config' in data:
			self.config = data['config']
		else:
			self.config = {
				"allow_teleport_to": true,
				"allow_teleport_out": true
			}

		self.this_floor = data['floor']

		self.objects 	= []

		self.tags = {}
		self.floors = {}

		for i in range(1,14):
			for j in range(1,14):
				if type(self.scene[i - 1][j - 1]) == list:
					scene_datas = self.scene[i - 1][j - 1]
				else:
					scene_datas = [self.scene[i - 1][j - 1]]
				for scene_data in scene_datas:
					if scene_data == 1:
						self.objects.append(object(screen, "resources/地形/wall.png", j, i, o_type = o_type.wall))

					elif scene_data == 2:
						self.objects.append(object(screen, "resources/地形/wall 2.png", j, i, o_type = o_type.wall))

					elif scene_data == 3:
						self.objects.append(object(screen, "resources/地形/wall 3.png", j, i, o_type = o_type.wall))

					elif type(scene_data) == dict and scene_data['o_type'] == 4:
						self.floors[(j, i)] = (scene_data['goto'], scene_data['location'])

						if not "allow_teleport_to" in scene_data:
							if scene_data['goto'] > self.this_floor:
								self.config['from_upper'] = (j, i)
							else:
								self.config["from_lower"] = (j, i)

						self.objects.append(object(screen, "resources/地形/" + str(scene_data['img']) + ".png", j, i, o_type = o_type.floor))

					elif type(scene_data) == dict and scene_data['o_type'] == o_type.npc.value:
						module = __import__("scripts." + scene_data['program'])
						exec("global NPC; NPC = module." + scene_data['program'] + ".NPC")
						path = "resources/NPC/" + ["仙女", "老人", "商人", "盜賊"][scene_data["npc_type"]] + " %s.png"

						self.objects.append(npc(screen, path , j, i, dynamic = True, o_type = o_type.npc, arg = scene_data, script = NPC))

					elif type(scene_data) == dict and scene_data['o_type'] == o_type.monster.value:
						module = __import__("scripts." + scene_data['program'])
						exec("global MST; MST = module." + scene_data['program'] + ".monster;")
						path = "resources/怪物/" + str(scene_data["m_type"] - 2000) + ",%s.png"

						self.objects.append(monster(screen, path , j, i, dynamic = True, o_type = o_type.monster, arg = {"m_type": scene_data["m_type"] - 2000}, script = MST))
					
					elif type(scene_data) == dict and scene_data['o_type'] == o_type.trigger.value:
						module = __import__("scripts." + scene_data['program'])
						exec("global trigger; trigger = module." + scene_data['program'] + ".trigger;")
						path = scene_data['img'] if 'img' in scene_data else ''

						self.objects.append(game_trigger(screen, path , j, i, o_type = o_type.trigger, script = trigger))
			

					elif type(scene_data) == dict and scene_data['o_type'] == o_type.door.value:
						if 'program' in scene_data:
							module = __import__("scripts." + scene_data['program'])
							exec("global DR; DR = module." + scene_data['program'] + ".monster")
						else:
							DR = None
						path = "resources/地形/門/" + ["黃","藍","紅","魔法","柵欄"][scene_data["d_type"]] + " 0.png"

						self.objects.append(door(screen, path , j, i, o_type = o_type.door, arg = scene_data , script = DR))

					elif 62 >= scene_data >= 60:
						self.objects.append(door(screen, "resources/地形/門/%s 0.png" % (["黃","藍","紅"][scene_data - 60]), j, i, o_type = o_type.door, arg = {"d_type": scene_data - 60}))
					
					elif 71 >= scene_data >= 70:
						self.objects.append(object(screen, "resources/地形/" + (["lava","star"][scene_data - 70]) + " %s.png", j, i, dynamic = True, o_type = o_type.wall))
					
					elif 2000 > scene_data >= 1000:
						self.objects.append(item(screen, "resources/道具/%s.png" % str(scene_data - 1000), j, i, o_type = o_type.item, arg = {'i_type': scene_data - 1000}))
					elif scene_data >= 2000:
						self.objects.append(monster(screen, "resources/怪物/" + str(scene_data - 2000) + ",%s.png", j, i, dynamic = True, o_type = o_type.monster, arg = {'m_type': scene_data % 1000}))

					if type(scene_data) == dict and 'tag' in scene_data:
							self.tags[scene_data['tag']] = self.objects[-1]
					if type(scene_data) == dict and 'valid' in scene_data:
							self.objects[-1].valid = scene_data['valid']
					if type(scene_data) == dict and 'visible' in scene_data:
							self.objects[-1].visible = scene_data['visible']

					self.objects[-1].floor = self
				
	def blitme(self):
		for i in self.objects:
			i.blitme()

class item(object):
	def init2(self, arg):
		self.i_type = arg['i_type']

	def trigger(self):
		global conversation_control, item_system
		item_system.trigger(self.i_type)
		self.valid = False
		self.visible = False
		return True


class player(object):
	def __init__(self, screen):
		self.screen = screen

		self.counter = 0
		self.images = [[],[],[],[]]
		for i in range(4):
			self.images[0].append(pygame.transform.scale(pygame.image.load('resources/勇者/right %s.png' % i), (48, 48)))
			self.images[1].append(pygame.transform.scale(pygame.image.load('resources/勇者/left %s.png' % i), (48, 48)))
			self.images[2].append(pygame.transform.scale(pygame.image.load('resources/勇者/down %s.png' % i), (48, 48)))
			self.images[3].append(pygame.transform.scale(pygame.image.load('resources/勇者/up %s.png' % i), (48, 48)))
		self.rect = self.images[0][0].get_rect()
		self.vector = [0,0,2]

		self.location = [1,1]
		self.speed = 3

	def blitme(self):
		self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width/2
		self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height

		self.screen.blit(self.images[self.vector[2]][self.counter], self.rect)

	def move(self, objs):
		if self.vector[:2] != [0,0]:
			self.counter += 1
			if self.counter == 4:
				self.counter = 0
		else:
			return

		for i in objs:
			if i.valid and i.location == [self.location[0] + self.vector[0], self.location[1] + self.vector[1]]:
				if i.o_type == o_type.floor:
					t = this_floor.floors[(self.location[0] + self.vector[0], self.location[1] + self.vector[1])]
					jump(self.screen, t[0], t[1])
					return
				if not i.trigger():
					return

				
		self.location[0] += self.vector[0] 
		self.location[1] +=  self.vector[1] 

		if parameter['is_poisoning']:
			parameter['health'] -= 20
			if parameter['health'] <= 0:
				parameter['health'] = 1
			


def jump(screen, destination, location):
	global warrior, parameter, this_floor
	warrior.vector = [0, 0, warrior.vector[2]]

	if floors[destination].config['allow_teleport_to']:
		parameter['teleport_points'].add(destination)

		floors[parameter["this_floor"]] = this_floor
		this_floor = floors[destination]
		warrior.location = location

	warrior.location = list(warrior.location)
	parameter["this_floor"] = destination

def produce_number(screen, number,x ,y):
	c = []
	for i,j in enumerate(number):
		c.append(object(screen, "resources/字/%s.png" % j, x + 0.5 * i, y - 0.025, o_type = o_type.scene, multiple = 0.22))
	return c

def play_audio(path):
	global audio_player

	if audio_player.get_busy():
		audio_player.stop()

	audio_player.load("resources/音效/" + path + ".mp3")
	audio_player.play()


def update_screen(screen, objects):
	for i in objects:
		i.blitme()
	pygame.display.flip()



pygame.init()

screen  = pygame.display.set_mode((int(576 * 1.5 + 144), int(480 * 1.5)))
audio_player = pygame.mixer.music

conversation_control = conversation(screen)
fight_system = fight(screen)
key_system = key_event(screen)
tools_system = tools(screen)

grounds 	= []
scenes 		= []


for j in range(0,15):
	for i in range(-5,0):
		scenes.append(object(screen, "resources/地形/ground.png", i, j, o_type = o_type.ground))
	for i in range(0,15):
		grounds.append(object(screen, "resources/地形/ground.png", i, j, o_type = o_type.ground))


for i in range(-6,0):
	scenes.append(object(screen, "resources/地形/wall 3.png", i,  0, o_type = o_type.scene))
	scenes.append(object(screen, "resources/地形/wall 3.png", i, 14, o_type = o_type.scene))
	scenes.append(object(screen, "resources/地形/wall 3.png", i, 7, o_type = o_type.scene))

for i in range(15):
	scenes.append(object(screen, "resources/地形/wall 3.png", i,  0, o_type = o_type.wall))
	scenes.append(object(screen, "resources/地形/wall 3.png", i, 14, o_type = o_type.wall))
	scenes.append(object(screen, "resources/地形/wall 3.png", 0,  i, o_type = o_type.wall))
	scenes.append(object(screen, "resources/地形/wall 3.png", 14, i, o_type = o_type.wall))
	scenes.append(object(screen, "resources/地形/wall 3.png", -6, i, o_type = o_type.scene))

scenes.append(object(screen, "resources/勇者/down 0.png", -4.5, 1.25, o_type = o_type.scene))
scenes.append(object(screen, "resources/字/等级.png", -2.5, 0.75, o_type = o_type.scene,multiple = 1.2))

scenes.append(object(screen, "resources/字/体力.png", -3.5, 2, o_type = o_type.scene))
scenes.append(object(screen, "resources/字/攻击.png", -3.5, 3, o_type = o_type.scene))
scenes.append(object(screen, "resources/字/防御.png", -3.5, 4, o_type = o_type.scene))
scenes.append(object(screen, "resources/字/敏捷.png", -3.5, 5, o_type = o_type.scene))
scenes.append(object(screen, "resources/道具/16.png", -4.5, 9.5, o_type = o_type.scene))
scenes.append(object(screen, "resources/道具/17.png", -4.5, 10.5, o_type = o_type.scene))
scenes.append(object(screen, "resources/道具/18.png", -4.5, 11.5, o_type = o_type.scene))
scenes.append(object(screen, "resources/道具/31.png", -4.6, 12.5, o_type = o_type.scene))

warrior = player(screen)
pygame.display.set_caption("Mota")

f = json.load(open("data/floors_data.json", encoding="utf-8"))

for i in f['floors']:
	floors[i['floor']] = floor(screen, i)

this_floor = floors[f["start"]]
parameter['teleport_points'].add(f['start'])

warrior.location = list(f['location'])

del f

item_system = data.items.items(parameter, play_audio, conversation_control)


while True:
	if not conversation_control.in_conversation:
		key_system.check_events(scenes + this_floor.objects)

	information = (produce_number(screen, str(parameter['level']), -2.1, 1) + 
		   produce_number(screen, str(parameter['health']), -3, 2) + 
		   produce_number(screen, str(parameter['attack']), -3, 3) + 
		   produce_number(screen, str(parameter['defence']), -3, 4) + 
		   produce_number(screen, str(parameter['agility']), -3, 5) +
		   produce_number(screen, str(parameter['0_key']), -3.5, 9) +
		   produce_number(screen, str(parameter['1_key']), -3.5, 10) +
		   produce_number(screen, str(parameter['2_key']), -3.5, 11) +
		   produce_number(screen, str(parameter['money']), -3.5, 12))

	if parameter['is_poisoning']:
		information.append(text_object(screen, pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 24).render(str("（中毒）") , True , (0,255,0)), (-4.1, -0.8)))
	if parameter['sword'] != -1:
		information.append(object(screen, "resources/道具/%s.png" % parameter['sword'], -4.5, 8.25, o_type = o_type.scene))
	if parameter['shield'] != -1:
		information.append(object(screen, "resources/道具/%s.png" % parameter['shield'], -2.5, 8.25, o_type = o_type.scene))

	update_screen(screen, grounds + scenes + information + [this_floor, warrior] + conversation_control.objects)
	time.sleep(0.075)