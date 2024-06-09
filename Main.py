import pygame
import csv
from World import world
from Button import Button

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
start_game = False
move_left, move_right = False, False
shoot = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Niggas in Forest: 2nd Semester Edition')

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75
SCROLL_THRESH = 200
screen_scroll = 0
bg_scroll = 0
ROWS = 40
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPE = 18
MAX_LEVELS = 4
level = 1


start_img = pygame.image.load('Asset/Menu/Start.png')
exit_img = pygame.image.load('Asset/Menu/Exit.png')
restart_img = pygame.image.load('Asset/Menu/Restart.png')

BG = (255, 153, 255)
GREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
FOREST = (20,60,10)

pine1_img = pygame.image.load('Asset/Background/pine1.png')
pine2_img = pygame.image.load('Asset/Background/pine2.png')
mount_img = pygame.image.load('Asset/Background/mountain.png')
sky_img = pygame.image.load('Asset/Background/sky_cloud.png')

font = pygame.font.SysFont('Minecraft', 24)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_bg():
    screen.fill(GREY)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x*width) - bg_scroll * 0.5, 0))
        screen.blit(mount_img, ((x*width) - bg_scroll * 0.6, SCREEN_HEIGHT - mount_img.get_height()-300))
        screen.blit(pine1_img, ((x*width) - bg_scroll*0.7, SCREEN_HEIGHT - pine1_img.get_height()-140))
        screen.blit(pine2_img, ((x*width) - bg_scroll*0.8, SCREEN_HEIGHT - pine2_img.get_height()))
    
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    item_box_group.empty()
    decs_group.empty()
    spike_group.empty()
    exit_group.empty()

    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


img_list = []
for x in range(TILE_TYPE):
    img = pygame.image.load(f'Asset/Tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

health_box_img = pygame.image.load('Asset/Icons/Heartbox.png').convert_alpha()
rock_box_img = pygame.image.load('Asset/Icons/Rockbox.png').convert_alpha()

item_boxes = {
    'Health'    : health_box_img,
    'Rock'      : rock_box_img
}

start_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 5)
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 5)
restart_button = Button(SCREEN_WIDTH // 2 - 110 , SCREEN_HEIGHT // 2 , restart_img, 3)

rock_img = pygame.image.load('Asset/Icons/Rock.png').convert_alpha()
heart_img = pygame.image.load('Asset/Icons/Heart.png').convert_alpha()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decs_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()

world_data = []
for row in range(ROWS):
    r = [-1]*COLS
    world_data.append(r)
    
with open(f'Levels/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

Environment = world()
player, health_bar = Environment.process_data(world_data, img_list, TILE_SIZE, enemy_group, item_box_group, item_boxes, decs_group, exit_group, spike_group)          


run = True
while run:
    
    clock.tick(FPS)
    
    if start_game == False:
        screen.fill(FOREST)
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:
        draw_bg()
            
        Environment.draw(screen, screen_scroll)
            
        health_bar.draw(player.health, screen)
            
        draw_text(f'AMMO: {player.ammo}', font, BLACK, SCREEN_WIDTH-120, 10)
        
        player.update()
        player.draw(screen)
            
        for enemy in enemy_group:
            enemy.ai(player, TILE_SIZE, GRAVITY, bullet_group, rock_img, Environment.obstacle_list, SCREEN_WIDTH, SCREEN_HEIGHT, SCROLL_THRESH, screen_scroll, Environment.level_len, spike_group, bg_scroll, exit_group)
            enemy.update()
            enemy.draw(screen)
            
        bullet_group.update(SCREEN_WIDTH, player, bullet_group, enemy_group, Environment.obstacle_list,screen_scroll)
        item_box_group.update(player, screen_scroll)
        exit_group.update(screen_scroll)
        decs_group.update(screen_scroll)
        spike_group.update(screen_scroll)
        bullet_group.draw(screen)
        item_box_group.draw(screen)
        exit_group.draw(screen)
        decs_group.draw(screen)
        spike_group.draw(screen)
            
        if player.alive:
            if shoot:
                player.shoot(bullet_group, rock_img)
            if player.in_air:
                player.update_action(1)
            elif move_left or move_right:
                player.update_action(2)
            else:
                player.update_action(0)
            screen_scroll, level_complete = player.move(move_left, move_right, GRAVITY, Environment.obstacle_list, SCREEN_WIDTH, SCREEN_HEIGHT, SCROLL_THRESH, screen_scroll, bg_scroll, Environment.level_len, TILE_SIZE, spike_group, exit_group)
            bg_scroll -= screen_scroll
            if level_complete:
                level+=1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    with open(f'Levels/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

                Environment = world()
                player, health_bar = Environment.process_data(world_data, img_list, TILE_SIZE, enemy_group, item_box_group, item_boxes, decs_group, exit_group, spike_group) 
            
        else:
            screen_scroll = 0
            if restart_button.draw(screen):
                bg_scroll = 0
                world_data = reset_level() 
                with open(f'Levels/level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter = ',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)

                Environment = world()
                player, health_bar = Environment.process_data(world_data, img_list, TILE_SIZE, enemy_group, item_box_group, item_boxes, decs_group, exit_group, spike_group)          
                    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_SPACE and player.alive:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
                    
                        
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()

pygame.quit()
