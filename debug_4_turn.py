#!/usr/bin/env python3
"""
Trace exactly what's happening with frozen state
to debug the 4-turn issue
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_state import GameState, ActionType

print("="*70)
print("DEBUGGING: 4-TURN ISSUE AFTER FREEZEBALL")
print("="*70)

state = GameState()
state.player1_pos = [5, 3]
state.player2_pos = [5, 2]

turn_actions = []

# ROUND 1
print("\n" + "="*70)
print("ROUND 1: Freezeball Round")
print("="*70)

print("\nPhase 1: P1_ACT - Freezeball")
state.advance_turn()
result = state.apply_action(1, ActionType.USE_FREEZEBALL)
turn_actions.append(('P1', 'FREEZE'))
print(f"  P1 frozen: {state.player1_frozen}")
print(f"  P2 frozen: {state.player2_frozen} ← Should be 2")
print(f"  pending_bonus: {state.pending_bonus_turn}")

print("\nPhase 2: P1_BONUS - Throw")
state.consume_bonus_turn(1)
result = state.apply_action(1, ActionType.THROW_SNOWBALL)
turn_actions.append(('P1', 'THROW (bonus)'))
print(f"  P2 frozen: {state.player2_frozen} ← Still 2")

print("\nPhase 3: P2_ACT - Should SKIP (frozen=2)")
print(f"  Check: P2 frozen = {state.player2_frozen} > 0?")
if state.player2_frozen > 0:
    print(f"  ✓ Yes, should skip")
    state.tick_frozen(2)
    turn_actions.append(('P2', 'SKIP'))
    print(f"  P2 frozen after tick: {state.player2_frozen}")
else:
    print(f"  ✗ No, will act normally (BUG!)")
    result = state.apply_action(2, ActionType.AIM)
    turn_actions.append(('P2', 'AIM'))

# ROUND 2
print("\n" + "="*70)
print("ROUND 2: After Freeze (P2 still frozen?)")
print("="*70)

print("\nPhase 4: P1_ACT (next round)")
state.advance_turn()
print(f"  P1 frozen: {state.player1_frozen}")
print(f"  P2 frozen: {state.player2_frozen} ← Should still be 1")
result = state.apply_action(1, ActionType.AIM)
turn_actions.append(('P1', 'AIM'))

print("\nPhase 5: P2_ACT (next round)")
print(f"  Check: P2 frozen = {state.player2_frozen} > 0?")
if state.player2_frozen > 0:
    print(f"  ✓ Yes, should skip")
    state.tick_frozen(2)
    turn_actions.append(('P2', 'SKIP'))
    print(f"  P2 frozen after tick: {state.player2_frozen}")
else:
    print(f"  ✗ No, will act normally (BUG!)")
    result = state.apply_action(2, ActionType.AIM)
    turn_actions.append(('P2', 'AIM'))

# ROUND 3
print("\n" + "="*70)
print("ROUND 3: Should be normal play")
print("="*70)

print("\nPhase 6: P1_ACT (round 3)")
state.advance_turn()
print(f"  P2 frozen: {state.player2_frozen} ← Should be 0 now")
result = state.apply_action(1, ActionType.AIM)
turn_actions.append(('P1', 'AIM'))

print("\nPhase 7: P2_ACT (round 3) - Should NOW be unfrozen!")
print(f"  Check: P2 frozen = {state.player2_frozen} > 0?")
if state.player2_frozen > 0:
    print(f"  ✗ Still frozen (BUG!)")
    state.tick_frozen(2)
    turn_actions.append(('P2', 'SKIP'))
else:
    print(f"  ✓ Unfrozen, can act")
    result = state.apply_action(2, ActionType.AIM)
    turn_actions.append(('P2', 'AIM'))

# SUMMARY
print("\n" + "="*70)
print("ACTION SUMMARY:")
print("="*70)
p1_count = sum(1 for p, _ in turn_actions if p == 'P1')
p2_count = sum(1 for p, _ in turn_actions if p == 'P2')

for i, (player, action) in enumerate(turn_actions, 1):
    print(f"  {i}. {player}: {action}")

print(f"\nTotal P1 actions: {p1_count}")
print(f"Total P2 actions: {p2_count}")

print("\n" + "="*70)
if p1_count + p2_count == 4:
    print(f"✗ ERROR: Got {p1_count + p2_count} total actions (4 total)")
    print(f"  Expected: P1=3, P2=1 (after freeze wears off)")
    print(f"  Got:      P1={p1_count}, P2={p2_count}")
elif p2_count < 2:
    print(f"✓ CORRECT: {p1_count + p2_count} actions total")
    print(f"  P1: {p1_count} actions (2 normal + 1 bonus)")
    print(f"  P2: {p2_count} actions (skipped while frozen)")
else:
    print(f"? UNCLEAR: P1={p1_count}, P2={p2_count}")

print("="*70)
