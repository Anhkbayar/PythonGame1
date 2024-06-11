import pygame
class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed
		self.fade_counter = 0


	def fade(self, screen, S_W, S_H):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1:
			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, S_W // 2, S_H))
			pygame.draw.rect(screen, self.colour, (S_W // 2 + self.fade_counter, 0, S_W, S_H))
			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, S_W, S_H // 2))
			pygame.draw.rect(screen, self.colour, (0, S_H // 2 +self.fade_counter, S_W, S_H))
		if self.direction == 2:
			pygame.draw.rect(screen, self.colour, (0, 0, S_W, 0 + self.fade_counter))
		if self.fade_counter >= S_W:
			fade_complete = True

		return fade_complete