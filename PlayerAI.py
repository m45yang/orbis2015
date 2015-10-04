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
			True: "NO_MOVE"
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

		# first move to initialize positions of static turrets
		if (self.timer == 0):
			self.turrets = gameboard.turrets
			for turret in self.turrets:
				turret.killzone = turret_kill_zone(turret.x, turret.y, gameboard.width, gameboard.height)

		return self.action_convert[find_move(self, gameboard, player, opponent)]


# HELPER METHODS #

# finds the best possible move
def find_move(self, gameboard, player, opponent):
	# defensive maneuvre decision tree
	defence = defensive_action(self, gameboard, player.x, player.y)
	if (defence):
		return decide_direction(self.direction_convert, defence, player.direction)

	# if player.direction in directions:
	# 	return "SHOOT"

	# else:
	# 	return "FACE_RIGHT"


# This shit is recursive backtracking, handle it like it's a fucking time bomb dude
# Recursively searches through all possible defensive maneuvres and returns the first possible one
# which will ensure survival for the next 2 turns
def defensive_action(self, gameboard, x, y):
	# get possible directions that are not blocked by walls
	directions = possible_moves(self, gameboard, x, y)

	bullets = gameboard.bullets
	for bullet in bullets:
		if (bullet.y == y and get_x(gameboard.width, bullet.x + 1) - x < 3):
			if (bullet.direction == Direction.RIGHT):
				print("bullet coming from the left!")
				up = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1))
				if (up and Direction.UP in directions):
					return Direction.UP
				down = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1))
				if (down and Direction.DOWN in directions):
					return Direction.DOWN
				else:
					return False
		if (bullet.y == y and get_x(gameboard.width, bullet.x - 1) - x < -3):
			if (bullet.direction == Direction.LEFT):
				print("bullet coming from the right!")
				up = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1))
				if (up and Direction.UP in directions):
					return Direction.UP
				down = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1))
				if (down and Direction.DOWN in directions):
					return Direction.DOWN
				else:
					return False
		if (bullet.x == x and get_y(gameboard.height, bullet.y - 1) - y < 3):
			if (bullet.direction == Direction.UP):
				print("bullet coming from below!")
				right = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y)
				if (right and Direction.RIGHT in directions):
					return Direction.RIGHT
				left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y)
				if (left and Direction.LEFT in directions):
					return Direction.LEFT
				else:
					return False
		if (bullet.x == x and get_y(gameboard.height, bullet.y + 1) - y < -3):
			if (bullet.direction == Direction.DOWN):
				print("bullet coming from above!")
				right = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y)
				if (right and Direction.RIGHT in directions):
					return Direction.RIGHT
				left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y)
				if (left and Direction.LEFT in directions):
					return Direction.LEFT
				else:
					return False

	return True

# returns a decision for which direction the player should turn
def decide_direction(map, tile_to_move, current_direction):
	if (tile_to_move == current_direction):
		return "FORWARD"
	else:
		return map[tile_to_move]

# returns an array containing the kill zone of a turret when it fires
def turret_kill_zone(x, y, width, height):
	killzone = []
	x = x - 4
	y = y - 4
	for i in range(-4, 4):
		x = x + 1
		y = y + 1
		if (x != 0 and y != 0):
			killzone.append([get_x(width, x), get_y(width, y)])
	return killzone

# returns the new x-coordinate after a move which compensates for wrap effect
def get_x(width, next_move):
	if (next_move > width - 1):
		return 0
	elif (next_move < 0):
		return width - 1
	else:
		return next_move

# returns the new y-coordinate after a move which compensates for wrap effect
def get_y(height, next_move):
	if (next_move > height - 1):
		return 0
	elif (next_move < 0):
		return height - 1
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
	print(moves)
	return moves
