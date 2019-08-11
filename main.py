import sys
import pygame
import time
import json
from random import random as rnd
from enum import Enum

class o_type(Enum):
	effect  = -2
	scene 	= -1
	ground 	= 0
	wall 	= 1
	monster = 2
	npc 	= 3

	up_floor 	= 4
	down_floor 	= 5

	door = 6
	barrier = 7

	item = 8


class d_type(Enum):
	yellow = 0
	blue   = 1
	red    = 2
	magic  = 3

class atk_type(Enum):
	physic = 0
	magic  = 1
	poisonous = 2
	double = 3
	triple = 4

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
	"player": "resources/勇者/down 0.png"
}

monsters = {}
monster = json.load(open("data/monsters_data.json"))
floors = {}

for i in monster['monster']:
	monsters[i['id']] = i

parameter = {'highest_floor': 0,'this_floor': 0, 'lower_floor': 0}

parameter['level'] 		= 1
parameter['health'] 	= 1000
parameter['attack'] 	= 90
parameter['defence'] 	= 10
parameter['agility'] 	= 1
parameter['money'] 		= 0

parameter['0_key']  = 1
parameter['1_key']  = 1
parameter['2_key']  = 1

parameter['sword']  = 52
parameter['shield']  = -1

parameter['is_poisoning'] = False

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

	def fly(self):
		global this_floor, parameter

		objects = []
		objects.append(object(self.screen, "resources/字/fgt_box.png", 13, 13, o_type = o_type.scene, multiple = 1))

		now = this_floor.this_floor

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_KP_ENTER:
						jump(self.screen, now)
						break
					elif event.key == pygame.K_UP:
						if now < parameter['highest_floor']:
							now += 1
					elif event.key == pygame.K_DOWN:
						if now > parameter['lower_floor']:
							now -= 1

					

				update_screen(screen, grounds + information + scenes + [this_floor, warrior] + conversation_control.objects)
				time.sleep(0.075)

	def illustration(self):
		pass

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
		

		i = 1
		if attack_type == atk_type.double.value:
			i = 2
		elif attack_type == atk_type.triple.value:
			i = 3

		j = i

		counter = 3
		this_scenes = []
		this_scenes.append(object(self.screen, "resources/字/fgt_box.png", 13, 13, o_type = o_type.scene, multiple = 1))
		this_scenes.append(text_object(self.screen, font.render(str(name) , True , (255,255,255)), (2, 1.3)))
		this_scenes.append(text_object(self.screen, font.render(str("勇者") , True , (255,255,255)), (9.5, 1.3)))
		this_scenes.append(text_object(self.screen, font.render("ATK： " + str(atk) , True , (255,255,255)), (2, 5.2)))
		this_scenes.append(text_object(self.screen, font.render("ATK： " + str(parameter['attack']) , True , (255,255,255)), (9, 5.2)))
		this_scenes.append(text_object(self.screen, font.render("DFS： " + str(dfs) , True , (255,255,255)), (2, 5.9)))
		this_scenes.append(text_object(self.screen, font.render("DFS： " + str(parameter['defence']) , True , (255,255,255)), (9, 5.9)))
		
		effects = []

		while self.in_fighting and ((hp > 0 and parameter['health'] > 0) or (counter < 4 or 4 < counter < 9)):

			objects = []

			objects.append(object(self.screen, monster.path , 4, 6, dynamic = True, o_type = o_type.scene, multiple = 3))
			objects.append(object(self.screen, icons['player'], 11, 6, o_type = o_type.scene, multiple = 3))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == ord("q"):
					self.quit()

			if counter == 4:
				if rnd() > (agl - parameter['agility'] / 3)/100:
					if rnd() < (parameter['agility'] - agl / 3)/100:
						hp -= max(parameter['attack'] - dfs, 0) * 2					
						if parameter['sword'] != -1:
							play_audio("critical_cut")
							effects.append(effect(self.screen, "resources/攻擊/sword" + str(parameter['sword']) + " %s.png", 4, 6, dynamic = True, o_type = o_type.effect, multiple = 1))
						else:
							play_audio("critical_hit")
							effects.append(effect(self.screen, "resources/攻擊/hit %s.png", 4, 6, dynamic = True, o_type = o_type.effect, multiple = 1))

					else:
						hp -= max(parameter['attack'] - dfs, 0)			
						if parameter['sword'] != -1:
							play_audio("cut")
							effects.append(effect(self.screen, "resources/攻擊/sword" + str(parameter['sword']) + " %s.png", 4, 6, dynamic = True, o_type = o_type.effect, multiple = 1))
						else:
							play_audio("hit")
							effects.append(effect(self.screen, "resources/攻擊/hit %s.png", 4, 6, dynamic = True, o_type = o_type.effect, multiple = 1))


					hp = max(hp, 0)
				else:
					play_audio("miss")
			
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
				if rnd() > (parameter['agility'] - dexterity / 3)/100:
					if rnd() < (dexterity - parameter['agility'] / 3)/100:
						parameter['health'] -= max(atk - parameter['defence'], 0) * 2
						play_audio("critical_" + sound)
						effects.append(effect(self.screen, "resources/攻擊/" + img + " %s.png", 11, 6, dynamic = True, o_type = o_type.effect, multiple = 1))
					else:
						parameter['health'] -= max(atk - parameter['defence'], 0)
						play_audio(sound)
						effects.append(effect(self.screen, "resources/攻擊/" + img + " %s.png", 11, 6, dynamic = True, o_type = o_type.effect, multiple = 1))
					parameter['health'] = max(parameter['health'], 0)
				else:
					play_audio("miss")

			objects.append(text_object(self.screen, font.render("HP： " + str(hp) , True , (255,255,255)), (2, 4.5)))
			objects.append(text_object(self.screen, font.render("HP： " + str(parameter['health']) , True , (255,255,255)), (9, 4.5)))

			update_screen(self.screen, grounds + information + scenes + [warrior] + this_floor.objects + this_scenes + objects + effects)

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
		global warrior
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					warrior.vector = [1, 0, 0]
				elif event.key == pygame.K_LEFT:
					warrior.vector = [-1,0, 1]
				if event.key == pygame.K_DOWN:
					warrior.vector = [0, 1, 2]
				elif event.key == pygame.K_UP:
					warrior.vector = [0,-1, 3]
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
		global this_floor, grounds, information, scenes,warrior
		global conversation_control
		while conversation_control.in_conversation:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if keys == []:
						conversation_control.end_conversation()
						return event.key
					elif event.key in keys:
						conversation_control.end_conversation()
						return event.key
			update_screen(self.screen, grounds + information + scenes + [warrior] + this_floor.objects + conversation_control.objects)
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
			self.objects.append(object(self.screen, icons[path], 1.75, 11.25, o_type = o_type.scene, multiple = 1.5))

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

