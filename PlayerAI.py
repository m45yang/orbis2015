from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *


class PlayerAI:
	def __init__(self):
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

	def get_move(self, gameboard, player, opponent):
		# LET'S DO THIS
		return self.action_convert[find_move(self, gameboard, player, opponent)]


# HELPER METHODS #

# finds the best possible move
def find_move(self, gameboard, player, opponent):
	directions = possible_moves(self, gameboard, player, opponent)

	# defensive maneuvre decision tree
	defence = defensive_action(self, gameboard, player, directions)
	if (defence):
		return defence

	if player.direction in directions:
		return "SHOOT"

	else:
		return "FACE_RIGHT"

def defensive_action(self, gameboard, player, directions):
	bullets = gameboard.bullets
	for bullet in bullets:
		if (bullet.y == player.y and get_x(gameboard.width, bullet.x + 1) - player.x <= -1):
			if (bullet.direction == Direction.RIGHT):
				directions.remove(Direction.RIGHT)
				directions.remove(Direction.LEFT)
				if (player.direction == Direction.RIGHT or player.direction == Direction.LEFT):
					return "FACE_DOWN"
				else:
					return "FORWARD"
		if (bullet.y == player.y and get_x(gameboard.width, bullet.x - 1) - player.x <= 1):
			if (bullet.direction == Direction.LEFT):
				directions.remove(Direction.RIGHT)
				directions.remove(Direction.LEFT)
				if (player.direction == Direction.RIGHT or player.direction == Direction.LEFT):
					return "FACE_UP"
				else:
					return "FORWARD"
		if (bullet.x == player.x and get_y(gameboard.height, bullet.y + 1) - player.y <= -1):
			if (bullet.direction == Direction.UP):
				directions.remove(Direction.UP)
				directions.remove(Direction.DOWN)
				if (player.direction == Direction.UP or player.direction == Direction.DOWN):
					return "FACE_LEFT"
				else:
					return "FORWARD"
		if (bullet.x == player.x and get_y(gameboard.height, bullet.y + 1) - player.y <= 1):
			if (bullet.direction == Direction.DOWN):
				directions.remove(Direction.UP)
				directions.remove(Direction.DOWN)
				if (player.direction == Direction.UP or player.direction == Direction.DOWN):
					return "FACE_RIGHT"
				else:
					return "FORWARD"

		turrets = gameboard.turrets

	return False

def decide_direction(directions):
	return False


def get_x(width, next_move):
	if (next_move > width - 1):
		return 0
	elif (next_move < 0):
		return width - 1
	else:
		return next_move

def get_y(height, next_move):
	if (next_move > height - 1):
		return 0
	elif (next_move < 0):
		return height - 1
	else:
		return next_move


# returns array with all possible moves
def possible_moves(self, gameboard, player, opponent):
	moves = []

	if (not gameboard.is_wall_at_tile(get_x(gameboard.width, player.x + 1), player.y)):
		moves.append(Direction.RIGHT)
	if (not gameboard.is_wall_at_tile(get_x(gameboard.width, player.x - 1), player.y)):
		moves.append(Direction.LEFT)
	if (not gameboard.is_wall_at_tile(player.x, get_y(gameboard.height, player.y + 1))):
		moves.append(Direction.UP)
	if (not gameboard.is_wall_at_tile(player.x, get_y(gameboard.height, player.y - 1))):
		moves.append(Direction.DOWN)
	return moves