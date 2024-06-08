import pygame
from Player import Character
from Bullet import Rock

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

BG = (255, 153, 255)
BLACK = (50, 50, 50)
def draw_BG():
    screen.fill(BG)
    pygame.draw.line(screen, BLACK, (0, 500), (SCREEN_WIDTH, 500))
player = Character('Player', 200, 0, 4, 2, 3)
enemy = Character('Player', 400, 450, 4, 2, 30)
rock_img = pygame.image.load('Asset/Icons/Rock.png').convert_alpha()
bullet_group = pygame.sprite.Group()

run = True
while run:
    
    clock.tick(FPS)
    
    draw_BG()
    player.update()
    player.draw(screen)
    enemy.draw(screen)
    
    bullet_group.update(SCREEN_WIDTH)
    bullet_group.draw(screen)
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
