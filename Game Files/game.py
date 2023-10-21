import pygame
import random
import time
import math
import os

pygame.init()
pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def asset_path(asset_name):
    base_path = os.path.abspath(os.path.dirname(__file__))
    asset_path = os.path.join(base_path, asset_name)
    if os.path.exists(asset_path):
        return asset_path
    return asset_name  

audio_on = True
#Adding Sounds:
correct_sound = pygame.mixer.Sound(asset_path('correct.wav'))
wrong_sound = pygame.mixer.Sound(asset_path('wrong.wav'))



if audio_on is True:
    pygame.mixer.music.load(asset_path('spooky_8bit.wav'))
    pygame.mixer.music.set_volume(0.15)  # 30% of the maximum volume
    pygame.mixer.music.play(-1)


# Our variables, subject to change
WIDTH, HEIGHT = 640, 640
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
SEQUENCE_LENGTH = 2  # Starting sequence length, starts at 2, increases by 1 for every score, making the game difficult
DISPLAY_TIME = 2  #Time initialized to one , this is the time the player sees a square, for every score the player gets, add -0.1 seconds of display time

# Halloween themed colors???
DARK_GRAY = (40, 40, 40)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

HALLOWEEN_COLORS = [ORANGE, PURPLE, GREEN]

#Adding highscore:

high_score = 0


difficulty = "Medium"

def generate_new_cell(last_cell=None):
    global GRID_SIZE
    new_cell = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    while new_cell == last_cell:
        new_cell = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    return new_cell

#pumpkin art
pumpkin_image = pygame.image.load(asset_path('carved_pumpkin.png'))
scaled_pumpkin = pygame.transform.scale(pumpkin_image, (CELL_SIZE, CELL_SIZE))

purple_ghost_image = pygame.image.load(asset_path('purple_ghost.png'))
scaled_ghost = pygame.transform.scale(purple_ghost_image, (CELL_SIZE, CELL_SIZE))

green_tombstone_image = pygame.image.load(asset_path('green_tomb.png'))
scaled_tombstone = pygame.transform.scale(green_tombstone_image, (CELL_SIZE, CELL_SIZE))

def draw_grid(highlighted_cells=[]):
    global GRID_SIZE
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = DARK_GRAY
            if (x, y) in highlighted_cells:
                color = HALLOWEEN_COLORS[highlighted_cells.index((x, y)) % len(HALLOWEEN_COLORS)]
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
            pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))
            
            if color == ORANGE:
                screen.blit(scaled_pumpkin, (x * CELL_SIZE, y * CELL_SIZE))
            
            if color == PURPLE:
                screen.blit(scaled_ghost, (x * CELL_SIZE, y * CELL_SIZE))
            
            if color == GREEN:
                screen.blit(scaled_tombstone, (x * CELL_SIZE, y * CELL_SIZE))


def get_cell_position(mouse_x, mouse_y):
    return mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

