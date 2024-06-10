import pygame
import os
import random


class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.flip = False
        self.in_air = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # ai
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 30)
        self.idling = False
        self.idling_count = 0

        animation_types = ['Idle', 'Jump', 'Walk', 'Die']
        for animation in animation_types:
            temp_list = []
            num_of_file = len(os.listdir(
                f'Asset/{self.char_type}/{animation}'))
            for i in range(num_of_file):
                img = pygame.image.load(
                    f'Asset/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, move_left, move_right, gravity, obstacle_list, S_W, S_H, Scroll_Thres, Scren_Scroll, bg_scroll, level_len, tilesize, spike_group, exit_group):
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
            self.vel_y = -8
            self.jump = False
            self.in_air = True

        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        #Collision
        for tile in obstacle_list:
            #x-axis
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'Enemy':
                    self.direction *= -1
                    self.move_counter = 0
            #y-axis
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        
        if pygame.sprite.spritecollide(self, spike_group, False):
            self.health = 0
        
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
        
        if self.rect.bottom  > S_H:
            self.health = 0
        
        if self.char_type == 'Player':
            if self.rect.left + dx < 0 or self.rect.right + dx > S_W:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.char_type == 'Player':
            if (self.rect.right > S_W - Scroll_Thres and bg_scroll < (level_len * tilesize) - S_W)\
				or (self.rect.left < Scroll_Thres and bg_scroll > abs(dx)):
                self.rect.x -= dx
                Scren_Scroll = -dx

            return Scren_Scroll, level_complete

    def shoot(self, bullet_group, rock_img, throw_fx):
        from Bullet import Rock
        from pygame import mixer
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 40
            bullet = Rock(self.rect.centerx + (0.3 *
                          self.rect.size[0] * self.direction), self.rect.centery, self.direction, rock_img)
            bullet_group.add(bullet)
            self.ammo -= 1
            throw_fx.play()
            
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def ai(self, player, tilesize, gravity, bullet_group, bullet_img, obstacle_list, S_W, S_H, Scroll_Thres, Scren_Scroll, level_len, spike_group, bg_scroll, exit_group, shoot_fx):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50

            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot(bullet_group, bullet_img, shoot_fx)
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_move_right = True
                    else:
                        ai_move_right = False
                    ai_move_left = not ai_move_right
                    self.move(ai_move_left, ai_move_right, gravity,
                              obstacle_list, S_W, S_H, Scroll_Thres, Scren_Scroll,bg_scroll, level_len, tilesize, spike_group, exit_group)
                    self.update_action(2)
                    self.move_counter += 1

                    self.vision.center = (
                        self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > tilesize:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        self.rect.x += Scren_Scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)
