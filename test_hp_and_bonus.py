#!/usr/bin/env python3
"""Test HP reduction and bonus turn mechanics"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_state import GameState, ActionType

print("="*60)
print("Testing HP Reduction and Bonus Turn Mechanics")
print("="*60)

# Test 1: Regular snowball hit reduces HP
print("\n[TEST 1] Snowball hit reduces HP:")
state = GameState()
state.player1_pos = [5, 3]
state.player2_pos = [5, 2]
print(f"  Initial P2 HP: {state.player2_hp}")

# P1 throws multiple times until it hits
for i in range(20):
    result = state.apply_action(1, ActionType.THROW_SNOWBALL)
    if result.get('hit', False):
        print(f"  HIT on attempt {i+1}!")
        print(f"  Result: {result['message']}")
        print(f"  Final P2 HP: {state.player2_hp}")
        print(f"  HP reduced: {100 - state.player2_hp == result.get('damage', 0)}")
        break
else:
    print("  No hits in 20 attempts (unlucky!)")

# Test 2: Freezeball + Bonus Turn mechanics
print("\n[TEST 2] Freezeball and Bonus Turn:")
state = GameState()
state.player1_pos = [5, 3]
state.player2_pos = [5, 2]

print(f"  Initial: P1 items={state.player1_items}, P2 frozen={state.player2_frozen}")
print(f"  pending_bonus_turn: {state.pending_bonus_turn}")

# P1 uses freezeball
result1 = state.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"  P1 uses freezeball: {result1['message']}")
print(f"  P2 frozen: {state.player2_frozen}")
print(f"  pending_bonus_turn: {state.pending_bonus_turn}")
print(f"  P1 items after: {state.player1_items}")

# Consume the bonus turn
bonus_was_granted = state.consume_bonus_turn(1)
print(f"  Bonus turn consumed: {bonus_was_granted}")
print(f"  pending_bonus_turn after consume: {state.pending_bonus_turn}")

# P1 should now be able to act again (bonus turn)
legal_actions = state.get_legal_actions(1)
print(f"  P1 legal actions: {[a.name for a in legal_actions]}")

# P1 throws during bonus turn
result2 = state.apply_action(1, ActionType.THROW_SNOWBALL)
print(f"  P1 bonus turn action: {result2['message']}")

# Test 3: Check triple turn bug
print("\n[TEST 3] Check for triple turn scenarios:")
state = GameState()
state.player1_pos = [5, 3]
state.player2_pos = [5, 2]
state.player1_items = {'freezeball': 2, 'medkit': 3}
state.player2_items = {'freezeball': 2, 'medkit': 3}

print(f"  P1 and P2 both have 2 freezeballs")

# P1 uses freezeball on P2
result = state.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"  P1 uses freezeball: {result['message']}")
print(f"  P2 frozen={state.player2_frozen}, pending_bonus={state.pending_bonus_turn}")

# P1 bonus turn - try freezeball again (should work)
state.consume_bonus_turn(1)
result = state.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"  P1 bonus turn (freezeball): {result['message']}")
print(f"  P1 items after 2 freezeballs: {state.player1_items}")
print(f"  pending_bonus_turn after bonus action: {state.pending_bonus_turn}")
print(f"  → Should NOT allow P1 a 3rd turn")

print("\n" + "="*60)
print("Test complete!")
print("="*60)
