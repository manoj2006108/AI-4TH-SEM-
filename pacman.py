import pygame
import sys

pygame.init()

# Settings
CELL_SIZE = 32
ROWS = 15
COLS = 19

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Maze
maze = [
    "###################",
    "#........#........#",
    "#.#####..#..#####.#",
    "#.................#",
    "#.###.#######.###.#",
    "#........#........#",
    "#####.##.#.##.#####",
    "#.................#",
    "#.#####.....#####.#",
    "#.......#.#.......#",
    "#.###.###.###.###.#",
    "#.................#",
    "#.#####.###.#####.#",
    "#........#........#",
    "###################"
]

# Player start
player_x = 1
player_y = 1

# Create pellets
pellets = set()

for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == ".":
            pellets.add((x, y))

score = 0

running = True

while running:

    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    new_x = player_x
    new_y = player_y

    if keys[pygame.K_LEFT]:
        new_x -= 1
    elif keys[pygame.K_RIGHT]:
        new_x += 1
    elif keys[pygame.K_UP]:
        new_y -= 1
    elif keys[pygame.K_DOWN]:
        new_y += 1

    if maze[new_y][new_x] != "#":
        player_x = new_x
        player_y = new_y

    if (player_x, player_y) in pellets:
        pellets.remove((player_x, player_y))
        score += 10

    screen.fill(BLACK)

    # Draw walls
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "#":
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                )

    # Draw pellets
    for px, py in pellets:
        pygame.draw.circle(
            screen,
            WHITE,
            (
                px * CELL_SIZE + CELL_SIZE // 2,
                py * CELL_SIZE + CELL_SIZE // 2
            ),
            4
        )

    # Draw player
    pygame.draw.circle(
        screen,
        YELLOW,
        (
            player_x * CELL_SIZE + CELL_SIZE // 2,
            player_y * CELL_SIZE + CELL_SIZE // 2
        ),
        CELL_SIZE // 2 - 2
    )

    # Score
    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (10, 10))

    # Win condition
    if len(pellets) == 0:
        win_text = font.render(
            "YOU WIN!",
            True,
            YELLOW
        )

        screen.blit(
            win_text,
            (
                WIDTH // 2 - 80,
                HEIGHT // 2
            )
        )

    pygame.display.flip()