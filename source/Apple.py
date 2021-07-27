import pygame
from Snake import Snake
from random import randint
from typing import Tuple

class Apple:
	def __init__(self, snake: Snake, golden=False):
		self.score_value: int = 1 if not golden else 3
		self.position: Tuple[int, int]
		self.consumer: Snake = snake
		self.asset_image: pygame.Surface

		self.initialize_assets()
		self.generate_position()

	def initialize_assets(self) -> None:
		apple_image: pygame.Surface = pygame.image.load("../assets/objects_asset.png").subsurface((30, 0), (60, 30))
		self.asset_image = apple_image.subsurface(
			((0, 0), (30, 30)) if self.score_value == 1 else ((30, 0), (30, 30))
		)

	def generate_position(self) -> None:
		apple_interrupted: bool = True
		while apple_interrupted:
			self.position = (
				randint(0, self.consumer.grid_size_y - 2),
				randint(0, self.consumer.grid_size_x - 2)
			)
			apple_interrupted = (
				self.position in [self.consumer.head_pos, self.consumer.tail_pos]
				or self.position in self.consumer.body_pos
			)

	def consumed(self) -> bool:
		return self.position in self.consumer.body_pos or self.position == self.consumer.head_pos
	
	def add_consumed_score(self) -> None:
		self.consumer.score += self.score_value