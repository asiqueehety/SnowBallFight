#!/usr/bin/env python3
"""Test frozen mechanics explicitly"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_state import GameState, ActionType

# Create game state
state = GameState()

print("="*60)
print("Testing Frozen Mechanics")
print("="*60)

# Move players closer
state.player1_pos = [4, 3]
state.player2_pos = [5, 2]

print(f"\nInitial state:")
print(f"  P1 snowballs: {state.player1_snowballs}")
print(f"  P1 frozen: {state.player1_frozen}")
print(f"  P2 snowballs: {state.player2_snowballs}")
print(f"  P2 frozen: {state.player2_frozen}")

# Player 1 uses freezeball
print(f"\nP1 uses freezeball:")
result = state.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"  Result: {result['message']}")
print(f"  P2 frozen counter: {state.player2_frozen}")

# Try to get legal actions for frozen player
print(f"\nP2 legal actions when frozen:")
legal_actions = state.get_legal_actions(2)
print(f"  Legal actions: {[a.name for a in legal_actions]}")

# Try P2 to use MEDKIT (should fail)
print(f"\nP2 tries to use MEDKIT while frozen:")
result = state.apply_action(2, ActionType.USE_MEDKIT)
print(f"  Result: {result}")
print(f"  Success: {result['success']}")
print(f"  Message: {result['message']}")

# Try P2 to move (should fail)
print(f"\nP2 tries to move LEFT while frozen:")
result = state.apply_action(2, ActionType.MOVE_LEFT)
print(f"  Result: {result}")
print(f"  Success: {result['success']}")
print(f"  Message: {result['message']}")

# P2 should only be able to AIM
print(f"\nP2 tries to AIM while frozen:")
result = state.apply_action(2, ActionType.AIM)
print(f"  Result: {result}")
print(f"  Success: {result['success']}")
print(f"  Message: {result['message']}")

# Advance turn (should decrement frozen counter)
print(f"\nAdvance turn (frozen counter: {state.player2_frozen} -> {state.player2_frozen - 1}):")
state.advance_turn()
print(f"  P2 frozen counter: {state.player2_frozen}")

# Check legal actions again after 1st turn
print(f"\nP2 legal actions after 1st frozen turn:")
legal_actions = state.get_legal_actions(2)
print(f"  Legal actions: {[a.name for a in legal_actions]}")

# Advance turn again
print(f"\nAdvance turn (frozen counter: {state.player2_frozen} -> {state.player2_frozen - 1}):")
state.advance_turn()
print(f"  P2 frozen counter: {state.player2_frozen}")

# Check legal actions when unfrozen
print(f"\nP2 legal actions when unfrozen:")
legal_actions = state.get_legal_actions(2)
print(f"  Legal actions: {[a.name for a in legal_actions]}")

print("\n" + "="*60)
print("Frozen mechanics test complete!")
print("="*60)
