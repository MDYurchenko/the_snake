from game_objects import *

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


def is_apple_cell(snake: Snake, apple: Apple):
    if snake.position == apple.position:
        apple.randomize_position()
        snake.eat_apple()

def main():
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        time.sleep(0.2)

        # Тут опишите основную логику игры.
        apple.draw()
        snake.draw()

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        is_apple_cell(snake, apple)

        pygame.display.update()


if __name__ == '__main__':
    main()
