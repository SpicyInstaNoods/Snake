import pygame
import pygame_widgets as pygame_w
from time import sleep
from Snake import Snake
from Apple import Apple
from typing import Optional, Union, List, Tuple, Dict

class Game:
	def __init__(self, grid_size_y:int=15, grid_size_x:int=15) -> None:
		self.gameplay_size: Tuple[int, int] = ((grid_size_x + 1) * 30, (grid_size_y + 1) * 30)
		self.display_surface: pygame.Surface = pygame.display.set_mode((400, 600))
		pygame.display.set_caption("Snake")
		pygame.display.set_icon(pygame.image.load("../assets/snake_asset.png").subsurface((0, 0), (30, 30)))
		self.number_assets: Dict[str, pygame.Surface] = {}
		self.player_snake: Snake = Snake(grid_size_y, grid_size_x)
		self.player_normal_apple: Optional[Apple] = None
		self.player_golden_apple: Optional[Apple] = None
		
		self.initialize_number_assets()
		self.set_input_difficulty()
		self.main_gameplay()
		
	def initialize_number_assets(self) -> None:
		# Extracting digits' images from a horizontal sprite sheet.
		number_sheet: pygame.Surface = pygame.image.load("../assets/number_asset.png")
		for num in range(10):
			COORDINATES: Tuple[int, int] = (num * 30, 0)
			SIZE: Tuple[int, int] = (30, 30)
			self.number_assets[str(num)] = number_sheet.subsurface(COORDINATES, SIZE)

	def draw_diff_select_screen(self) -> None:
		# Two difficulty details panes displayed simultaneously for users to choose one difficulty.
		score_select: pygame.Surface = pygame.image.load("../assets/score_select.png")
		speed_select: pygame.Surface = pygame.image.load("../assets/speed_select.png")
		
		self.display_surface.blit(score_select, (0, 0))
		self.display_surface.blit(speed_select, (200, 0))
		
		pygame.display.update()
		
	def set_input_difficulty(self) -> None:
		def approx_mouse_pos() -> int:
			DIFF_SPRITE_SIZE: int = 200
			mouse_pos_x: int = pygame.mouse.get_pos()[1]
			return (mouse_pos_x - (mouse_pos_x % DIFF_SPRITE_SIZE)) // DIFF_SPRITE_SIZE
		
		self.draw_diff_select_screen()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit(0)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					diff_details: List[Tuple[int, float]] = [(30, 0.25), (60, 0.1), (120, 0.05)]
					selected_diff_pos: int = approx_mouse_pos()
					
					self.player_snake.target_score = diff_details[selected_diff_pos][0]
					self.player_snake.delay_between_move = diff_details[selected_diff_pos][1]
					return

	@staticmethod
	def conv_direction(value: Union[int, str]) -> Union[str, int]:
		if type(value) is int:
			values: Dict[int, str] = {
				pygame.K_RIGHT: "right",
				pygame.K_UP: "up",
				pygame.K_LEFT: "left",
				pygame.K_DOWN: "down"
			}
			return values[value]
		elif type(value) is str:
			values: Dict[str, int] = {
				"right": pygame.K_RIGHT,
				"up": pygame.K_UP,
				"down": pygame.K_LEFT,
				"left": pygame.K_DOWN
			}
			return values[value]

	def validate_direction_input(self, event) -> str:
		directions: List[int] = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]
		if event.key in directions:
			str_direction: str = self.conv_direction(event.key)
			# Prevent the snake from rotating its head 180 degrees.
			if str_direction == "right" and self.player_snake.head_direction != "left":
				return str_direction
			elif str_direction == "left" and self.player_snake.head_direction != "right":
				return str_direction
			elif str_direction == "up" and self.player_snake.head_direction != "down":
				return str_direction
			elif str_direction == "down" and self.player_snake.head_direction != "up":
				return str_direction
		# Unchanged result if above conditions not met.
		return self.player_snake.head_direction

	def draw_waiting_enter_keypress(self) -> None:
		# Acts as a kind of cue of what to do when meeting certain conditions.
		enter_image: pygame.Surface = pygame.image.load("../assets/press_enter_signal.png")
		self.display_surface.blit(
			enter_image, ((self.player_snake.grid_size_x - 5) * 30, (self.player_snake.grid_size_y - 5) * 30)
		)
		pygame.display.update()

	def draw_playing_grid(self) -> None:
		# Drawing separate components.
		def draw_background() -> None:
			BLACK: Tuple[int, int, int, int] = (0, 0, 0, 255)
			GREY: Tuple[int, int, int, int] = (211, 211, 211, 255)
			self.display_surface.fill(BLACK)
			
			# Filling the screen with black cells with grey border.
			for i in range(self.player_snake.grid_size_y):
				for j in range(self.player_snake.grid_size_x):
					COORDINATES: Tuple[int, int] = ((i + 1) * 30, (j + 1) * 30)
					NET_SHAPE_SIZE: Tuple[int, int] = (31, 31)
					pygame.draw.rect(self.display_surface, GREY, COORDINATES + NET_SHAPE_SIZE, 1)

		def draw_wall() -> None:
			#Bordering the screen with predefined border sprite.
			wall_texture: pygame.Surface = pygame.image.load("../assets/objects_asset.png").subsurface((0, 0), (30, 30))
			for i in range(self.player_snake.grid_size_x + 1):
				for j in (0, self.player_snake.grid_size_y):
					COORDINATES: Tuple[int, int] = (i * 30, j * 30)
					self.display_surface.blit(wall_texture, COORDINATES)

			for i in (0, self.player_snake.grid_size_x):
				for j in range(self.player_snake.grid_size_y + 1):
					COORDINATES: Tuple[int, int] = (i * 30, j * 30)
					self.display_surface.blit(wall_texture, COORDINATES)

		def draw_apple() -> None:
			if not (self.player_normal_apple is None):
				# noinspection PyTypeChecker
				COORDINATES: Tuple[int, int] = tuple([(n + 1) * 30 for n in self.player_normal_apple.position])
				self.display_surface.blit(self.player_normal_apple.asset_image, COORDINATES)

			if not (self.player_golden_apple is None):
				# noinspection PyTypeChecker
				COORDINATES: Tuple[int, int] = tuple([(n + 1) * 30 for n in self.player_golden_apple.position])
				self.display_surface.blit(self.player_golden_apple.asset_image, COORDINATES)

		def draw_snake() -> None:
			STATUS: str = "win" if self.player_snake.has_won() else ("alive" if self.player_snake.is_alive else "dead")
			# noinspection PyTypeChecker
			HEAD_COORDS: Tuple[int, int] = tuple([(n + 1 )* 30 for n in self.player_snake.head_pos])
			self.display_surface.blit(
				self.player_snake.get_asset(
					"head", STATUS, self.player_snake.head_direction
				), HEAD_COORDS
			)
			
			# noinspection PyTypeChecker
			TAIL_COORDS: Tuple[int, int] = tuple([(n + 1) * 30 for n in self.player_snake.tail_pos])
			self.display_surface.blit(
				self.player_snake.get_asset(
					"tail", STATUS, self.player_snake.tail_direction
				), TAIL_COORDS
			)
			
			for pos in self.player_snake.body_pos:
				# noinspection PyTypeChecker
				BODY_COORDS: Tuple[int, int] = tuple([(n + 1) * 30 for n in pos])
				self.display_surface.blit(
					self.player_snake.get_asset(
						"body", STATUS, "right"
					), BODY_COORDS
				)

		def draw_score() -> None:
			# Draw score in relation to the grid size.
			raw_score: str = str(self.player_snake.score)
			x_dimension: int = self.player_snake.grid_size_x // 2
			if len(raw_score) == 3:
				self.display_surface.blit(self.number_assets[raw_score[0]], ((x_dimension - 1) * 30, 0))
				self.display_surface.blit(self.number_assets[raw_score[1]], (x_dimension * 30, 0))
				self.display_surface.blit(self.number_assets[raw_score[2]], ((x_dimension + 1) * 30, 0))
			else:
				if len(raw_score) == 1:
					raw_score = "0" + raw_score
				self.display_surface.blit(self.number_assets[raw_score[0]], (x_dimension * 30, 0))
				self.display_surface.blit(self.number_assets[raw_score[1]], ((x_dimension + 1) * 30, 0))

		draw_background()
		draw_wall()
		draw_apple()
		draw_snake()
		draw_score()
		pygame.display.flip()
		pygame.display.update()

	@staticmethod
	def wait_final_input() -> None:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.display.quit()
					quit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
						return

	def update_apple(self) -> None:
		if not (self.player_normal_apple is None):
			if self.player_normal_apple.consumed():
				self.player_snake.extend_by_one()
				self.player_normal_apple.add_consumed_score()
				self.player_normal_apple = None
		
		if not (self.player_golden_apple is None):
			if self.player_golden_apple.consumed():
				self.player_golden_apple.add_consumed_score()
				self.player_golden_apple = None

	def generate_apple(self) -> None:
		if self.player_normal_apple is None:
			self.player_normal_apple = Apple(self.player_snake, False)
		if self.player_snake.score != 0:
			if self.player_snake.score % 6 == 0 and self.player_golden_apple is None:
				self.player_golden_apple = Apple(self.player_snake, True)

	def main_gameplay(self) -> None:
		pygame.init()
		self.display_surface = pygame.display.set_mode(self.gameplay_size)
		self.display_surface.fill((0, 0, 0, 0))
		pygame.display.update()

		self.draw_waiting_enter_keypress()
		self.wait_final_input()

		user_inputs: List[str] = []
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.display.quit()
					quit(0)
				elif event.type == pygame.KEYDOWN:
					user_inputs.append(self.validate_direction_input(event))
					break

			# Mechanism for handling multiple inputs in one event iteration
			if user_inputs:
				self.player_snake.head_direction = user_inputs.pop(0)

			self.generate_apple()
			self.update_apple()
			
			self.player_snake.update_is_alive()
			self.draw_playing_grid()
			sleep(self.player_snake.delay_between_move)

			self.player_snake.move_one_unit()

			if not self.player_snake.is_alive or self.player_snake.has_won():
				# Redraw screen to graphically output final result: defeat or victory.
				self.draw_playing_grid()
				self.draw_waiting_enter_keypress()
				self.wait_final_input()
				return
