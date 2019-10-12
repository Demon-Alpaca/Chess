import gym
import gym_gomoku
env = gym.make('Gomoku19x19-v0') # default 'beginner' level opponent policy

env.reset()
env.render()
env.step(15) # place a single stone, black color first

# play a game
env.reset()
for _ in range(20):
    action = env.action_space.sample() # sample without replacement
    observation, reward, done, info = env.step(action)
    env.render()
    if done:
        print ("Game is Over")
        break