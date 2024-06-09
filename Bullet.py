import pygame

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 12
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center =  (x,y)
        self.direction = direction
    
    def update(self, Width, player, bullet_group, enemy_group, obstacle_group, screen_scroll):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        
        if self.rect.right < 0 or self.rect.left > Width:
            self.kill()
            
        for tile in obstacle_group:
            if tile[1].colliderect(self.rect):
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