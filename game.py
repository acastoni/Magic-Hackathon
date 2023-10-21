import pygame
import random
import time

pygame.init()

#Version 1.0
# Our variables, subject to change
WIDTH, HEIGHT = 640, 640
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
SEQUENCE_LENGTH = 2  # Starting sequence length, starts at 2, increases by 1 for every score, making the game difficult
DISPLAY_TIME = 1  #Time initialized to one , this is the time the player sees a square, for every score the player gets, add -0.1 seconds of display time

# Halloween themed colors???
DARK_GRAY = (40, 40, 40)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
HALLOWEEN_COLORS = [ORANGE, PURPLE, GREEN]

def draw_grid(highlighted_cells=[]):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = DARK_GRAY
            if (x, y) in highlighted_cells:
                color = HALLOWEEN_COLORS[highlighted_cells.index((x, y)) % len(HALLOWEEN_COLORS)]
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
            pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))

def get_cell_position(mouse_x, mouse_y):
    return mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

#Loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Halloween Horror")

running = True
sequence = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(SEQUENCE_LENGTH)]
user_sequence = []
current_index = 0
score = 0

show_sequence = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not show_sequence:
            x, y = pygame.mouse.get_pos()
            cell_x, cell_y = get_cell_position(x, y)
            user_sequence.append((cell_x, cell_y))
            if len(user_sequence) == SEQUENCE_LENGTH:
                if user_sequence == sequence:
                    score += 1
                    SEQUENCE_LENGTH += 1  # Increase sequence length
                    print(f"Correct Sequence! Score: {score}")
                    DISPLAY_TIME = max(0.1, DISPLAY_TIME - 0.1)  # Decrement DISPLAY_TIME, ensuring it doesn't go below 0.1
                else:
                    print(f"Wrong Sequence! Score: {score}")
                sequence = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(SEQUENCE_LENGTH)]
                user_sequence = []
                show_sequence = True

    # Game Visuals
    if show_sequence:
        if current_index < SEQUENCE_LENGTH:
            draw_grid([sequence[current_index]])
            pygame.display.flip()
            time.sleep(DISPLAY_TIME)
            current_index += 1
            draw_grid([])
            pygame.display.flip()
            time.sleep(0.3)
        else:
            current_index = 0
            show_sequence = False
    else:
        draw_grid(user_sequence)

    pygame.display.flip()

pygame.quit()