def draw_text(text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect

def update_settings_based_on_difficulty():
    global DISPLAY_TIME, SEQUENCE_LENGTH
    if difficulty == "Easy":
        DISPLAY_TIME = 2.0
        SEQUENCE_LENGTH = 2
    elif difficulty == "Medium":
        DISPLAY_TIME = 1.5
        SEQUENCE_LENGTH = 2
    else:  # Hard
        DISPLAY_TIME = 0.8
        SEQUENCE_LENGTH = 3

def start_screen():
    global audio_on, difficulty, GRID_SIZE
    
    #Adds and loads halloween horror logo image
    logo_image = pygame.image.load(asset_path('halloween_horror_logo.png'))
    logo_image = pygame.transform.scale(logo_image, (int(WIDTH * 0.7), int(HEIGHT * 0.5)))
    logo_rect = logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 3.5))

    amplitude = 15  # Amplitude of the bounce, in pixels
    speed = 2.5  # Speed of the bounce, higher is faster
    initial_y = logo_rect.topleft[1]



    start_game = False
    while not start_game:
        screen.fill(BLACK)

        # Logo in start menu
        screen.blit(logo_image, logo_rect.topleft)

        start_button = draw_text("Start", 40, WIDTH // 2, HEIGHT * 3 // 4, WHITE)
        exit_button = draw_text("Exit", 40, WIDTH // 2, HEIGHT * 3 // 4 + 50, WHITE)
        audio_button = draw_text(f"Audio: {'On' if audio_on else 'Off'}", 40, WIDTH // 2, HEIGHT * 3 // 4 - 50, WHITE)
        difficulty_button = draw_text(f"Difficulty: {difficulty}", 40, WIDTH // 2, HEIGHT * 3 // 4 - 100, WHITE)

        bounce_value = math.sin(pygame.time.get_ticks() * speed * 0.001) * amplitude
        logo_rect.topleft = (logo_rect.topleft[0], initial_y + bounce_value)

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
                    if audio_on:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                elif difficulty_button.collidepoint((x, y)):
                    if difficulty == "Easy":
                        difficulty = "Medium"
                    elif difficulty == "Medium":
                        difficulty = "Hard"
                    else:
                        difficulty = "Easy"
                    update_settings_based_on_difficulty()

def display_score():
    global difficulty
    global audio_on
    draw_text(f"Score: {score}", 30, WIDTH // 4, 10, PURPLE)  # Color set to PURPLE for the score
    draw_text(f"High Score: {high_score}", 30, 3 * WIDTH // 4, 10, GREEN)  # Color set to GREEN for the high score


#Loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption("Popping Pumpkins")
start_screen()

running = True
sequence = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(SEQUENCE_LENGTH)]
user_sequence = []
current_index = 0
score = 0

show_sequence = True

clock = pygame.time.Clock()  # Initialize the clock


def game_over_screen():

    logo_image = pygame.image.load(asset_path('quit_logo.png'))
    logo_image = pygame.transform.scale(logo_image, (int(WIDTH * 0.7), int(HEIGHT * 0.5)))
    logo_rect = logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    amplitude = 15  # Amplitude of the bounce, in pixels
    speed = 2.5  # Speed of the bounce, higher is faster
    initial_y = logo_rect.topleft[1]

    screen.fill(BLACK)
    draw_text("GAME OVER", 50, WIDTH // 2, HEIGHT // 2, ORANGE)
    restart_button = draw_text("Restart", 40, WIDTH // 2, HEIGHT * 3 // 4, WHITE)
    exit_button = draw_text("Exit", 40, WIDTH // 2, HEIGHT * 3 // 4 + 50, WHITE)

    pygame.display.flip()

    waiting_for_decision = True
    while waiting_for_decision:
        screen.fill(BLACK)

        bounce_value = math.sin(pygame.time.get_ticks() * speed * 0.001) * amplitude
        logo_rect.topleft = (logo_rect.topleft[0], initial_y + bounce_value)
        screen.blit(logo_image, logo_rect.topleft)

        draw_text("GAME OVER", 50, WIDTH // 2, HEIGHT // 2, ORANGE)
        restart_button = draw_text("Restart", 40, WIDTH // 2, HEIGHT * 3 // 4, WHITE)
        exit_button = draw_text("Exit", 40, WIDTH // 2, HEIGHT * 3 // 4 + 50, WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if restart_button.collidepoint((x, y)):
                    update_settings_based_on_difficulty()
                    waiting_for_decision = False
                elif exit_button.collidepoint((x, y)):
                    pygame.quit()
                    return

#Main game loop

while running:
    screen.fill(BLACK)
    display_score()
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not show_sequence:
            x, y = pygame.mouse.get_pos()
            cell_x, cell_y = get_cell_position(x, y)
            user_sequence.append((cell_x, cell_y))
            if user_sequence[-1] == sequence[len(user_sequence) - 1]:
                if audio_on:
                    correct_sound.play()
            else:
                if audio_on:
                    wrong_sound.play()
            if len(user_sequence) == SEQUENCE_LENGTH:
                if user_sequence == sequence:
                    if audio_on:
                        correct_sound.play()  # Adding Sound
                    score += 1          #Score tracking system.
                    if score > high_score:
                        high_score = score
                    SEQUENCE_LENGTH += 1  # Increase sequence length
                    
                    DISPLAY_TIME = max(0.1, DISPLAY_TIME - 0.2)  # Decrement DISPLAY_TIME, ensuring it doesn't go below 0.1
                else:
                    if audio_on:
                        wrong_sound.play()
                    game_over_screen()
                    score = 0  # Reset score to zero if sequence is incorrect
                    SEQUENCE_LENGTH = 2
                    DISPLAY_TIME = 2
                    
                last_update_time = pygame.time.get_ticks()  # Reset these two values
                update_delay = DISPLAY_TIME * 1000
                
                # Sequence generation modification
                sequence = [generate_new_cell()]
                for _ in range(1, SEQUENCE_LENGTH):
                    sequence.append(generate_new_cell(sequence[-1]))

                user_sequence = []
                show_sequence = True

    
    
    # Game Visuals
    # Inside the game loop:

    if show_sequence:
            # Simply draw and pause for DISPLAY_TIME seconds for each cell in the sequence
            for cell in sequence:
                draw_grid([cell])
                pygame.display.flip()  # Update the display after drawing each cell
                time.sleep(DISPLAY_TIME)  # Wait for DISPLAY_TIME seconds
            show_sequence = False  # After showing the entire sequence, set this to False
            user_sequence = []  # Prepare to receive the user's input
    else:
        draw_grid(user_sequence)  # Draw user's current sequence

    display_score()
    pygame.display.flip()
    clock.tick(60)


    #!!