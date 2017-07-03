import gym
from gym import wrappers
import numpy as np

def main():
    env = gym.make('CartPole-v0')
    env = wrappers.Monitor(env, 'cartpole-exp-1')

    for i_episode in range(300):
        observation = env.reset()
        action = get_initial_action(observation)

        for t in range(200):
            env.render()
            print("{}, {}".format(observation, action))
            
            observation, reward, done, info = env.step(action)
            action = get_action(observation, action)
            if done:
                print('Episode Terminated after {} timesteps with observation {}'.format(t+1, observation))
                break

'''
Get initial action based on initial
observation
'''
def get_initial_action(observation):
    theta = observation[2]
    ang_vel = observation[3] 
    action = 0 if theta < 0 else 1
    #prev_action = action
    #prev_act_time = 0
    return action

'''
Get new action based on new observation and prev action
'''
def get_action(observation, action):
    '''if prev_act_time < 2:
            action = action
        else:
            action = 1 - prev_action
            prev_act_time = 0'''
        #action = action if prev_act_time < 2 else 1 - prev_action
        #action = 1 if prev_action == 0 else 0
        #prev_action = action
        #prev_act_time += 1
    #prev_act_time += 1
    theta = observation[2]
    ang_vel = observation[3]
    
    '''
    If absolute value of theta and ang vel outside proper range,
    change action
    '''
    if (np.fabs(theta) > 0.05 or np.fabs(ang_vel) > 0.5):
        action = 1 - action
        #prev_act_time = 0
    return action    

#Run if this is the main file
if __name__ == '__main__':
    main()