import gymnasium as gym
import pygame
import numpy as np


def main():
    # --- SETTINGS ---
    # continuous=True: Realistic physics (gas + steering simultaneously)
    # render_mode="human": Opens in a window
    env = gym.make("LunarLander-v3", render_mode="human", continuous=True)

    pygame.init()
    pygame.display.set_caption("Lunar Lander Challenge - Can YOU land it?")

    print("--- LUNAR LANDER CHALLENGE ---")
    print("Controls:")
    print("  UP / W:       Main Engine")
    print("  LEFT / A:     Left Engine (Push Right)")
    print("  RIGHT / D:    Right Engine (Push Left)")
    print("  R:            Restart (when finished)") # Note: Code currently auto-restarts

    running = True
    while running:
        obs, info = env.reset()
        current_score = 0
        terminated = False
        truncated = False

        # Game loop for one episode
        while not (terminated or truncated):
            # 1. Watch for exit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    terminated = True

            # 2. Controls (Continuous mode)
            keys = pygame.key.get_pressed()

            # Main engine (0..1)
            # If UP or W is pressed, engine is ON (1.0), otherwise OFF (-1.0)
            main_engine = 1.0 if (keys[pygame.K_UP] or keys[pygame.K_w]) else -1.0

            # Steering (-1..1)
            lateral_engine = 0.0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                lateral_engine += 1.0  # Fires left engine, pushes RIGHT
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                lateral_engine -= 1.0  # Fires right engine, pushes LEFT

            # Construct action vector
            action = np.array([main_engine, lateral_engine])

            # 3. Step in the environment
            obs, rew, terminated, truncated, info = env.step(action)
            current_score += rew

            # If the user closes the window during the game
            if not running:
                break

        # End of episode evaluation
        if running:
            print(f"--- END OF EPISODE ---")
            print(f"Final Score: {current_score:.2f}")
            if current_score >= 200:
                print("RESULT: 🏆 PROFESSIONAL LANDING! 🏆")
            elif current_score >= 0:
                print("RESULT: ✅ Safe, but not perfect.")
            else:
                print("RESULT: 💥 CRASH!")
            print("------------------------------------------")

    env.close()
    pygame.quit()


if __name__ == "__main__":
    main()
