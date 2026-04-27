"""
Snowball Fight GUI — Fixed & Enhanced
  • Correct freeze/bonus-turn: attacker acts twice, victim skips turn
  • Proper dodge animation: ghost trail + destination tile highlight
  • Frozen aura with orbiting ice crystals and shake
  • Smart item HUD with icons
"""
import pygame, sys, os, time, math, random
from pathlib import Path
from game_state import GameState, ActionType
from game import SnowballGame
from enum import Enum


class GameScreen(Enum):
    MENU = 1
    GAMEPLAY = 2
    GAME_OVER = 3


def draw_rounded_box(surf, rect, fill, border, radius=10, border_width=2):
    pygame.draw.rect(surf, fill, rect, border_radius=radius)
    pygame.draw.rect(surf, border, rect, border_width, border_radius=radius)


class Button:
    HOVER_TINT = (255, 255, 255, 55)

    def __init__(self, image, x, y, w, h, callback, label=""):
        self.image = pygame.transform.smoothscale(image, (w, h)) if image else None
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.label = label
        self.hovered = False

    # ── Main loop ────────────────────────────────────────────────
    def draw(self):
        if self.current_screen == GameScreen.MENU:
            self.draw_menu()
        elif self.current_screen == GameScreen.GAMEPLAY:
            self.draw_gameplay()
        elif self.current_screen == GameScreen.GAME_OVER:
            self.draw_game_over()
        pygame.display.flip()

    def run(self):
        print("\nControls: 1/2/3 = start | SPACE = pause | UP/DOWN = speed | Q = quit\n")
        while self.running:
            self.handle_events()
            self.update_game()
            self.draw()
            self.clock.tick(60)
        print("Thanks for playing!")
        pygame.quit()


def main():
    gui = CompleteGameGUI()
    gui.run()


if __name__ == "__main__":
    main()