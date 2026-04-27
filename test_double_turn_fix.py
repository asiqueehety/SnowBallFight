#!/usr/bin/env python3
"""Test that bonus turns don't cause triple actions"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_state import GameState, ActionType

print("="*70)
print("TESTING DOUBLE TURN FIX (not triple)")
print("="*70)

state = GameState()
state.player1_pos = [5, 3]
state.player2_pos = [5, 2]

p1_actions = []

print("\n[Phase 1] P1 uses freezeball")
result = state.apply_action(1, ActionType.USE_FREEZEBALL)
p1_actions.append("FREEZE")
print(f"  Result: {result['message'][:60]}...")
print(f"  used_bonus_turn: {state.used_bonus_turn}")
print(f"  pending_bonus_turn: {state.pending_bonus_turn}")

print("\n[Phase 2] P1 consumes bonus and acts")
state.consume_bonus_turn(1)
print(f"  After consume_bonus_turn:")
print(f"  used_bonus_turn: {state.used_bonus_turn}")
print(f"  pending_bonus_turn: {state.pending_bonus_turn}")

result = state.apply_action(1, ActionType.THROW_SNOWBALL)
p1_actions.append("THROW (bonus)")
print(f"  Result: {result['message'][:60]}...")

print("\n[Phase 3] P2 skipped (frozen)")
state.tick_frozen(2)  # Simulate P2's skipped turn
print(f"  P2 frozen after tick: {state.player2_frozen}")

print("\n[Phase 4] P1's next normal turn (should be SKIPPED because of bonus)")
print(f"  Before checking: used_bonus_turn = {state.used_bonus_turn}")
if state.used_bonus_turn == 1:
    print(f"  ✓ P1 should SKIP this turn (bonus exhaustion)")
    state.clear_bonus_skip(1)
    p1_actions.append("SKIPPED (bonus exhaustion)")
    print(f"  After clear: used_bonus_turn = {state.used_bonus_turn}")
else:
    print(f"  ✗ P1 would be allowed to act again (BUG!)")
    result = state.apply_action(1, ActionType.THROW_SNOWBALL)
    p1_actions.append("THROW (next normal)")
    print(f"  Result: {result['message'][:60]}...")

print("\n" + "="*70)
print("ACTION SEQUENCE FOR P1:")
print("="*70)
for i, action in enumerate(p1_actions, 1):
    print(f"  {i}. {action}")

print("\n" + "="*70)
if len(p1_actions) == 3 and "SKIPPED" in p1_actions[2]:
    print("✓ CORRECT: P1 gets freeze + bonus + skip = 2 net actions")
elif len(p1_actions) == 2:
    print("✓ CORRECT: P1 gets only freeze + bonus = 2 actions")
else:
    print(f"✗ ERROR: P1 has {len(p1_actions)} actions in sequence")
    if len(p1_actions) > 2:
        print("  This is the triple-turn bug!")

print("="*70)
