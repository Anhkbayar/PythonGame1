import pygame
from Player import Character
from Bullet import Rock
from ItemBox import itembox

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
move_left, move_right = False, False
shoot = False


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Niggas in Jungle: 2nd Semester Edition')

clock = pygame.time.Clock()
FPS = 60 

GRAVITY = 0.75
TILE_SIZE = 16

BG = (255, 153, 255)
BLACK = (50, 50, 50)


def scale(scale, pic_path):
    img = pygame.image.load(pic_path).convert_alpha()
    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    return img

font = pygame.font.SysFont('Minecraft', 24)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_BG():
    screen.fill(BG)
    pygame.draw.line(screen, BLACK, (0, 500), (SCREEN_WIDTH, 500))

player = Character('Player', 200, 0, 4, 2, 10)

rock_img = pygame.image.load('Asset/Icons/Rock.png').convert_alpha()
heart_img = pygame.image.load('Asset/Icons/Heart.png').convert_alpha()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

health_box_img = pygame.image.load('Asset/Icons/Heartbox.png').convert_alpha()
rock_box_img = pygame.image.load('Asset/Icons/Rockbox.png').convert_alpha()

item_boxes = {
    'Health'    : health_box_img,
    'Rock'      : rock_box_img
}

item_box = itembox('Health', 100, 500-16, item_boxes, TILE_SIZE)
item_box_group.add(item_box)
item_box =  itembox('Rock', 400, 500-16, item_boxes, TILE_SIZE)
item_box_group.add(item_box)

enemy1 = Character('Player', 400, 450, 4, 2, 30)
enemy2 = Character('Player', 300, 400, 4, 2, 30)
enemy_group.add(enemy1)
enemy_group.add(enemy2)


run = True
while run:
    
    clock.tick(FPS)
    
    draw_BG()
    
    draw_text(f'AMMO: {player.ammo}', font, BLACK, 600, 10)
    draw_text(f'HP: {player.health}', font, BLACK, 600, 30)
    for x in range(player.health):
        screen.blit(heart_img, (90 + (x*10), 40))
    player.update()
    player.draw(screen)
    
    for enemy in enemy_group:
        enemy.update()
        enemy.draw(screen)
    
    bullet_group.update(SCREEN_WIDTH, player, enemy, bullet_group, enemy_group)
    item_box_group.update(player)
    bullet_group.draw(screen)
    item_box_group.draw(screen)
    
    if player.alive:
        if shoot:
            player.shoot(bullet_group, rock_img)
        if player.in_air:
            player.update_action(1)
        elif move_left or move_right:
            player.update_action(2)
        else:
            player.update_action(0)
        player.move(move_left, move_right, GRAVITY)

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
