import pygame
class screenfade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_count = 0 
    
    def fade(self, screen, S_W, S_H):
        complete = False
        self.fade_count += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.color, (0 - self.fade_count, 0, S_W // 2, S_H))
            pygame.draw.rect(screen, self.color, (S_W // 2 + self.fade_count, 0, S_W, S_H))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_count, S_W, S_H // 2))
            pygame.draw.rect(screen, self.color, (0, S_H // 2 +self.fade_count, S_W, S_H))
        if self.direction == 2:
            pygame.draw.rect(screen, self.color, (0, 0, S_W, 0 + self.fade_count))
        if self.fade_count >= S_W:
            complete = True

        return complete
            
        return complete