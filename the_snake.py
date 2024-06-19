import pygame
import time
from random import randrange

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    This is a common class of game object. It creates a structure of
    child classes.
    body_color - color of object
    position - position of apple or head snake position
    """

    def __init__(self):
        self.body_color = None
        self.position = None

    def draw(self):
        """Used to draw object on game field. Override in child class."""


class Snake(GameObject):
    """The main object of the game, that is controlled by player."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.position = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
        self.last = None

        self.direction = (0, 1)
        self.next_direction = None

        self.body_color = SNAKE_COLOR

    def __check_eat_yourself(self):
        """
        Checks if snake head is at snake body cell.
        If so, restarts the game.
        Uses attributes: position and positions.
        """
        if self.position in self.positions[1:]:
            self.reset()

    def update_direction(self):
        """
        Sets direction of snake motion in next time tick
        if next_direction is not None.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def __check_edge(self):
        """
        Calculates new head position. If position isn't at game field,
        sets head position at the opposite side of
        game field.
        """
        next_position = tuple(
            [
                snake_coord + speed_projection for
                snake_coord, speed_projection in
                zip(
                    self.position,
                    map(lambda coord: coord * SPEED, self.direction)
                )
            ]
        )
        if next_position[0] < 0:
            self.position = (int(SCREEN_WIDTH - GRID_SIZE), next_position[1])
        elif next_position[0] >= SCREEN_WIDTH:
            self.position = (0, next_position[1])
        elif next_position[1] < 0:
            self.position = (next_position[0], int(SCREEN_HEIGHT - GRID_SIZE))
        elif next_position[1] >= SCREEN_HEIGHT:
            self.position = (next_position[0], 0)
        else:
            self.position = next_position

    def eat_apple(self):
        """
        Defines the logic of eating apple.
        Increases length of snake, not wash snake tail.
        """
        self.length += 1
        self.positions += [self.last]
        self.last = None

    def move(self):
        """
        Defines the logic of snake motion.
        Checks if snake head at the edge of game field,
        sets list of snake parts positions. Checks if snake eat yourself.
        :return:
        """
        self.__check_edge()
        self.last = self.positions[-1]
        self.positions = [self.position] + self.positions[:-1]
        self.__check_eat_yourself()

    def draw(self):
        """
        Overrides parent method. Draw head and body of snake.
        Wash last body cell.
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Get head position.
        :return: tuple of x, y snake head position
        """
        return self.positions[0]

    def reset(self):
        """
        Sets action executed at the game end:
        erase old snake, draw new snake.
        """
        for body_cell in self.positions:
            body_rect = pygame.Rect(body_cell, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, body_rect)
        self.length = 1
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.position = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
        self.direction = (1, 0)
        time.sleep(1)


class Apple(GameObject):
    """Apple object, that designed to be eaten by a snake"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))

    def randomize_position(self):
        """Sets random position of apple at game field."""
        self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))

    def draw(self):
        """Draws apple at game field."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object: Snake):
    """
    Handles keystrokes "up", "down", "left", "right", "Esc" on keyboard.
    Used to set next_direction for Snake.
    :param game_object: class instance that moves across the game field.
    Supposed Snake object.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def is_apple_cell(snake: Snake, apple: Apple):
    """
    Checks if snake head located at cell with apple.
    If so, spawn new apple, delete old apple
    and increase snake length by 1.
    :param snake: Snake instance
    :param apple: Apple instance
    """
    if snake.position == apple.position:
        apple.randomize_position()
        snake.eat_apple()


def main():
    """
    Initialize game. Create objects of classes Snake and Apple.
    Provide main game logic: snake and apple spawning,
    moving, interaction snake with the
    environment. Set the end of game condition.
    """
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        time.sleep(0.2)

        apple.draw()
        snake.draw()

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        is_apple_cell(snake, apple)

        pygame.display.update()


if __name__ == '__main__':
    main()
