import pygame
import time
from game_objects import Snake, Apple
from the_snake.field_settings import DOWN, SPEED, UP, LEFT, RIGHT, clock


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
