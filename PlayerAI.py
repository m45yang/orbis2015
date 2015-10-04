from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *

# PeaceBot v1.0
# Creator: HardcoreEgg

class PlayerAI:
	def __init__(self):
		# Define how paranoid PeaceBot will be
		self.PARNOID_LEVEL = 6

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
				turret.schedule = [turret.fire_time, turret.cooldown_time, turret.fire_time + turret.cooldown_time]

		return self.action_convert[find_move(self, gameboard, player, opponent)]


# HELPER METHODS #

# finds the best possible move
def find_move(self, gameboard, player, opponent):
	# defensive maneuvre decision tree
	defence = defensive_action(self, gameboard, player.x, player.y, 0, player, opponent)
	if (defence != "Safe"):
		return decide_direction(self.direction_convert, defence, player.direction)

	return "NO_MOVE"


# This shit is recursive backtracking, handle it like it's a fucking time bomb dude
# Recursively searches through all possible defensive maneuvres and returns the first possible one
# which will ensure survival for the next 3 turns (hopefully)
def defensive_action(self, gameboard, x, y, turn, player, opponent):
	# stop at depth 3, can increase if time permits
	if (turn == 3):
		return True

	if (is_hit(self, gameboard, x, y, turn) and turn != 0):
		return False

	turn = turn + 1

	# get possible directions that are not blocked by walls
	directions = possible_moves(self, gameboard, x, y)

	# dodge turrets
	lethal_turrets = find_lethal_turrets(self, x, y)
	for turret in lethal_turrets:
		# turret will fire right when you land on the tile
		if (turret_will_fire(turret, turn - 2 + self.timer)):
			return False
		# turret about to fire this turn
		elif (turret_will_fire(turret, turn - 1 + self.timer)):
			if (turret.y == y):
				if (player.direction == Direction.UP):
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					return False
				elif (player.direction == Direction.DOWN):
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					return False
				else:
					return False
			if (turret.x == x):
				if (player.direction == Direction.LEFT):
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					return False
				elif (player.direction == Direction.RIGHT):
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					return False
				else:
					return False
		# turret about to fire next turn
		elif (turret_will_fire(turret, turn + self.timer)):
			if (turret.y == y):
				if (player.direction == Direction.UP):
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					return False
				elif (player.direction == Direction.DOWN):
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					return False
				else:
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					return False
			if (turret.x == x):
				if (player.direction == Direction.LEFT):
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					return False
				elif (player.direction == Direction.RIGHT):
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					return False
				else:
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					return False
	# dodge bullets
	bullets = gameboard.bullets
	for bullet in bullets:
		if (bullet.y == y and get_x(gameboard.width, bullet.x + turn) - x > -3 and get_x(gameboard.width, bullet.x + turn) - x < 0):
			if (bullet.direction == Direction.RIGHT):
				print("bullet coming from the left!")
				if (player.direction == Direction.UP):
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					return False
				if (player.direction == Direction.DOWN):
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					return False
				else:
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					return False
		if (bullet.y == y and get_x(gameboard.width, bullet.x - turn) - x < 3 and get_x(gameboard.width, bullet.x - turn) - x > 0):
			if (bullet.direction == Direction.LEFT):
				print("bullet coming from the right!")
				if (player.direction == Direction.UP):
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					return False
				if (player.direction == Direction.DOWN):
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					return False
				else:
					up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
					if (up and Direction.UP in directions):
						return Direction.UP
					down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
					if (down and Direction.DOWN in directions):
						return Direction.DOWN
					return False
		if (bullet.x == x and get_y(gameboard.height, bullet.y - turn) - y < 3 and get_y(gameboard.height, bullet.y - turn) - y > 0):
			if (bullet.direction == Direction.UP):
				print("bullet coming from below!")
				if (player.direction == Direction.LEFT):
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					return False
				if (player.direction == Direction.RIGHT):
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					return False
				else:
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					return False
		if (bullet.x == x and get_y(gameboard.height, bullet.y + turn) - y > -3 and get_y(gameboard.height, bullet.y + turn) - y < 0):
			if (bullet.direction == Direction.DOWN):
				print("bullet coming from above!")
				if (player.direction == Direction.LEFT):
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					return False
				if (player.direction == Direction.RIGHT):
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					return False
				else:
					left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
					if (left and Direction.LEFT in directions):
						return Direction.LEFT
					right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
					if (right and Direction.RIGHT in directions):
						return Direction.RIGHT
					return False

	# keep distance from opponent
	if (opponent.y == player.y and (abs(opponent.x - player.x) < self.PARNOID_LEVEL or (gameboard.width - abs(opponent.x - player.x)) < self.PARNOID_LEVEL)):
		if (player.direction == Direction.UP):
			up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
			if (up and Direction.UP in directions):
				return Direction.UP
			down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
			if (down and Direction.DOWN in directions):
				return Direction.DOWN
			return False
		if (player.direction == Direction.DOWN):
			down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
			if (down and Direction.DOWN in directions):
				return Direction.DOWN
			up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
			if (up and Direction.UP in directions):
				return Direction.UP
			return False
		else:
			up = defensive_action(self, gameboard, x, get_y(gameboard.height, y - 1), turn, player, opponent)
			if (up and Direction.UP in directions):
				return Direction.UP
			down = defensive_action(self, gameboard, x, get_y(gameboard.height, y + 1), turn, player, opponent)
			if (down and Direction.DOWN in directions):
				return Direction.DOWN
			return False
	elif (opponent.x == player.x and (abs(opponent.y - player.y) < self.PARNOID_LEVEL or (gameboard.height - abs(opponent.y - player.y)) < self.PARNOID_LEVEL)):
		if (player.direction == Direction.LEFT):
			left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
			if (left and Direction.LEFT in directions):
				return Direction.LEFT
			right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
			if (right and Direction.RIGHT in directions):
				return Direction.RIGHT
			return False
		if (player.direction == Direction.RIGHT):
			right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
			if (right and Direction.RIGHT in directions):
				return Direction.RIGHT
			left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
			if (left and Direction.LEFT in directions):
				return Direction.LEFT
			return False
		else:
			left = defensive_action(self, gameboard, get_x(gameboard.width, x - 1), y, turn, player, opponent)
			if (left and Direction.LEFT in directions):
				return Direction.LEFT
			right = defensive_action(self, gameboard, get_x(gameboard.width, x + 1), y, turn, player, opponent)
			if (right and Direction.RIGHT in directions):
				return Direction.RIGHT
			return False

	# if no move is required
	if (turn == 1):
		return "Safe"
	# went through a deep iterative check and there is no danger
	else:
		return True

