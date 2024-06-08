import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type =char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Asset/{self.char_type}/Idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Asset/{self.char_type}/Walk/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def move(self, move_left, move_right, gravity):
        dx = 0
        dy = 0
        if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump == True:
            self.vel_y = -11
            self.jump = False
        
        self.vel_y += gravity   
        dy +=self.vel_y        
       
        self.rect.x += dx
        self.rect.y += dy
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index+=1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),self.rect)
