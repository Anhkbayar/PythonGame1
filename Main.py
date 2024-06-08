import pygame
from Player import Character

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
move_left, move_right = False, False


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Niggas in Jungle: 2nd Semester Edition')

clock = pygame.time.Clock()
FPS = 60 

GRAVITY = 0.75

BG = (255, 153, 255)
def draw_BG():
    screen.fill(BG)
player = Character('Player', 200, 0, 10, 5)

run = True
while run:
    
    clock.tick(FPS)
    
    draw_BG()
    player.update_animation()
    player.draw(screen)
    if player.alive:
        if move_left or move_right:
            player.update_action(1)
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
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
            
                
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False

    pygame.display.update()

pygame.quit()
