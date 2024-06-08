import pygame

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center =  (x,y)
        self.direction = direction
    
    def update(self, Width, player, enemy, bullet_group, enemy_group):
        self.rect.x += (self.direction * self.speed) 
        
        if self.rect.right < 0 or self.rect.left > Width:
            self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 4
                self.kill()