import gym
from gym import wrappers
import numpy as np
import six.moves.cPickle as cPickle
import socket

def main():
    
    #Initialize the Cartpole Game Environment
    env = gym.make('CartPole-v0')
    
    #Create a wrapper to record logs/videos for uploading
    #Cartpole experiment directory, change this counter every run,
    #or delete existing directory of same name
    env = wrappers.Monitor(env, 'cartpole-exp-2')

    #Connect to the Java server to send messages
    client = setup_client()

    #How many times to run the game, min 100 required to submit results
    #Can reduce it for testing/debuging purpose
    #For good evaluation, 300 is recommended
    NUM_EPISODES = 100

    #Number of timesteps, for winning the game, needs to run for 200 timesteps
    NUM_TIMESTEPS = 200

    for i_episode in range(NUM_EPISODES):
        
        #Reset the game to get a new start state
        observation = env.reset()

        #Get initial action based on initial observation
        #Need not be a special case, can be part of the overall algorithm
        action = get_initial_action(client, observation)

        for t in range(NUM_TIMESTEPS):
            
            #Render the current timestep
            env.render()
            print("Current observation {}, Taking action {}".format(observation, action))
            
            #Get new observation based by taking the action
            observation, reward, done, info = env.step(action)

            #Get new action based on new observation and prev action
            #Need not specifically use knowledge of previous action
            action = get_new_action(client, observation, action)

            #If done, means game over
            if done:
                game_over(client, observation)
                print('Episode Terminated after {} timesteps with observation {}'.format(t+1, observation))
                break

def setup_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 6789))
    return client

'''
Get initial action based on initial
observation
0 - go left
1 - go right

Sample implementation - 
    theta = observation[2]
    ang_vel = observation[3] 
    action = 0 if theta < 0 else 1
    return action
'''
def get_initial_action(client, observation):
    return get_action(client, observation, 0, False, True)

'''
Get new action based on new observation and prev action
Need not specifically use knowledge of previous action
0 - go left
1 - go right

Sample implementation - 
    theta = observation[2]
    ang_vel = observation[3]
    
    \'''
    If absolute value of theta and ang vel outside proper range,
    change action
    \'''
    if (np.fabs(theta) > 0.05 or np.fabs(ang_vel) > 0.5):
        action = 1 - action
    return action    

'''
def get_new_action(client, observation, action):
    return get_action(client, observation, action, False, False)

'''
Send game over message to server
'''
def game_over(client, observation):
    return get_action(client, observation, 0, True, False)

'''
Get action from server, provided 
observation,
previous action
Done (i.e. Game over?)
Initial (i.e. Game just started?)
'''
def get_action(client, observation, action, done, initial):
    message = [observation, action, done, initial]
    message = cPickle.dumps(message)
    client.send(message)
    action = int(cPickle.loads(client.recv(8))) #8 bytes, size of int
    return action

#Run if this is the main file
if __name__ == '__main__':
    main()