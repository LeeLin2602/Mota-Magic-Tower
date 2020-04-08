from random import randint
from collections import deque
from enum import Enum


class randomList:
	def __init__(self, datas = []):
		self.datas = deque(datas)
		self.length = len(datas)

	def pop(self):

		if len(self.datas) == 0:
			raise IndexError("pop from empty list")

		index = randint(0, 1)
		if index ==  0: return self.datas.popleft()
		return self.datas.pop()

	def push(self, value):

		index = randint(0, 1)
		if index ==  0: self.datas.appendleft(value)
		self.datas.append(value)

	def is_empty(self):
		return len(self.datas) == 0


def create_maze(m, n, maze_map):
	visited  = [[0] * n for i in range(m)]

	queue = randomList()
	queue.push((0, 0, 0))

	while not queue.is_empty():
		i, j, f = queue.pop()

		if i >= m or j >= n or i < 0 or j < 0: continue
		if visited[i][j]: continue

		visited[i][j] = 1

		if f == 1:
			maze_map[i + 1][j] = 1
		if f == 2:
			maze_map[i - 1][j] = 1
		if f == 3:
			maze_map[i][j + 1] = 1
		if f == 4:
			maze_map[i][j - 1] = 1


		queue.push((i - 2, j, 1)) # From Right
		queue.push((i + 2, j, 2)) # From Left
		queue.push((i, j - 2, 3)) # From Down
		queue.push((i, j + 2, 4)) # From Up


class trigger():
	def __init__(self, arg = {}):
		pass

	def trigger(self):
		global maze_map
		this_floor = self.status

		if this_floor.ever_arrived:
			this_floor.objects = []
			this_floor.objects.append(this_floor.object_type(this_floor.screen, "resources/地形/4.png", 1, 1, o_type = this_floor.o_type.floor))
			this_floor.objects.append(this_floor.object_type(this_floor.screen, "resources/地形/5.png", 13, 13, o_type = this_floor.o_type.floor))

		m = n = 13

		maze_map = [[0] * n for i in range(m)]	# 0 is wall, 1 is road

		for i in range(0, m, 2):
			for j in range(0, n, 2):
				maze_map[i][j] = 1

		create_maze(m, n, maze_map)

		for i in range(13):
			for j in range(13):
				if maze_map[i][j] == 0:
					this_floor.objects.append(this_floor.object_type(this_floor.screen, "resources/地形/wall 2.png", j + 1, i + 1 , o_type = this_floor.o_type.wall))