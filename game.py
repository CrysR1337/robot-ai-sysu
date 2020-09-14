# init game.py
import pygame
from elements.robot import robot
from elements.ground import ground
from elements.define import *
import random
import math
vec = pygame.math.Vector2
class game():
    def __init__(self):
        pygame.init()
        # pygame.display.set_caption("robomaster-ai")
        # self.screen = pygame.display.set_mode((830, 530))
        self.clock = pygame.time.Clock()
        self.running = True
        self.ground = ground('elements/resource/ground.png')
        self.robot1 = robot('elements/resource/robot1.png', 'elements/resource/red_bullet.png', 'robot1', 200, 200, 270)
        self.robot2 = robot('elements/resource/robot2.png', 'elements/resource/blue_bullet.png', 'robot2', 600, 200, 0)

        self.ground_group = pygame.sprite.Group()
        self.robot1_group = pygame.sprite.Group()
        self.robot2_group = pygame.sprite.Group()
        self.ground_group.add(self.ground)
        self.robot1_group.add(self.robot1)
        self.robot2_group.add(self.robot2)
        self.time_tick_global = 0
        self.time_tick_local  = 0
        self.action_num = 54
        self.state_num  = 8


    def run(self):
        key = pygame.key.get_pressed()
        action1 = [0, 0, 0, 0]
        if key[pygame.K_a]: # move left
            action1[0] = -2 
        if key[pygame.K_d]: # move right
            action1[0] = 2
        if key[pygame.K_w]: # move up
            action1[1] = -2
        if key[pygame.K_s]: # move down
            action1[1] = 2
        if key[pygame.K_t]: # rotate counter clockwise
            action1[2] = 3
        if key[pygame.K_y]: # rotate clockwise
            action1[2] = -3
        if key[pygame.K_r]: # shoot
            action1[3] = 1


        action2 = [0, 0, 0, 0]
        if key[pygame.K_LEFT]:  # move left
            action2[0] = -2 
        if key[pygame.K_RIGHT]: # move right
            action2[0] = 2
        if key[pygame.K_UP]:    # move up
            action2[1] = -2
        if key[pygame.K_DOWN]:  # move down
            action2[1] = 2
        if key[pygame.K_j]:     # rotate counter clockwise
            action2[2] = 3
        if key[pygame.K_k]:     # rotate clockwise
            action2[2] = -3
        if key[pygame.K_l]:     # shoot
            action2[3] = 1
        return action1, action2

    def done(self):
        if self.time_tick_local < 5400:
            if self.robot1.hp <= 0 and self.robot2.hp > 0:
                self.robot1.loss()
                self.robot2.win()
                return True
            elif self.robot1.hp > 0 and self.robot2.hp <= 0:
                self.robot1.win()
                self.robot2.loss()
                return True
            elif self.robot1.hp <= 0 and self.robot2.hp <= 0:
                self.robot1.draw()
                self.robot2.draw()
                return True
        elif self.time_tick_local >= 5400:
            if self.robot1.hp > self.robot2.hp:
                self.robot1.win()
                self.robot2.loss()
            elif self.robot1.hp < self.robot2.hp:
                self.robot1.win()
                self.robot2.loss()
            else:
                self.robot1.draw()
                self.robot2.draw()
            return True
        return False

    def step(self, ain, typein='net'):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         exit()
        if typein == 'net':
            action1 = get_action(ain)
            action2 = get_action(random.randint(0,53))
            # _, action2 = self.run()
        elif typein == 'key':
            action1, action2 = self.run()

        # print(str(self.robot1.state) + ' ' + str(action1) + ' ' + str(self.robot1.reward))
        
        self.time_tick_local  += 1
        self.time_tick_global += 1
        self.robot1.step(action1, self.robot2_group, self.ground.block_group, bullet_color=red)
        self.robot2.step(action2, self.robot1_group, self.ground.block_group, bullet_color=blue)
        
        done = False
        info = 0
        # self.ground_group.draw(self.screen)
        # self.ground.block_group.draw(self.screen)
        # self.robot1_group.draw(self.screen)
        # self.robot2_group.draw(self.screen)
        # self.robot1.bullet_group.draw(self.screen)
        # self.robot2.bullet_group.draw(self.screen)
        # pygame.display.update()
        if self.done():
            done = True
            self.reset()
        # print(self.robot2.state[2], self.robot2.state[3])
        return self.robot1.state, self.robot1.reward, done, info

    def reset(self):
        self.time_tick_local = 0
        self.robot1.reset(200, 200)
        self.robot2.reset(600, 200)
        return self.robot1.state

if __name__ == '__main__':
    rm_ai_test = game()
    while True:
        rm_ai_test.step(0, typein='key')
        rm_ai_test.clock.tick(30)