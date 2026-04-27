"""
Main Game Logic
Orchestrates the AI vs AI game with proper freeze/bonus-turn handling.

Turn flow each round:
  1. P1 acts normally
     - If P1 used freezeball → pending_bonus_turn = 1
       * P2's turn is SKIPPED (frozen, tick down)
       * P1 gets BONUS TURN immediately
  2. P2 acts normally (unless skipped due to freeze)
"""

from typing import Dict
from game_state import GameState, ActionType
from minimax_agent import MinimaxAgent
from mcts_agent import MCTSAgent
import time


class SnowballGame:
    def __init__(self, agent1_type: str = "minimax", agent2_type: str = "mcts"):
        self.state = GameState()
        self.agent1_type = agent1_type
        self.agent2_type = agent2_type

        self.agent1 = (MinimaxAgent(player_id=1, depth=3)
                       if agent1_type == "minimax"
                       else MCTSAgent(player_id=1, iterations=400))

        self.agent2 = (MinimaxAgent(player_id=2, depth=3)
                       if agent2_type == "minimax"
                       else MCTSAgent(player_id=2, iterations=400))

        self.game_log = []
        self.turn_history = []

    # ── helpers ──────────────────────────────────────────────────

    def _act(self, player_id: int, turn_num: int, tag: str = "") -> bool:
        """Execute one action for player_id. Returns False if game ended."""
        agent = self.agent1 if player_id == 1 else self.agent2
        start = time.time()
        action = agent.get_best_action(self.state)
        t = time.time() - start
        result = self.state.apply_action(player_id, action)

        label = f"[{tag}]" if tag else ""
        print(f"  P{player_id}{label}: {action.name:20s} -> {result['message']}  ({t:.3f}s)")

        self.state.check_game_over()
        self.turn_history.append({
            'turn':      turn_num,
            'player':    player_id,
            'tag':       tag,
            'action':    action.name,
            'result':    result['message'],
            'p1_hp':     self.state.player1_hp,
            'p2_hp':     self.state.player2_hp,
            'p1_frozen': self.state.player1_frozen,
            'p2_frozen': self.state.player2_frozen,
            'time':      t,
        })
        return not self.state.is_game_over

    def play_turn(self) -> bool:
        """Play one full round (advance_turn + handle all actions incl. bonus turns)."""
        self.state.advance_turn()
        turn_num = self.state.current_turn

        print(f"\n{'='*60}")
        print(f"TURN {turn_num}")
        print(self.state)

        for player_id in [1, 2]:
            if self.state.is_game_over:
                return False

            frozen = self.state.player1_frozen if player_id == 1 else self.state.player2_frozen

            # ── SKIPPED: player is frozen (counter = 2 or 1) ──
            if frozen > 0:
                print(f"  P{player_id} FROZEN (turns left={frozen}) — SKIPPED!")
                self.state.tick_frozen(player_id)
                self.turn_history.append({
                    'turn': turn_num, 'player': player_id, 'tag': 'FROZEN',
                    'action': 'SKIPPED', 'result': f'Frozen ({frozen})',
                    'time': 0, 'p1_hp': self.state.player1_hp,
                    'p2_hp': self.state.player2_hp,
                    'p1_frozen': self.state.player1_frozen,
                    'p2_frozen': self.state.player2_frozen,
                })
                continue

            # ── NORMAL ACTION ──
            if not self._act(player_id, turn_num):
                return False

            # ── BONUS TURN: did this player just use a freezeball? ──
            if self.state.pending_bonus_turn == player_id:
                self.state.consume_bonus_turn(player_id)
                opp = 2 if player_id == 1 else 1
                print(f"  >>> P{player_id} BONUS TURN (P{opp} is frozen, {self.state.player2_frozen if player_id==1 else self.state.player1_frozen} turns left) <<<")
                if self.state.is_game_over:
                    return False
                if not self._act(player_id, turn_num, tag="BONUS"):
                    return False

        return True

    def play_full_game(self) -> Dict:
        print(f"\n{'#'*60}")
        print(f"# {self.agent1_type.upper()} vs {self.agent2_type.upper()}")
        print(f"{'#'*60}\n")

        start = time.time()
        while self.play_turn():
            if self.state.current_step > 500:
                break
        game_time = time.time() - start

        print(f"\nGAME OVER -- Winner: {self.state.winner}")
        print(f"Steps: {self.state.current_step}  Time: {game_time:.2f}s")
        print(f"P1 HP: {self.state.player1_hp}  P2 HP: {self.state.player2_hp}")
        print(f"P1 Items: {self.state.player1_items}  P2 Items: {self.state.player2_items}")

        return {
            'winner':             self.state.winner,
            'turns':              self.state.current_turn,
            'steps':              self.state.current_step,
            'final_p1_hp':        self.state.player1_hp,
            'final_p2_hp':        self.state.player2_hp,
            'p1_items_remaining': self.state.player1_items.copy(),
            'p2_items_remaining': self.state.player2_items.copy(),
            'game_time':          game_time,
            'agent1_type':        self.agent1_type,
            'agent2_type':        self.agent2_type,
            'history':            self.turn_history,
        }

    def get_game_state(self) -> GameState:
        return self.state

    def get_history(self) -> list:
        return self.turn_history


if __name__ == "__main__":
    game = SnowballGame(agent1_type="minimax", agent2_type="mcts")
    results = game.play_full_game()