# returns True if player will be hit at (x, y) at a particular turn
def is_hit(self, gameboard, x, y, turn):
	turrets = find_lethal_turrets(self, x, y)
	for turret in turrets:
		if (turret_will_fire(turret, self.timer + turn)):
			return True
	for bullet in gameboard.bullets:
		if (bullet.x == x and bullet.y == y):
			return True
	return False

# returns True if turret is designated to fire at the given turn
def turret_will_fire(turret, turn):
	cycle = turret.schedule[2]
	fire = turret.schedule[0]
	if (turn % cycle < fire):
		return True
	else:
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
	if (not gameboard.is_wall_at_tile(get_x(gameboard.width, x + 1), y) and not gameboard.turret_at_tile[get_x(gameboard.width, x + 1)][y]):
		moves.append(Direction.RIGHT)
	if (not gameboard.is_wall_at_tile(get_x(gameboard.width, x - 1), y) and not gameboard.turret_at_tile[get_x(gameboard.width, x - 1)][y]):
		moves.append(Direction.LEFT)
	if (not gameboard.is_wall_at_tile(x, get_y(gameboard.height, y - 1)) and not gameboard.turret_at_tile[x][get_y(gameboard.height, y - 1)]):
		moves.append(Direction.UP)
	if (not gameboard.is_wall_at_tile(x, get_y(gameboard.height, y + 1)) and not gameboard.turret_at_tile[x][get_y(gameboard.height, y + 1)]):
		moves.append(Direction.DOWN)
	return moves
