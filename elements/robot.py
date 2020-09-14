# class robot
import pygame
import numpy as np
from elements.bullet import bullet
from elements.define import *
from elements.ray import ray
vec = pygame.math.Vector2
class robot(pygame.sprite.Sprite):
    def __init__(self, image_path, bullet_path, player, x, y, yaw, bullet_num=500, hp=100):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_group = pygame.sprite.Group()
        self.player = player
        self.yaw = yaw
        self.image_path = image_path
        self.origin = pygame.image.load(self.image_path)
        rect_origin = self.origin.get_rect()
        self.w = rect_origin.w
        self.h = rect_origin.h
        self.image = pygame.transform.rotate(self.origin, yaw)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.bullet_path = bullet_path
        self.bullet_num = bullet_num
        self.hp = hp
        self.shoot_time = 30
        self.reward = 0
        self.state = [0, 0, 0, 0, 0, 0, 0, 0]

    def shoot(self, if_shoot, robot_group, block_group, color=red):
        if self.shoot_time > 0:
            self.shoot_time -= 1
        if (self.bullet_num > 0) and (self.shoot_time == 0) and (if_shoot == 1):
            new_bullet_x = self.pos[0] - self.h/2 * np.math.sin(self.yaw * 3.1415926 / 180)
            new_bullet_y = self.pos[1] - self.h/2 * np.math.cos(self.yaw * 3.1415926 / 180)
            self.bullet_group.add(bullet(self.bullet_path, self.player, new_bullet_x, new_bullet_y, self.yaw,v=10))
            self.bullet_num -= 1
            self.shoot_time = 30

        for b in self.bullet_group:
            b.move()
        hit = pygame.sprite.groupcollide(self.bullet_group, block_group, True, False)
        # reward 
        if len(hit) > 0:
            self.reward -= 0.01

        for robot in robot_group:
            hit = pygame.sprite.spritecollide(robot, self.bullet_group, True, False)
            hit_num = len(hit)
            while hit_num > 0:
                # reward
                self.reward += 2
                robot.be_hit()
                hit_num -= 1


    def move(self, vx, vy, rotate, robot_group, block_group):
        new_pos = self.pos + vec(vx, vy)
        new_yaw = float(int(self.yaw + rotate) % 360)
        self.image = pygame.transform.rotate(self.origin, new_yaw)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = new_pos
        if pygame.sprite.spritecollide(self, block_group, False, False) or \
           pygame.sprite.spritecollide(self, robot_group, False, False):
            self.rect.center = self.pos
            # reward
            self.reward -= 0.5
            return False
        else:
            self.pos = new_pos
            self.yaw = new_yaw
            # reward
            self.reward += 0.001
            return True

    def get_state(self, robot_group, block_group):
        # x, y, yaw, hp, bullet_num, x_e, y_e,
        found, diff, distance = 0, 0, 0
        ray_x = self.pos[0] - self.h/2 * np.math.sin(self.yaw * 3.1415926 / 180)
        ray_y = self.pos[1] - self.h/2 * np.math.cos(self.yaw * 3.1415926 / 180)
        for robot in robot_group:
            angle = get_yaw(ray_x, ray_y, robot.pos[0], robot.pos[1])
            diff_ = get_angle_diff(angle, self.yaw)
            if abs(diff_) <= 30: # 120
                ray_to_robot = ray(ray_x, ray_y, angle)
                hit_type, _, __ = ray_to_robot.move(robot_group, block_group)
                if hit_type == 'robot':
                    found = 1
                    diff = diff_
                    if abs(diff) < 5:
                        self.reward += 0.5
                    else:
                        self.reward += 0.1
                    distance = get_distance(self.pos[0], self.pos[1], robot.pos[0], robot.pos[1])
                    

        ray_yaw = 0
        p_xd = []
        p_yd = []
        while ray_yaw < 360:
            ray_acc = ray(self.pos[0], self.pos[1], ray_yaw)
            hit_type, xd, yd = ray_acc.move(robot_group, block_group)
            d = np.power(xd*xd+yd*yd, 0.5)
            #print('yaw = ' + str(ray_yaw) + ' d = ' + str(d))
            
            p_xd.append(30.0/float(d+11-30) * np.math.sin(ray_yaw * 3.1415926 / 180))
            p_yd.append(30.0/float(d+11-30) * np.math.cos(ray_yaw * 3.1415926 / 180))
            ray_yaw += 10
        # if self.player == 'robot1':
        #     print(str(np.array(p_xd).mean()) + ' ' + str(np.array(p_yd).mean()))

        self.state = [0, 0, 0, 0, 0, 0, 0, 0]
        self.state[0] = (self.pos[0]-10)/810
        self.state[1] = (self.pos[1]-10)/510
        self.state[2] = (np.array(p_xd).mean() + 8) / 16
        self.state[3] = (np.array(p_yd).mean() + 8) / 16
        self.state[4] = self.yaw / 360
        self.state[5] = found
        self.state[6] = (diff + 30) / 60
        self.state[7] = distance / 957
        
        return True

    def step(self, action, robot_group, block_group, bullet_color=red):
        self.reward = 0
        self.move(action[0], action[1], action[2], robot_group, block_group)
        self.shoot(action[3], robot_group, block_group, color=bullet_color)
        self.get_state(robot_group, block_group)
        return True

    def be_hit(self):
        self.hp -= 10
        self.reward -= 1
        # print(self.player + ' be hit ' + 'hp = ' + str(self.hp))
        # reward
        return True
    
    def win(self):
        # reward
        self.reward += 10
        print( 'winner: ' + self.player)
        return True
    
    def loss(self):
        # reward
        self.reward -= 10
        print('losser: ' + self.player)
        return True

    def draw(self):
        # reward
        self.reward -= 0.5
        print('draw: ' + self.player)
        return True

    def reset(self, x, y):
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.yaw = 0
        self.hp = 100
        self.bullet_num = 500
        self.bullet_group.empty()
        return True
        