def cost(item, amount):
	if parameter[item] >= amount:
		parameter[item] -= amount
		if item == "money":
			play_audio("gold")
		else:
			if amount > 0: 
				play_audio("yes")
		return True
	print("error")
	play_audio("error")
	return False

class object(): 
	def __init__(self, screen, path, x , y,dynamic = False, o_type = o_type.ground, multiple = 1.5, arg = {}, script = None, floor = None):
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

		self.o_type = o_type

		self.location = [x,y]

		self.script = script

		self.init2(arg)

	def init2(self, arg):
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
			self.script.status = self
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
		global conversation_control

		self.script.conversation_control = conversation_control

		self.name = arg["name"]
		if self.script != None:
			self.script.status = self
			self.script.__init__(self.script, arg)

	def trigger(self):
		if self.script != None:
			global warrior
			warrior.vector = [0, 0, warrior.vector[2]]
			warrior.counter = 0

			self.script.trigger(self.script)
			return False
	def cost(self, item, amount):
		return cost(item, amount)

class door(object):
	def init2(self, parameter):
		self.d_type = parameter['d_type']
		self.parameter = parameter
		self.is_open = False
		self.count   = 0
	def trigger(self):
		if not self.is_open:
			if not self.d_type == 3:
				if cost(str(self.d_type) + "_key", 1):
					self.is_open = True
					play_audio("open_door")
				return False
			else:
				if self.script!=None:
					if self.script.trigger():
						self.is_open = True
						play_audio("open_door")
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
			path = "resources/地形/門/" + ["黃","藍","紅","魔法"][self.d_type] + " %s.png" % self.count
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
		self.config = data['config']
		self.this_floor = data['floor']
		self.objects 	= []
		self.up_floor   = (0, 0)
		self.down_floor = (0, 0)

		self.tags = {}

		for i in range(1,14):
			for j in range(1,14):
				if self.scene[i - 1][j - 1] == 1:
					self.objects.append(object(screen, "resources/地形/wall.png", j, i, o_type = o_type.wall))

				elif self.scene[i - 1][j - 1] == 2:
					self.objects.append(object(screen, "resources/地形/wall 2.png", j, i, o_type = o_type.wall))

				elif self.scene[i - 1][j - 1] == 3:
					self.objects.append(object(screen, "resources/地形/wall 3.png", j, i, o_type = o_type.wall))

				elif self.scene[i - 1][j - 1] == 4:
					self.down_floor = (j, i)
					if not data['config']['prev_floor'] == None:
						self.objects.append(object(screen, "resources/地形/down_floor.png", j, i, o_type = o_type.down_floor))

				elif self.scene[i - 1][j - 1] == 5:
					self.up_floor = (j, i)
					if not data['config']['next_floor'] == None:
						self.objects.append(object(screen, "resources/地形/up_floor.png", j, i, o_type = o_type.up_floor))

				elif type(self.scene[i - 1][j - 1]) == dict and self.scene[i - 1][j - 1]['o_type'] == o_type.npc.value:
					module = __import__("scripts." + self.scene[i - 1][j - 1]['program'])
					exec("global NPC; NPC = module." + self.scene[i - 1][j - 1]['program'] + ".NPC")
					path = "resources/NPC/" + ["仙女", "老人", "商人", "盜賊"][self.scene[i - 1][j - 1]["npc_type"]] + " %s.png"

					self.objects.append(npc(screen, path , j, i, dynamic = True, o_type = o_type.npc, arg = self.scene[i - 1][j - 1], script = NPC))

				elif type(self.scene[i - 1][j - 1]) == dict and self.scene[i - 1][j - 1]['o_type'] == o_type.monster.value:
					module = __import__("scripts." + self.scene[i - 1][j - 1]['program'])
					exec("global MST; MST = module." + self.scene[i - 1][j - 1]['program'] + ".monster;")
					path = "resources/怪物/" + str(self.scene[i - 1][j - 1]["m_type"] - 2000) + ",%s.png"

					self.objects.append(monster(screen, path , j, i, dynamic = True, o_type = o_type.monster, arg = {"m_type": self.scene[i - 1][j - 1]["m_type"] - 2000}, script = MST))

				elif type(self.scene[i - 1][j - 1]) == dict and self.scene[i - 1][j - 1]['o_type'] == o_type.door.value:
					if 'program' in self.scene[i - 1][j - 1]:
						module = __import__("scripts." + self.scene[i - 1][j - 1]['program'])
						exec("global DR; DR = module." + self.scene[i - 1][j - 1]['program'] + ".monster")
					else:
						DR = None
					path = "resources/地形/門/" + ["黃","藍","紅","魔法"][self.scene[i - 1][j - 1]["d_type"]] + " 0.png"

					self.objects.append(door(screen, path , j, i, o_type = o_type.door, arg = self.scene[i - 1][j - 1] , script = DR))

					if 'tag' in self.scene[i - 1][j - 1]:
						self.tags[self.scene[i - 1][j - 1]['tag']] = self.objects[-1]

				elif 62 >= self.scene[i - 1][j - 1] >= 60:
					self.objects.append(door(screen, "resources/地形/門/%s 0.png" % (["黃","藍","紅"][self.scene[i - 1][j - 1] - 60]), j, i, o_type = o_type.door, arg = {"d_type": self.scene[i - 1][j - 1] - 60}))
				
				elif 71 >= self.scene[i - 1][j - 1] >= 70:
					self.objects.append(object(screen, "resources/地形/" + (["lava","star"][self.scene[i - 1][j - 1] - 70]) + " %s.png", j, i, dynamic = True, o_type = o_type.wall))
				
				elif 900 > self.scene[i - 1][j - 1] >= 800:
					self.objects.append(item(screen, "resources/道具/%s.pdng" % str(self.scene[i - 1][j - 1] - 800), j, i, o_type = o_type.item, arg = {'i_type': self.scene[i - 1][j - 1] - 800}))
				elif self.scene[i - 1][j - 1] >= 2000:
					self.objects.append(monster(screen, "resources/怪物/" + str(self.scene[i - 1][j - 1] % 1000) + ",%s.png", j, i, dynamic = True, o_type = o_type.monster, arg = {'m_type': self.scene[i - 1][j - 1] % 1000}))

				self.objects[-1].floor = self
				
	def blitme(self):
		for i in self.objects:
			i.blitme()

