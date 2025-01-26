import pygame
from sys import exit
from random import randint
def display_coins():
    coin_surf = test_font.render(f'Coins: {coins}', False, 'Black')  # Golden color
    coin_rect = coin_surf.get_rect(center=(650, 50))
    screen.blit(coin_surf, coin_rect)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 330:
                screen.blit(voldy_surf,obstacle_rect)
            else:
                screen.blit(owl_surf,obstacle_rect)
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > - 100]
        return obstacle_list
    else:
        return []
def collision(player, obstacle):
    if obstacle:
        player_shrunk = player.inflate(-20, -20)
        for obstacle_rect in obstacle:
            obstacle_rect_shrunk = obstacle_rect.inflate(-20, -20)
            if player_shrunk.colliderect(obstacle_rect_shrunk):
                return False
    return True

#coins
def coins_movement(coin_list):
    if coin_list:
        for coin_rect in coin_list:
            coin_rect.x -= 5
            screen.blit(coin_surf,coin_rect)
            
            coin_list = [coin for coin in coin_list if coin.x > - 100]
        return coin_list
    else:
        return []
def coin_collision(player, coin_list):
    global coins  # Access the global coins variable
    if coin_list:
        for coin in coin_list[:]:  # Use a copy of the list to iterate safely
            if player.colliderect(coin):
                coins += 1
                coin_list.remove(coin)  # Remove the collected coin
   
    
def display_score():
    currTime = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score:{currTime}', False , 'Black')
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return currTime
def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 320:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()#start the engine
screen = pygame.display.set_mode((800,400))#game window,widtg,height
pygame.display.set_caption('Runner ')#game name
clock = pygame.time.Clock()
test_font = pygame.font.Font('hello/Daily Bubble.ttf',50)
game_active = False
start_time = 0
score = 0
coins = 0

sky_surface = pygame.image.load('hello/castle.png')#regular surface
ground_surface = pygame.image.load('hello/ground.png').convert()

voldy_surf1 = pygame.transform.rotozoom(pygame.image.load('hello/voldy1.png').convert_alpha(),0,0.20)
voldy_surf1 = pygame.transform.flip(voldy_surf1,True,False)
voldy_surf2= pygame.transform.rotozoom(pygame.image.load('hello/voldy2.png').convert_alpha(),0,0.20)
voldy_surf2 = pygame.transform.flip(voldy_surf2,True,False)
voldy_frames = [voldy_surf1,voldy_surf2]
voldy_index = 0
voldy_surf = voldy_frames[voldy_index]

owl_surf1 = pygame.image.load('hello/fly1.png').convert_alpha()
owl_surf1 = pygame.transform.rotozoom(owl_surf1, 0, 0.20)
owl_surf1 = pygame.transform.flip(owl_surf1,True, False)
owl_surf2 = pygame.image.load('hello/fly2.png').convert_alpha()
owl_surf2 = pygame.transform.rotozoom(owl_surf2, 0, 0.20)
owl_surf2 = pygame.transform.flip(owl_surf2,True, False) 
owl_frames = [owl_surf1,owl_surf2]
owl_index = 0
owl_surf = owl_frames[voldy_index]
obstacle_list = []
coin_list = []

#player
player_index = 0
player_walk1 = pygame.transform.rotozoom(pygame.image.load('hello/walk1.png').convert_alpha(),0,0.20)
player_walk2 = pygame.transform.rotozoom(pygame.image.load('hello/walk2.png').convert_alpha(),0,0.20)
player_walk3 = pygame.transform.rotozoom(pygame.image.load('hello/walk3.png').convert_alpha(),0,0.20)
player_walk = [player_walk1,player_walk2,player_walk3]
player_jump = pygame.transform.rotozoom(pygame.image.load('hello/jump.png').convert_alpha(),0,0.20)
player_rect = player_walk[player_index].get_rect(midbottom = (150,320))

#coins
coin_surf = pygame.image.load('hello/coin.png').convert_alpha()
coin_surf = pygame.transform.rotozoom(coin_surf, 0, 0.1)
#intro
intro = pygame.image.load('hello/villian.png').convert_alpha()
intro = pygame.transform.rotozoom(intro, 0, 0.7)
intro_rect = intro.get_rect(center = (400,150))
game_message = test_font.render(f'Press space to start', False , 'White')
game_message_rect = game_message.get_rect(center = (400,320))


score_surf = test_font.render('score', False, 'Black')
score_rect = score_surf.get_rect(center= (400, 50))

#timer
obstacle_time = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_time, 1500)

coin_time = pygame.USEREVENT + 2
pygame.time.set_timer(coin_time, 2000)

voldy_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(voldy_animation_timer, 500)

owl_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(owl_animation_timer, 200)


player_gravity = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()#ends the engine
            exit()#closes all loops and operations

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 320:
                    player_gravity = -22
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #print(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 320:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -22
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
        if game_active:
            if event.type == obstacle_time:
                if randint(0,1):
                    obstacle_list.append(owl_surf.get_rect(bottomright = (randint(900,1100),180)))
                else:
                    obstacle_list.append(voldy_surf.get_rect(bottomright = (randint(900,1100),330)))
            
                coin_list.append(coin_surf.get_rect(bottomright = (randint(900,1100),randint(250,320))))
            if event.type == voldy_animation_timer:
                if voldy_index == 0: voldy_index = 1
                else: voldy_index = 0
                voldy_surf = voldy_frames[voldy_index]
            if event.type == owl_animation_timer:
                if owl_index == 0: owl_index = 1
                else: owl_index = 0
                owl_surf = owl_frames[owl_index]

        

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,320))
        #pygame.draw.rect(screen, 'Pink', score_rect)
        #pygame.draw.rect(screen, 'Pink', score_rect,10)
        #creen.blit(score_surf, score_rect)
        score = display_score()
        display_coins()

        #player_rect.right -= 1
        #if player_rect.right  < 0 : player_rect.right = 800
        player_gravity += 1
        player_rect.y += player_gravity #FALLING ILLUSIOn
        if player_rect.bottom >= 320 : player_rect.bottom = 320
        player_animation()
        screen.blit(player_surf,player_rect)#using rect

        #obstacle_movement
        obstacle_movement(obstacle_list)
        #coin_movement
        coin_list = coins_movement(coin_list)

        #man_rect.left -= 3
        #if(man_rect.left < 0): man_rect.left = 800
        #screen.blit(man_surface,man_rect)

        #shows mouse pressed
        # = pygame.mouse.get_pos()
        #if player_rect.collidepoint(mouse_pos):
        #    print(pygame.mouse.get_pressed())
        #if touches then game exits
        game_active = collision(player_rect, obstacle_list)
        coin_collision(player_rect, coin_list)
        #start_time = int(pygame.time.get_ticks()/1000)
    else:
        screen.fill('Black')
        screen.blit(intro, intro_rect)
        player_rect.midbottom = (150,320)
        player_gravity = 0
        obstacle_list.clear()
        start_time = int(pygame.time.get_ticks()/1000)
        score_message = test_font.render(f'Your Score: {score}', False , 'White')
        score_message_rect = score_message.get_rect(center = (400,320))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)#sets max frame rates,60 fps
