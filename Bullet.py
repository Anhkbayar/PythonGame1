import pygame

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center =  (x,y)
        self.direction = direction
    
    def update(self, Width):
        self.rect.x += (self.direction * self.speed) 
        
        if self.rect.right < 0 or self.rect.left > Width:
            self.kill()
        
        