from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *


class PlayerAI:
	def __init__(self):
		# Dictionary that maps direction to action
		self.direction_convert = {
			Direction.UP: "FACE_UP",
			Direction.DOWN: "FACE_DOWN",
			Direction.LEFT: "FACE_LEFT",
			Direction.RIGHT: "FACE_RIGHT",
			False: "NO_MOVE"
		}

		# Dictionary that converts string to API commands
		self.action_convert = {
			"FACE_UP": Move.FACE_UP,
			"FACE_DOWN": Move.FACE_DOWN,
			"FACE_LEFT" : Move.FACE_LEFT,
			"FACE_RIGHT": Move.FACE_RIGHT,
			"FORWARD": Move.FORWARD,
			"NO_MOVE": Move.NONE,
			"SHOOT": Move.SHOOT,
			"LASER": Move.LASER,
			"TELEPORT1": Move.TELEPORT_0,
			"TELEPORT2": Move.TELEPORT_2,
			"TELEPORT3": Move.TELEPORT_3,
			"TELEPORT4": Move.TELEPORT_4,
			"TELEPORT5": Move.TELEPORT_5
		}
		self.timer = 0
		self.turrets = []

	def get_move(self, gameboard, player, opponent):
		# LET'S DO THIS

		#increment turn count
		self.timer = self.timer + 1
		# first move to initialize positions of static turrets
		if (self.timer == 1):
			self.turrets = gameboard.turrets
			for turret in self.turrets:
				turret.killzone = turret_kill_zone(turret.x, turret.y, gameboard.width, gameboard.height)
				print(turret.killzone)
				turret.schedule = [turret.fire_time, turret.cooldown_time, turret.fire_time + turret.cooldown_time]

		return self.action_convert[find_move(self, gameboard, player, opponent)]


# HELPER METHODS #

# finds the best possible move
def find_move(self, gameboard, player, opponent):
	# defensive maneuvre decision tree
	defence = defensive_action(self, gameboard, player.x, player.y, 0)
	if (defence != "Safe"):
		return decide_direction(self.direction_convert, defence, player.direction)

	return "NO_MOVE"

	# else:
	# 	return "FACE_RIGHT"


# This shit is recursive backtracking, handle it like it's a fucking time bomb dude
# Recursively searches through all possible defensive maneuvres and returns the first possible one
# which will ensure survival for the next 2 turns
def defensive_action(self, gameboard, x, y, turn):
	# stop at depth 3, can increase if time permits
	if (turn == 3):
		return True

	if (is_hit(self, gameboard, x, y, turn)):
		print('is hit')
		return False

	# get possible directions that are not blocked by walls
	directions = possible_moves(self, gameboard, x, y)

	bullets = gameboard.bullets
	for bullet in bullets:
		if (bullet.y == y and get_x(gameboard.width, bullet.x + 1) - x > -3):
			if (bullet.direction == Direction.RIGHT):
				print("bullet coming from the left!")
				up = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn + 1)
				if (up and Direction.UP in directions):
					return Direction.UP
				down = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn + 1)
				if (down and Direction.DOWN in directions):
					return Direction.DOWN
				else:
					return False
		if (bullet.y == y and get_x(gameboard.width, bullet.x - 1) - x < 3):
			if (bullet.direction == Direction.LEFT):
				print("bullet coming from the right!")
				up = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn + 1)
				if (up and Direction.UP in directions):
					return Direction.UP
				down = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn + 1)
				if (down and Direction.DOWN in directions):
					return Direction.DOWN
				else:
					return False
		if (bullet.x == x and get_y(gameboard.height, bullet.y - 1) - y < 3):
			if (bullet.direction == Direction.UP):
				print("bullet coming from below!")
				left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn + 1)
				if (left and Direction.LEFT in directions):
					return Direction.LEFT
				right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn + 1)
				if (right and Direction.RIGHT in directions):
					return Direction.RIGHT
				else:
					return False
		if (bullet.x == x and get_y(gameboard.height, bullet.y + 1) - y > -3):
			if (bullet.direction == Direction.DOWN):
				print("bullet coming from above!")
				left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn + 1)
				if (left and Direction.LEFT in directions):
					return Direction.LEFT
				right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn + 1)
				if (right and Direction.RIGHT in directions):
					return Direction.RIGHT
				else:
					return False

	lethal_turrets = find_lethal_turrets(self, x, y)
	for turret in lethal_turrets:
		if (turret_will_fire(turret, turn + self.timer)):
			if (turret.y == y):
				up = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn + 1)
				if (up and Direction.UP in directions):
					return Direction.UP
				down = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn + 1)
				if (down and Direction.DOWN in directions):
					return Direction.DOWN
			if (turret.x == x):
				left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn + 1)
				if (left and Direction.LEFT in directions):
					return Direction.LEFT
				right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn + 1)
				if (right and Direction.RIGHT in directions):
					return Direction.RIGHT

	if (turn == 0):
		return "Safe"
	else:
		return True

# returns True if player will be hit at (x, y) at a particular turn
def is_hit(self, gameboard, x, y, turn):
	turrets = find_lethal_turrets(self, x, y)
	for turret in turrets:
		if (turret_will_fire(turret, self.timer + turn)):
			return True
	return False

# returns True if turret is designated to fire at the given turn
def turret_will_fire(turret, turn):
	cycle = turret.schedule[2]
	fire = turret.schedule[0]
	if (turn % cycle < fire):
		print("will fire: ")
		print(True)
		return True
	else:
		print("will fire: ")
		print(False)
		return False

# returns an array of turrets in range of player at turn
def find_lethal_turrets(self, x, y):
	lethal_turrets = []
	for turret in self.turrets:
		if ([x,y] in turret.killzone):
			lethal_turrets.append(turret)
	return lethal_turrets

# returns a decision for which direction the player should turn
def decide_direction(map, tile_to_move, current_direction):
	if (tile_to_move == current_direction):
		return "FORWARD"
	else:
		return map[tile_to_move]

# returns an array containing the kill zone of a turret when it fires
def turret_kill_zone(x, y, width, height):
	killzone = []
	temp_x = x - 4
	for i in range(-4, 5):
		if (temp_x != 0):
			killzone.append([get_x(width, temp_x), y])
		temp_x = temp_x + 1
	temp_y = y - 4
	for i in range(-4, 5):
		if (temp_y != 0):
			killzone.append([x, get_y(height, temp_y)])
		temp_y = temp_y + 1
	return killzone

# returns the new x-coordinate after a move which compensates for wrap effect
def get_x(width, next_move):
	if (next_move > width - 1):
		return next_move - width
	elif (next_move < 0):
		return width + next_move
	else:
		return next_move

# returns the new y-coordinate after a move which compensates for wrap effect
def get_y(height, next_move):
	if (next_move > height - 1):
		return next_move - height
	elif (next_move < 0):
		return height + next_move
	else:
		return next_move

# returns array with all possible moves
def possible_moves(self, gameboard, x, y):
	moves = []
	if (not gameboard.is_wall_at_tile(get_x(gameboard.width, x + 1), y)):
		moves.append(Direction.RIGHT)
	if (not gameboard.is_wall_at_tile(get_x(gameboard.width, x - 1), y)):
		moves.append(Direction.LEFT)
	if (not gameboard.is_wall_at_tile(x, get_y(gameboard.height, y - 1))):
		moves.append(Direction.UP)
	if (not gameboard.is_wall_at_tile(x, get_y(gameboard.height, y + 1))):
		moves.append(Direction.DOWN)
	return moves
