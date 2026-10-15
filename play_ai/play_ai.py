import os

# suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import gymnasium as gym
from stable_baselines3 import DQN

# render_mode="human": we will see it in a window
env = gym.make("LunarLander-v3", render_mode="human")

print("--- DEMÓ INDÍTÁSA ---")

model = DQN.load("lunar_lander_model")

ep = 0
while True:
    ep += 1
    obs, info = env.reset()
    done = False
    truncated = False
    total_reward = 0
    
    while not done and not truncated:
        # predict the action
        action, _states = model.predict(obs, deterministic=True)

        # execute the action
        obs, reward, done, truncated, info = env.step(action)
        total_reward += reward
        
    print(f"{ep+1}. leszállás pontszáma: {total_reward:.2f}")

env.close()