class item(object):
	def init2(self, arg):
		self.i_type = arg['i_type']

	def trigger(self):
		if self.i_type == 0:
			parameter['attack'] += 2
		if self.i_type == 1:
			parameter['defence'] += 2
		if self.i_type == 2:
			parameter['agility'] += 1
		if self.i_type == 4:
			parameter['health'] += 200
		if self.i_type == 5:
			parameter['health'] += 400
		if self.i_type == 15: 
			parameter['health'] *= 2
		if self.i_type == 16:
			parameter['0_key'] += 1
		if self.i_type == 17:
			parameter['1_key'] += 1
		if self.i_type == 18:
			parameter['2_key'] += 1
		if self.i_type == 19:
			parameter['0_key'] += 1
			parameter['1_key'] += 1
			parameter['2_key'] += 1
		if self.i_type == 31:
			parameter['money'] += 300
		if self.i_type == 36:
			parameter['level'] += 1
			parameter['attack'] += 5
			parameter['defence'] += 3
		if self.i_type == 48:
			parameter['attack'] += 10
			parameter['sword'] = max(48, parameter['sword'])
		if self.i_type == 49:
			parameter['attack'] += 28
			parameter['sword'] = max(49, parameter['sword'])
		if self.i_type == 50:
			parameter['attack'] += 40
			parameter['sword'] = max(50, parameter['sword'])
		if self.i_type == 51:
			parameter['attack'] += 65
			parameter['sword'] = max(51, parameter['sword'])
		if self.i_type == 52:
			parameter['attack'] += 80
			parameter['sword'] = max(52, parameter['sword'])
		if self.i_type == 56:
			parameter['defence'] += 12
			parameter['shield'] = max(56, parameter['shield'])
		if self.i_type == 57:
			parameter['defence'] += 30
			parameter['shield'] = max(57, parameter['shield'])
		if self.i_type == 58:
			parameter['defence'] += 42
			parameter['shield'] = max(58, parameter['shield'])
		if self.i_type == 59:
			parameter['defence'] += 68
			parameter['shield'] = max(59, parameter['shield'])
		if self.i_type == 60:
			parameter['defence'] += 85
			parameter['shield'] = max(60, parameter['shield'])
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
				if i.o_type == o_type.up_floor:
					jump(self.screen, this_floor.config['next_floor'])
					return
				elif i.o_type == o_type.down_floor:
					jump(self.screen, this_floor.config['prev_floor'])
					return
				if not i.trigger():
					return

				
		self.location[0] += self.vector[0] 
		self.location[1] +=  self.vector[1] 

		if parameter['is_poisoning']:
			parameter['health'] -= 20
			if parameter['health'] <= 0:
				parameter['health'] = 1
			


