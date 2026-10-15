---
title: Lunar Lander AI
emoji: 🚀
colorFrom: indigo
colorTo: gray
sdk: streamlit
sdk_version: 1.52.2
app_file: app.py
pinned: false
license: mit
short_description: A Deep Q-Network (DQN) agent learning to land on the Moon.
---

# 🌕 Lunar Lander AI

Welcome to the **Lunar Lander AI** project! This application demonstrates the power of **Deep Reinforcement Learning (DRL)** by showing how an AI agent controls a lunar lander to perform a safe landing on the moon's surface.

## 🧠 How it Works

The agent was trained using the **Deep Q-Network (DQN)** algorithm. Instead of being programmed with explicit rules (like "if speed is high, brake"), the AI learned by trial and error through thousands of simulations.

* **Goal:** Land the spacecraft between the two yellow flags.
* **Rewards:** The agent gets points for moving toward the pad, touching the ground with legs, and loses points for crashing or using fuel.
* **Observation:** The AI sees the lander's coordinates, velocity, angle, and ground contact sensors.
* **Actions:** It can choose to: Do nothing, Fire Main Engine, Fire Left Engine, or Fire Right Engine.

## 🛠️ Tech Stack

This project was built using the following technologies:

* **Python:** The core programming language.
* **Stable Baselines3:** For the implementation of the DQN algorithm.
* **Gymnasium (formerly OpenAI Gym):** Provides the `LunarLander-v3` simulation environment.
* **Streamlit:** Creates the interactive web interface you are using right now.

## 🎮 Features

* **Live Simulation:** Watch the trained AI generate a new landing attempt in real-time within your browser.
* **Performance Metrics:** See the score of each landing (Success, Crash, or Safe).
* **Downloadable Game:** You can download the trained agent and the game environment as a standalone Windows package to run on your own machine.

## 🚀 Usage

Click the **"Start Simulation"** button to generate a new episode. The app will run the simulation in the background and present a replay GIF of the landing.

---
*Created by [Csaba Faragó](http://faragocsaba.hu) & Gemini*
