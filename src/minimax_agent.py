"""
Minimax AI Agent with Alpha-Beta Pruning — Optimized Tactical v4

Key improvements:
  - Proper freeze double-turn: freezeball gives us 1 guaranteed bonus throw
  - Smart dodge prediction: move away BEFORE opponent throws (not after)
  - Aim optimization: prefer columns with lower hit chance for opponent
  - Attack timing: lead with throw when opponent just moved (they can't dodge again)
  - Medkit threshold: heal when it's efficient AND we have breathing room
"""

import random
from typing import Tuple, Optional
from game_state import GameState, ActionType


class MinimaxAgent:
    def __init__(self, player_id: int, depth: int = 3):
        self.player_id = player_id
        self.opponent_id = 2 if player_id == 1 else 1
        self.depth = depth
        self.nodes_explored = 0

    # ──────────────────────────────────────────────────────────────
    # Evaluation function
    # ──────────────────────────────────────────────────────────────