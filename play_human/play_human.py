import gymnasium as gym
import pygame
import numpy as np

# --- BEÁLLÍTÁSOK ---
# Fontos: continuous=True-ra váltunk, hogy egyszerre lehessen gázt adni és kormányozni
env = gym.make("LunarLander-v3", render_mode="human", continuous=True)

# Pygame inicializálása a billentyűzet figyeléséhez
pygame.init()
pygame.display.set_caption("Lunar Lander - Continuous Control")

print("--- EMBERI JÁTÉK (CONTINUOUS MÓD) ---")
print("Irányítás:")
print("  FEL / W:     Főhajtómű")
print("  BAL / A:     Bal fúvóka (Jobbra lök)")
print("  JOBB / D:    Jobb fúvóka (Balra lök)")
print("Tipp: Most már egyszerre is nyomhatod őket!")


def run_game():
    running = True
    while running:
        # Környezet resetelése
        obs, info = env.reset()
        current_score = 0
        terminated = False
        truncated = False

        # Óra az FPS limitáláshoz (hogy ne fusson túl gyorsan)
        clock = pygame.time.Clock()

        while not (terminated or truncated):
            # 1. Pygame események (kilépés figyelése)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    terminated = True  # Kilépünk a belső ciklusból is

            # 2. Billentyűk állapotának lekérdezése
            keys = pygame.key.get_pressed()

            # 3. Akció összeállítása (Continuous módban)
            # action[0]: Főhajtómű (-1..1), de csak a >0 ér valamit
            # action[1]: Kormányzás (-1..1). -1: Jobb fúvóka (Balra lök), +1: Bal fúvóka

            main_engine = 0.0
            lateral_engine = 0.0

            # Gázadás
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                main_engine = 1.0
            else:
                main_engine = -1.0  # Kikapcsolt állapot

            # Kormányzás (prioritás nélkül, összeadódik ha mindkettőt nyomod -> 0)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                lateral_engine += 1.0  # Bal fúvóka (Jobbra tol)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                lateral_engine -= 1.0  # Jobb fúvóka (Balra tol)

            # Az akció egy tömb: [főhajtómű, kormányzás]
            action = np.array([main_engine, lateral_engine])

            # 4. Lépés a környezetben
            obs, rew, terminated, truncated, info = env.step(action)
            current_score += rew

            # FPS limit (30 FPS, mint az eredetiben)
            clock.tick(30)

        # Ha vége a körnek (de nem léptünk ki teljesen)
        if running:
            print(f"--- JÁTÉK VÉGE ---")
            print(f"Végső pontszám: {current_score:.2f}")
            if current_score >= 200:
                print("Eredmény: PROFESSZIONÁLIS LESZÁLLÁS! 🏆")
            elif current_score >= 0:
                print("Eredmény: Biztonságos, de pontatlan.")
            else:
                print("Eredmény: Zuhanás / Összetörés. 💥")
            print("------------------------------------------")

    env.close()
    pygame.quit()


# Indítás
if __name__ == "__main__":
    run_game()
