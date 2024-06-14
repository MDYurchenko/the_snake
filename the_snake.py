from random import choice, randint

import pygame

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


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position):
        self.body_color = None
        self.position = position

    def draw(self):
        pass

class Snake(GameObject):

    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)] #
        self.position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.direction = (0, 1)
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def update_direction(self):
     if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None

    def move(self):
        self.last = self.positions[-1]
        if self.position[0] + 20*self.direction[0] > SCREEN_WIDTH:
            y = self.position[1]
            self.position = (0, y)
            self.positions[0] = (0, y)
        elif self.position[0] + 20*self.direction[0] < 0:
            y = self.position[1]
            self.position = (SCREEN_WIDTH, y)
            self.positions[0] = (SCREEN_WIDTH, y)
        elif self.position[1] + 20*self.direction[1] < 0:
            x = self.position[0]
            self.position = (x, SCREEN_HEIGHT)
            self.positions[0] = (x, SCREEN_HEIGHT)
        elif self.position[1] + 20 * self.direction[1] > SCREEN_HEIGHT:
            x = self.position[0]
            self.position = (x, 0)
            self.positions[0] = (x, 0)
        self.positions = [tuple([x + y for x, y in zip(self.positions[0], map(lambda x: x*20, self.direction))]),] + self.positions[:-1]
        print(self.positions)
        self.position = self.positions[0]


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
        self.length = 1
        self.positions = [(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)), ]
        self.direction = (1, 0)

class Apple(GameObject):
    def __init__(self):
        self.body_color = (255, 0, 0)
        self.position = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))

    def randomize_position(self):
        self.position = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

def handle_keys(game_object):
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

def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.

    snake = Snake()
    apple = Apple()

    #pygame.draw.rect(screen, (255, 255, 255), (10, 10, 10, 10))
    #pygame.display.update()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
