import pygame
from typing import List, Tuple, Dict

class Snake:
	def __init__(self, grid_size_y=15, grid_size_x=15) -> None:
		# Required so as to draw onto the window a grid-like playfield.
		self.grid_size_y = grid_size_y
		self.grid_size_x = grid_size_x
		self.tail_pos: Tuple[int, int] = (4, 4)
		self.head_pos: Tuple[int, int] = (4, 7)
		self.body_pos: List[Tuple[int, int]] = [(4, 5), (4, 6)]
		
		self.head_direction: str = "right"  # Graphical and mechanic-related feature
		self.tail_direction: str = "right"  # Graphical feature
		self.is_alive: bool = True
		self.score: int = 0
		
		# Customizable based on user input
		self.target_score: int = 0
		self.delay_between_move: float = 0.0
		
		self.assets: Dict[str, Dict[str, pygame.Surface]] = {}
		self.initialize_assets()

	def initialize_assets(self) -> None:
		PART_SIZE: int = 30
		PART_IMAGE_SIZE: Tuple[int, int] = (PART_SIZE * 3, PART_SIZE)
		SPRITE_SIZE: Tuple[int, int] = (PART_SIZE, ) * 2
		# Sprite sheet divided into columns and rows of different properties
		snake_parts_image: pygame.Surface = pygame.image.load("../assets/snake_asset.png")
		
		# Splicing 2D parts out of the master spritesheet.
		for y, part in enumerate(["head", "body", "tail"]):
			COORDINATES_Y: Tuple[int, int] = (0, y * PART_SIZE)
			part_image: pygame.Surface = snake_parts_image.subsurface(COORDINATES_Y, PART_IMAGE_SIZE)
			part_dict: Dict[str, pygame.Surface] = {}
			
			for x, status in enumerate(["alive", "dead", "win"]):
				COORDINATES_X: Tuple[int, int] = (x * PART_SIZE, 0)
				part_dict[status]: pygame.Surface = part_image.subsurface(COORDINATES_X, SPRITE_SIZE)
			self.assets[part]: Dict[str, pygame.Surface] = part_dict

	def get_asset(self, part: str, status: str, direction: str) -> pygame.Surface:
		# Pygame uses anti-clockwise rotation + default sprite direction = rightwards.
		def convert_to_direction(s: pygame.Surface, direction: str) -> pygame.Surface:
			if direction == "left":
				return pygame.transform.rotate(s, 180)
			elif direction == "up":
				return pygame.transform.rotate(s, 90)
			elif direction == "down":
				return pygame.transform.rotate(s, 270)
			elif direction == "right":
				return s

		return convert_to_direction(self.assets[part][status], direction)

	def moved_pos_offset(self) -> Tuple[int, int]:
		# Positional differences when moving one unit (or cell)
		if self.head_direction == "right":
			return 1, 0
		elif self.head_direction == "left":
			return -1, 0
		elif self.head_direction == "down":
			return 0, 1
		elif self.head_direction == "up":
			return 0, -1

	def update_tail_direction(self) -> None:
		# To be determined when updating the snake's tail, purely graphical feature.
		if self.body_pos[0][0] == self.body_pos[1][0]:
			self.tail_direction = ("up" if self.body_pos[0][1] == self.body_pos[1][1] + 1 else "down")
		elif self.body_pos[0][1] == self.body_pos[1][1]:
			self.tail_direction = ("left" if self.body_pos[0][0] == self.body_pos[1][0] + 1 else "right")

	def move_one_unit(self) -> None:
		self.update_tail_direction()
		self.tail_pos = self.body_pos.pop(0)
		# noinspection PyTypeChecker
		self.body_pos.append(self.head_pos)
		self.head_pos = tuple([self.head_pos[i] + self.moved_pos_offset()[i] for i in range(2)])

	def extend_by_one(self) -> None:
		# noinspection PyTypeChecker
		self.body_pos.append(self.head_pos)
		self.head_pos = tuple([self.head_pos[i] + self.moved_pos_offset()[i] for i in range(2)])

	def update_is_alive(self) -> None:
		def snake_not_in_border():
			return (
				self.head_pos[0] not in [self.grid_size_y - 1, -1]
				and self.head_pos[1] not in [self.grid_size_x - 1, -1]
			)
		def snake_not_in_itself():
			return self.head_pos not in self.body_pos and self.head_pos != self.tail_pos

		self.is_alive = snake_not_in_border() and snake_not_in_itself()

	def has_won(self) -> bool:
		return self.score >= self.target_score