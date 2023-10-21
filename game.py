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
WHITE = (255, 255, 255)

HALLOWEEN_COLORS = [ORANGE, PURPLE, GREEN]

audio_on = True
difficulty = "Medium"

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

def draw_text(text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect

def start_screen():
    global audio_on, difficulty

    #Adds and loads halloween horror logo image
    logo_image = pygame.image.load('halloween_horror_logo.png')
    logo_image = pygame.transform.scale(logo_image, (int(WIDTH * 0.8), int(HEIGHT * 0.4)))
    logo_rect = logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    start_game = False
    while not start_game:
        screen.fill(BLACK)

        # Logo in start menu
        screen.blit(logo_image, logo_rect.topleft)

        start_button = draw_text("Start", 40, WIDTH // 2, HEIGHT * 3 // 4, WHITE)
        exit_button = draw_text("Exit", 40, WIDTH // 2, HEIGHT * 3 // 4 + 50, WHITE)
        audio_button = draw_text(f"Audio: {'On' if audio_on else 'Off'}", 40, WIDTH // 2, HEIGHT * 3 // 4 - 50, WHITE)
        difficulty_button = draw_text(f"Difficulty: {difficulty}", 40, WIDTH // 2, HEIGHT * 3 // 4 - 100, WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if start_button.collidepoint((x, y)):
                    start_game = True
                elif exit_button.collidepoint((x, y)):
                    pygame.quit()
                    return
                elif audio_button.collidepoint((x, y)):
                    audio_on = not audio_on
                elif difficulty_button.collidepoint((x, y)):
                    if difficulty == "Easy":
                        difficulty = "Medium"
                    elif difficulty == "Medium":
                        difficulty = "Hard"
                    else:
                        difficulty = "Easy"


#Loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Halloween Horror")

start_screen()

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
