from PPO import PPO, Memory
import torch
import cv2
from game import game
import pygame

def test():
    ############## Hyperparameters ##############
    # creating environment
    rm_ai = game()
    state_dim = rm_ai.state_num
    action_dim = rm_ai.action_num
    render = False
    max_timesteps = 500
    n_latent_var = 64           # number of variables in hidden layer
    lr = 0.0007
    betas = (0.9, 0.999)
    gamma = 0.99                # discount factor
    K_epochs = 4                # update policy for K epochs
    eps_clip = 0.2              # clip parameter for PPO
    #############################################

    n_episodes = 3
    max_timesteps = 300
    render = True


    filename = "PPO_{}.pth".format("robomaster")
    
    memory = Memory()
    ppo = PPO(state_dim, action_dim, n_latent_var, lr, betas, gamma, K_epochs, eps_clip)
    
    ppo.policy_old.load_state_dict(torch.load(filename))
    
    for ep in range(1, n_episodes+1):
        ep_reward = 0
        state = rm_ai.reset()
        for t in range(max_timesteps):
            action = ppo.policy_old.act(state, memory)
            print(action)
            state, reward, done, _ = rm_ai.step(action)
            ep_reward += reward
            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
           
            if done:
                break
            
        print('Episode: {}\tReward: {}'.format(ep, int(ep_reward)))
        ep_reward = 0
    
if __name__ == '__main__':
    test()
    
    
