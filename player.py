import pygame
from config import width, height, screen, player_health, amount_required_for_new_level, \
    initial_proj_speed, max_proj_speed, linear_increment_proj_speed, tb_border_width, heart_slowdown, amount_proj_trail
from asteroid import Asteroid
import os
import math


class Player:
    def __init__(self):
        self.lives = player_health
        self.current_speed_of_asteroids = 1
        self.ast_to_follow = None
        self.should_follow_ast = False
        self.proj_pos = pygame.Vector2(width/2, height)
        self.proj_radius = 8
        self.proj_current_vel = pygame.Vector2(0, 0)
        self.proj_start_speed = 0.1
        self.proj_current_acc = 0.0
        self.proj_current_acc_acc = 0.01
        self.proj_max_speed = 11

        self.proj_color = (173, 216, 230)

        self.level = 1
        self.proj_beaten_on_current_level = 0

        self.asteroid_currrent_speed = initial_proj_speed

        self.heart_radius = 40

        self.hearts = [None]*12
        self.counter = 0

        for i in range(12):
            self.hearts[i] = pygame.image.load(
                os.path.join(f'heart_frames\dummy-removebg-preview_{i+1}.png'))
            self.hearts[i] = pygame.transform.scale(self.hearts[i], (self.hearts[i].get_width(
            )*2*self.heart_radius/self.hearts[i].get_height(), 2*self.heart_radius))

        self.projectile_image = pygame.image.load(
            os.path.join('projectile player.png'))
        self.projectile_image = pygame.transform.scale(
            self.projectile_image, (2*self.proj_radius, 2*self.proj_radius))

        self.proj_trails = [pygame.Vector2(width*2, height)]*amount_proj_trail

        self.score = 0

        self.wrong_stuffs = []

    def draw(self):
        pygame.draw.circle(screen, self.proj_color,
                           self.proj_pos, self.proj_radius)

        for i in range(amount_proj_trail-1):
            self.proj_trails[i] = self.proj_trails[i+1].copy()
            # for j in self.proj_trails:
            #    print(j)
            pygame.draw.circle(
                screen, self.proj_color, self.proj_trails[i], self.proj_radius*(0.9)**(amount_proj_trail-i))
        self.proj_trails[-1] = self.proj_pos.copy()
        # screen.blit(self.projectile_image, (self.proj_pos.x -
        #            self.proj_radius, self.proj_pos.y-self.proj_radius))
        # edit [i] toi correct image

    def shoot_asteroid(self, ast):
        self.proj_pos = pygame.Vector2(width/2, height-175)
        temp = ast.pos-self.proj_pos
        temp.scale_to_length(self.proj_start_speed)
        self.proj_current_vel = temp

        self.ast_to_follow = ast
        self.should_follow_ast = True
        self.proj_trails = [pygame.Vector2(width*2, height)]*amount_proj_trail

    def move_proj(self):
        self.proj_current_acc += self.proj_current_acc_acc
        temp = self.ast_to_follow.pos-self.proj_pos
        temp.scale_to_length(self.proj_current_acc)
        self.proj_current_vel += temp
        self.proj_pos += self.proj_current_vel
        self.proj_current_vel.scale_to_length(
            min(self.proj_current_vel.magnitude(), self.proj_max_speed))

    def has_collided_with_asteroid(self):
        if (self.proj_pos.x-self.ast_to_follow.pos.x)**2+(self.proj_pos.y-self.ast_to_follow.pos.y)**2 <= (self.proj_radius+self.ast_to_follow.radius)**2:
            self.ast_to_follow = None
            self.should_follow_ast = False
            self.proj_pos = pygame.Vector2(width/2, height)
            self.proj_current_vel = pygame.Vector2(0, 0)

            self.proj_beaten_on_current_level += 1
            self.score += math.sqrt(self.proj_beaten_on_current_level +
                                    self.level)
            return True

    def is_new_level(self) -> bool:
        if self.proj_beaten_on_current_level >= amount_required_for_new_level:
            # print('FJHSDGBUYSDFJHKGUDFSHJKGDSJKGKDJSFGJKNSDFG')
            self.proj_beaten_on_current_level = 0
            self.level += 1
            self.asteroid_currrent_speed = min(
                max_proj_speed, self.asteroid_currrent_speed+linear_increment_proj_speed)
            self.proj_current_acc_acc = min(
                0.05, self.proj_current_acc_acc+0.01)
            self.proj_current_acc = min(1, self.proj_current_acc+0.2)
            self.proj_max_speed = min(11+1*6, self.proj_max_speed+1)
            return True
        return False

    def update(self):
        if self.should_follow_ast:
            self.move_proj()
            self.draw()
        self.counter += 1

    def hearts_draw(self):
        for i in range(self.lives):
            # pygame.draw.circle(screen,(255,0,0),
            #    (width-self.heart_radius-self.heart_radius*2.2*i,self.heart_radius+tb_border_width),self.heart_radius)
            screen.blit(self.hearts[(2*i+self.counter//heart_slowdown) % 12],
                        (width-1*self.heart_radius-2*i*self.heart_radius-self.hearts[(2*i+self.counter//heart_slowdown) % 12].get_width()/2, 0))
            # edit [i] toi correct image
