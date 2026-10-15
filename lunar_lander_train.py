import os

# suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import gymnasium as gym
from stable_baselines3 import DQN

# --- 1. CONFIGURATION ---
# render_mode=None: we won't draw the environment during training (it's much faster)
env = gym.make("LunarLander-v3", render_mode=None)

# --- 2. CREATE THE AGENT ---
# DQN (Deep Q-Network): this is the neural network that learns the "value function".
model = DQN("MlpPolicy", env, verbose=1)

# --- 3. TRAINING (CONTINUATION) ---
print("--- TRAINING ---")

# If the file exists, we load it; otherwise, we start a new one
if os.path.exists("lunar_lander_model.zip"):
    print("Load existing model...")
    model = DQN.load("lunar_lander_model", env=env)
else:
    model = DQN("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=5000) # increase this to higher value

print("--- SAVE... ---")
model.save("lunar_lander_model")

env.close()
