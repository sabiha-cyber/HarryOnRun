import pygame
from sys import exit
from random import randint
from button import Button
import pygame_textinput
import json  # To save/load leaderboard data

# Initialize Pygame
pygame.init()

# Screen and Game Setup
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('hello/Daily Bubble.ttf', 50)

# Load Assets
BG = pygame.image.load("hello/Background.png")
sky_surface = pygame.image.load('hello/sky.png').convert()
ground_surface = pygame.image.load('hello/ground.png').convert()
man_surface = pygame.image.load('hello/Attack_1.png').convert_alpha()
fly_surf = pygame.transform.rotozoom(pygame.image.load('hello/fly.png').convert_alpha(), 0, 0.25)
fly_surf = pygame.transform.flip(fly_surf, True, False)
coin_surf = pygame.transform.rotozoom(pygame.image.load('hello/coin.png').convert_alpha(), 0, 0.1)
player_surface = pygame.image.load('hello/jump.png').convert_alpha()

# Sound
sound = -1
music = True
jump_sound = pygame.mixer.Sound('hello/jump_sound.mp3')
jump_sound.set_volume(0.3)
coin_sound = pygame.mixer.Sound('hello/coin.mp3')
coin_sound.set_volume(0.5)
theme_sound = pygame.mixer.Sound('hello/theme.mp3')
theme_sound.set_volume(0.5)
theme_sound.play(loops=sound)

# Intro Screen
intro = pygame.transform.rotozoom(player_surface, 0, 4)
intro_rect = intro.get_rect(center=(400, 200))
game_message = test_font.render('Press SPACE to start', False, 'White')
game_message_rect = game_message.get_rect(center=(400, 320))

# Game Variables
player_rect = player_surface.get_rect(midbottom=(150, 320))
player_gravity = 0
game_active = False
start_time = 0
score = 0
coins = 0
obstacle_list = []
coin_list = []

# Leaderboard Variables
leaderboard_file = "leaderboard.json"
leaderboard = []

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, 2000)


def get_font(size):
    """Returns a font of the desired size."""
    return pygame.font.Font("hello/Daily Bubble.ttf", size)


def display_score():
    """Displays the current score."""
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def display_coins():
    """Displays the current coin count."""
    coin_surf_display = test_font.render(f'Coins: {coins}', False, (255, 215, 0))
    coin_rect = coin_surf_display.get_rect(center=(700, 50))
    screen.blit(coin_surf_display, coin_rect)


