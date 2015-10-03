from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *


class PlayerAI:
	def __init__(self):
		# Initialize any objects or variables you need here.
		pass

	def get_move(self, gameboard, player, opponent):
		# LET'S DO THIS MOTHERFUCKERS

		# Dictionary that converts string to API commands
		action_convert = {
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

		return action_convert[find_move(self, gameboard, player, opponent)]




# finds the best possible move
def find_move(self, gameboard, player, opponent):
	directions = possible_moves(self, gameboard, player, opponent)

	if player.direction in directions:
		return "FORWARD"

	else:
		return "FACE_RIGHT"

# returns array with all possible moves
def possible_moves(self, gameboard, player, opponent):
	moves = []

	if (not gameboard.is_wall_at_tile(get_x(gameboard.width - 1, player.x + 1), player.y)):
		moves.append(Direction.RIGHT)
	if (not gameboard.is_wall_at_tile(get_x(gameboard.width - 1, player.x - 1), player.y)):
		moves.append(Direction.LEFT)
	if (not gameboard.is_wall_at_tile(player.x, get_y(gameboard.height - 1, player.y + 1))):
		moves.append(Direction.UP)
	if (not gameboard.is_wall_at_tile(player.x, get_y(gameboard.height - 1, player.y - 1))):
		moves.append(Direction.DOWN)

	return moves

def get_x(width, next_move):
	print(width)
	if (next_move > width):
		return 0
	elif (next_move < 0):
		return width
	else:
		return next_move

def get_y(height, next_move):
	if (next_move > height):
		return 0
	elif (next_move < 0):
		return height
	else:
		return next_move