def jump(screen, destination):
	global warrior, parameter, this_floor
	warrior.vector = [0, 0, warrior.vector[2]]

	if destination > parameter['highest_floor']:
		parameter['highest_floor'] = destination
		floors[parameter["this_floor"]] = this_floor
		this_floor = floors[destination]
		warrior.location = this_floor.down_floor
	elif destination < parameter['lower_floor']:
		parameter['lower_floor'] = destination
		floors[parameter["this_floor"]] = this_floor
		this_floor = floors[destination]
		warrior.location = this_floor.up_floor
	else:
		floors[parameter["this_floor"]] = this_floor
		this_floor = floors[destination]
		if destination < parameter["this_floor"]:
			warrior.location = this_floor.up_floor
		else:
			warrior.location = this_floor.down_floor

	warrior.location = list(warrior.location)
	parameter["this_floor"] = destination

def produce_number(screen, number,x ,y):
	c = []
	for i,j in enumerate(number):
		c.append(object(screen, "resources/字/%s.png" % j, x + 0.5 * i, y - 0.025, o_type = o_type.scene, multiple = 0.22))
	return c

def play_audio(path):
	if pygame.mixer.music.get_busy():
		pygame.mixer.music.stop()

	audio_player = pygame.mixer.music
	audio_player.load("resources/音效/" + path + ".mp3")
	audio_player.play()



def update_screen(screen, objects):
	for i in objects:
		i.blitme()
	pygame.display.flip()



pygame.init()

screen  = pygame.display.set_mode((int(576 * 1.5 + 144), int(480 * 1.5)))

conversation_control = conversation(screen)
fight_system = fight(screen)
key_system = key_event(screen)

grounds 	= []
scenes 		= []

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


for i in range(-6,15):
	for j in range(0,15):
		grounds.append(object(screen, "resources/地形/ground.png", i, j, o_type = o_type.ground))

warrior = player(screen)
pygame.display.set_caption("Mota")

f = json.load(open("data/floors_data.json"))

for i in f['floors']:
	floors[i['floor']] = floor(screen, i)

this_floor = floors[f["start"]]

warrior.location = list(f['location'])

del f

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

	update_screen(screen, grounds + information + scenes + [this_floor, warrior] + conversation_control.objects)
	time.sleep(0.075)