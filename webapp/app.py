# pip install streamlit gymnasium
# streamlit run app.py

import streamlit as st
import gymnasium as gym
from stable_baselines3 import DQN
import imageio
import time
import os
import base64

# --- CONFIGURATION ---
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
st.set_page_config(page_title="Lunar Lander AI", page_icon="🚀", layout="wide")

# --- CSS FOR STABILITY ---
# Enforce scrollbar visibility to prevent layout thrashing/jittering
st.markdown("""
    <style>
        .stApp {
            overflow-y: scroll;
        }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "simulation_active" not in st.session_state:
    st.session_state.simulation_active = False


def start_simulation():
    st.session_state.simulation_active = True


# --- HTML DOWNLOAD BUTTON ---
def get_binary_file_downloader_html(bin_file, file_label='File'):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'''
        <a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}" style="text-decoration: none;">
            <div style="
                background-color: #4CAF50; color: white; padding: 15px 20px; text-align: center;
                border-radius: 8px; font-family: sans-serif; font-weight: bold;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s; margin-top: 10px;
                display: flex; align-items: center; justify-content: center; gap: 10px;
            ">
                📥 DOWNLOAD {file_label}
            </div>
        </a>
        '''
        return href
    except FileNotFoundError:
        return None


# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    path = "lunar_lander_model.zip"
    if os.path.exists(path):
        return DQN.load("lunar_lander_model")
    return None


# --- UI LAYOUT ---
st.title("🌕 Lunar Lander AI")
st.markdown("Demonstration of the **Deep Q-Network (DQN)** algorithm.")

col_game, col_download = st.columns([2, 1])

# ==========================================
# 1. RIGHT SIDE (FIXED)
# ==========================================
with col_download:
    container = st.container(border=True)
    with container:
        st.info("🎮 **Try it yourself!**")
        st.write("The AI has learned it... but can you do it? Download the game to your computer!")

        zip_filename = "lunar_lander_challenge.zip"
        download_btn_html = get_binary_file_downloader_html(zip_filename, "GAME PACKAGE")
        if download_btn_html:
            st.markdown(download_btn_html, unsafe_allow_html=True)
            st.caption("Windows .zip | Includes: Python code + Auto launcher")
        else:
            st.warning("⚠️ The game package (zip) is currently unavailable.")

# ==========================================
# 2. LEFT SIDE (SIMULATION)
# ==========================================
with col_game:
    model = load_model()

    if model is None:
        st.error("⚠️ The 'lunar_lander_model.zip' file is missing!")
    else:
        st.subheader("🤖 AI Replay")

        # Placeholders
        controls_placeholder = st.empty()
        status_placeholder = st.empty()
        video_placeholder = st.empty()
        result_placeholder = st.empty()

        if not st.session_state.simulation_active:
            # INITIAL STATE
            controls_placeholder.button("▶️ Start Simulation", type="primary", on_click=start_simulation,
                                        use_container_width=True)

        else:
            # RUNNING
            status_placeholder.info("🔄 Calculating simulation in the background... Please wait.")

            env = gym.make("LunarLander-v3", render_mode="rgb_array")
            obs, info = env.reset()
            done = False
            truncated = False
            total_reward = 0
            frames = []

            while not done and not truncated:
                action, _states = model.predict(obs, deterministic=True)
                obs, reward, done, truncated, info = env.step(action)
                total_reward += reward
                frames.append(env.render())
            env.close()

            # GIF
            gif_path = "replay.gif"
            fps = 30
            imageio.mimsave(gif_path, frames, fps=fps)
            video_duration = len(frames) / fps

            # PLAYBACK
            status_placeholder.info(f"🎬 Replay in progress... ({video_duration:.1f} s)")

            # --- FIX HERE: ---
            # Removed 'use_container_width=True' to maintain fixed size/stability.
            video_placeholder.image(gif_path, caption="AI Landing")

            time.sleep(video_duration)

            # RESULT
            status_placeholder.empty()

            if total_reward >= 200:
                msg = f"✅ **SUCCESS!** Professional work.\n\nScore: **{total_reward:.2f}**"
                result_placeholder.success(msg)
                st.balloons()
            elif total_reward >= 0:
                msg = f"⚠️ **OK.** Safe, but not perfect.\n\nScore: **{total_reward:.2f}**"
                result_placeholder.warning(msg)
            else:
                msg = f"💥 **CRASH!**\n\nScore: **{total_reward:.2f}**"
                result_placeholder.error(msg)

            # RESET
            st.session_state.simulation_active = False

            # Restore button
            controls_placeholder.button("🔄 New Simulation", type="primary", on_click=start_simulation,
                                        use_container_width=True)
