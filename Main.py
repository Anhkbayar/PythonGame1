from Tiles import *
from SpriteSheet import Spritesheet

pygame.init()
DISPLAY_W = 800
DISPLAY_H = int(DISPLAY_W*0.6)
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
pygame.display.set_caption('Niggas in Jungle: 2nd Semester Edition')

x = 200
y = 200
scale = 3
img = pygame.image.load('Asset/Walking_Test.png')
img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
rect = img.get_rect()
rect.center = (x,y)

clock = pygame.time.Clock()

running = True
while running:
    
    window.blit(img, rect)
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass
        
        
    pygame.display.update()