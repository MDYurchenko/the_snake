from random import randrange
import time
from field_settings import *
# Тут опишите все классы игры.
class GameObject:
    def __init__(self):
        self.body_color = None
        self.position = None

    def draw(self):
        pass


class Snake(GameObject):

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
        if self.position in self.positions[1:]:
            self.reset()

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def __check_edge(self):
        next_position = tuple([snake_coord + speed_proection for snake_coord, speed_proection
                               in zip(self.position, map(lambda coord: coord * SPEED, self.direction))])
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
        self.length += 1
        self.positions += [self.last]
        self.last = None

    def move(self):
        self.__check_edge()
        self.last = self.positions[-1]
        self.positions = [self.position] + self.positions[:-1]
        self.__check_eat_yourself()

    def draw(self):
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
        return self.positions[0]

    def reset(self):
        for body_cell in self.positions:
            body_rect = pygame.Rect(body_cell, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, body_rect)
        self.length = 1
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.position = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
        self.direction = (1, 0)
        time.sleep(1)


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE), randrange(0, SCREEN_HEIGHT, GRID_SIZE))

    def randomize_position(self):
        self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE), randrange(0, SCREEN_HEIGHT, GRID_SIZE))

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)