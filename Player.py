import pygame, os


class Character(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type =char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.flip = False
        self.in_air = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        animation_types = ['Idle', 'Jump', 'Walk']
        for animation in animation_types:
            temp_list = []
            num_of_file = len(os.listdir(f'Asset/{self.char_type}/{animation}'))
            for i in range(num_of_file):
                img = pygame.image.load(f'Asset/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        self.update_animation()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -=1
            
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
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y
        dy +=self.vel_y    
        
        if self.rect.bottom + dy > 500:
            dy = 500 - self.rect.bottom
            self.in_air = False
   
       
        self.rect.x += dx
        self.rect.y += dy
        
    def shoot(self, bullet_group, rock_img):
        from Bullet import Rock
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 50
            bullet = Rock(self.rect.centerx + (0.15 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, rock_img)
            bullet_group.add(bullet)
            self.ammo -=1
            
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
