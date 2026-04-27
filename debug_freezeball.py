"""Debug script to trace apply_action calls."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

print("=" * 70)
print("CHECKING INITIAL STATE")
print("=" * 70)
print(f"P1 items: {state.player1_items}")
print(f"P2 items: {state.player2_items}")
print(f"P1 frozen: {state.player1_frozen}")
print(f"P2 frozen: {state.player2_frozen}")

print("\n" + "=" * 70)
print("P1 USES FREEZEBALL")
print("=" * 70)

result = state.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"Result keys: {list(result.keys())}")
print(f"Success: {result.get('success', 'N/A')}")
print(f"Message: {result.get('message', 'N/A')}")
print(f"Freeze applied: {result.get('freeze_applied', 'N/A')}")
print(f"Bonus turn granted: {result.get('bonus_turn_granted', 'N/A')}")

print(f"\nState after freezeball:")
print(f"P1 items: {state.player1_items}")
print(f"P2 items: {state.player2_items}")
print(f"P1 frozen: {state.player1_frozen}")
print(f"P2 frozen: {state.player2_frozen}")
print(f"P1 pending_bonus_turn: {state.pending_bonus_turn}")