def obstacle_movement(obstacles):
    """Moves and displays obstacles."""
    if obstacles:
        for obstacle_rect in obstacles:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 320:
                screen.blit(man_surface, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        obstacles = [obs for obs in obstacles if obs.x > -100]
    return obstacles


def coins_movement(coins):
    """Moves and displays coins."""
    if coins:
        for coin_rect in coins:
            coin_rect.x -= 5
            screen.blit(coin_surf, coin_rect)
        coins = [coin for coin in coins if coin.x > -100]
    return coins


def collision(player, obstacles):
    """Checks for collisions with obstacles."""
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def coin_collision(player, coin_list):
    global coins
    for coin_rect in coin_list[:]:
        if player.colliderect(coin_rect):
            coins += 1
            coin_list.remove(coin_rect)
            coin_sound.play()


def load_leaderboard():
    """Loads the leaderboard from a file."""
    global leaderboard
    try:
        with open(leaderboard_file, "r") as file:
            content = file.read().strip()
            if content:  # Check if the file is not empty
                leaderboard = json.loads(content)
            else:
                leaderboard = []  # If file is empty, initialize as empty list
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = []  # If file doesn't exist or is invalid, initialize as empty list



def save_leaderboard():
    """Saves the leaderboard to a file."""
    with open(leaderboard_file, "w") as file:
        json.dump(leaderboard, file)


def update_leaderboard(player_name, score):
    """Updates the leaderboard with the player's score."""
    global leaderboard
    leaderboard.append({"name": player_name, "score": score})
    
    # Sort the leaderboard by score in descending order
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    
    # Keep only the top 5 highest scores
    if(len(leaderboard) > 5):
       leaderboard = leaderboard[:5]
    
    # Save the updated leaderboard to the file
    save_leaderboard()


def get_player_name():
    """Displays the input screen for the player's name."""
    textinput = pygame_textinput.TextInputVisualizer(font_object=get_font(50))
    textinput.cursor_color = "White"
    player_name = ""
    input_active = True

    while input_active:
        screen.fill("Pink")
        title_surface = get_font(60).render("Enter Your Name:", True, "White")
        title_rect = title_surface.get_rect(center=(400, 150))
        screen.blit(title_surface, title_rect)

        # Display the text input box
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Handle keypresses to stop input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key confirms input
                    player_name = textinput.value.strip()
                    if player_name:  # Ensure the name isn't empty
                        input_active = False  # Exit the loop
                elif event.key == pygame.K_BACKSPACE:  # Backspace to delete
                    textinput.value = textinput.value[:-1]

        # Update the text input field
        textinput.update(events)
        screen.blit(textinput.surface, (300, 250))  # Position of the input field
        pygame.display.update()

    return player_name



def display_leaderboard():
    """Displays the leaderboard."""
    while True:
        screen.fill("Black")
        title_surface = get_font(50).render("Leaderboard", True, "White")
        title_rect = title_surface.get_rect(center=(400, 50))
        screen.blit(title_surface, title_rect)

        for i, entry in enumerate(leaderboard):
            text_surface = get_font(40).render(f"{i + 1}. {entry['name']} - {entry['score']}", True, "White")
            text_rect = text_surface.get_rect(topleft=(200, 100 + i * 50))
            screen.blit(text_surface, text_rect)

        back_button = Button(image=None, pos=(400, 350), text_input="BACK",
                             font=get_font(50), base_color="White", hovering_color="Green")
        back_button.update(screen)
        back_button.changeColor(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.checkForInput(pygame.mouse.get_pos()):
                return

        pygame.display.update()

def play():
    """Main gameplay loop."""
    global game_active, start_time, player_gravity, obstacle_list, coin_list, score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_rect.bottom >= 320:
                    player_gravity = -20
                    jump_sound.play()
                if event.type == obstacle_timer:
                    if randint(0, 1):
                        obstacle_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 220)))
                    else:
                        obstacle_list.append(man_surface.get_rect(bottomright=(randint(900, 1100), 320)))
                if event.type == coin_timer:
                    coin_list.append(coin_surf.get_rect(bottomright=(randint(900, 1100), randint(250, 320))))

            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 320))
            score = display_score()
            display_coins()

            # Player movement
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 320:
                player_rect.bottom = 320
            screen.blit(player_surface, player_rect)

            # Obstacle and coin movement
            obstacle_list = obstacle_movement(obstacle_list)
            coin_list = coins_movement(coin_list)

            # Collision detection
            game_active = collision(player_rect, obstacle_list)
            coin_collision(player_rect, coin_list)
        else:
            screen.fill('Black')
            screen.blit(intro, intro_rect)
            player_rect.midbottom = (150, 320)
            player_gravity = 0
            obstacle_list.clear()
            coin_list.clear()
            score_message = test_font.render(f'Your Score: {score}', False, 'White')
            score_message_rect = score_message.get_rect(center=(400, 320))
            options_mouse_pos = pygame.mouse.get_pos()
            if score == 0:
                screen.blit(game_message, game_message_rect)
            else:
                
                screen.blit(score_message,score_message_rect)
                back_button = Button(image=None, pos=(400, 350), text_input="BACK",
                font=get_font(50), base_color="Black", hovering_color="Green")
                back_button.changeColor(options_mouse_pos)
                back_button.update(screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if back_button.checkForInput(options_mouse_pos):
                            update_leaderboard(player_name, score)
                            score = 0
                            return


        pygame.display.update()
        clock.tick(60)


def options():
    """Displays the options menu."""
    while True:
        options_mouse_pos = pygame.mouse.get_pos()
        screen.fill("white")
        options_text = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        options_rect = options_text.get_rect(center=(400, 200))
        screen.blit(options_text, options_rect)

        back_button = Button(image=None, pos=(400, 350), text_input="BACK",
                             font=get_font(50), base_color="Black", hovering_color="Green")
        back_button.changeColor(options_mouse_pos)
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(options_mouse_pos):
                    return

        pygame.display.update()

def main_menu():
    """Displays the main menu."""
    while True:
        screen.blit(BG, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(400, 50))
        screen.blit(menu_text, menu_rect)

        play_button = Button(image=None, pos=(400, 150), text_input="PLAY",
                             font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        leaderboard_button = Button(image=None, pos=(400, 250), text_input="LEADERBOARD",
                                     font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=None, pos=(400, 350), text_input="QUIT",
                             font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [play_button, leaderboard_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)
        global score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):

                    play()
                if leaderboard_button.checkForInput(menu_mouse_pos):
                    display_leaderboard()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()


# Main Game Execution
if __name__ == "__main__":
    load_leaderboard()
    player_name = get_player_name()
    main_menu()
