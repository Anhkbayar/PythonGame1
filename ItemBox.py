import pygame

class itembox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, item_boxes, TILE_SIZE):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health  = player.max_health
            elif self.item_type == 'Rock':
                player.ammo += 5
            
            self.kill()