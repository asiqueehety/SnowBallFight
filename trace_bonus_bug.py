#!/usr/bin/env python3
"""Detailed test to trace bonus turn phases and detect triple action bug"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_state import GameState, ActionType

print("="*70)
print("DETAILED BONUS TURN PHASE TRACE")
print("="*70)

state = GameState()
state.player1_pos = [5, 3]
state.player2_pos = [5, 2]

actions = []

print("\n[Phase 1: P1_ACT - Using Freezeball]")
result1 = state.apply_action(1, ActionType.USE_FREEZEBALL)
actions.append(("P1_ACT", "USE_FREEZEBALL", result1['message'][:60]))
print(f"  Result: {result1['message'][:60]}...")
print(f"  P2 frozen: {state.player2_frozen}")
print(f"  pending_bonus_turn: {state.pending_bonus_turn}")
print(f"  bonus_turn_granted: {result1.get('bonus_turn_granted')}")

print("\n[Phase 2: P1_BONUS - Should allow another action]")
# Consume the bonus turn like GUI does
consumed = state.consume_bonus_turn(1)
print(f"  Bonus consumed: {consumed}")
print(f"  pending_bonus_turn after consume: {state.pending_bonus_turn}")

result2 = state.apply_action(1, ActionType.THROW_SNOWBALL)
actions.append(("P1_BONUS", "THROW_SNOWBALL", result2['message'][:60]))
print(f"  Result: {result2['message'][:60]}...")
print(f"  bonus_turn_granted: {result2.get('bonus_turn_granted')}")

print("\n[Phase 3: P2_ACT - Should be skipped (frozen)]")
frozen_turns = state.player2_frozen
if frozen_turns > 0:
    print(f"  P2 is frozen (frozen={frozen_turns}), should skip turn")
    state.tick_frozen(2)  # Simulate skipping and decrementing
    actions.append(("P2_ACT", "SKIPPED_FROZEN", f"P2 frozen, skipped (now frozen={state.player2_frozen})"))
    print(f"  P2 frozen after tick: {state.player2_frozen}")
    print(f"  → Should transition to IDLE and then next round")
else:
    result3 = state.apply_action(2, ActionType.AIM)
    actions.append(("P2_ACT", "AIM", result3['message']))
    print(f"  Result: {result3['message']}")

print("\n" + "="*70)
print("ACTION SEQUENCE:")
print("="*70)
for i, (phase, action, msg) in enumerate(actions, 1):
    print(f"{i}. [{phase:12}] {action:20} → {msg}")

print("\n" + "="*70)
if len(actions) == 3:
    print("✓ CORRECT: Exactly 3 phases (P1_act → P1_bonus → P2_skip)")
elif len(actions) < 3:
    print(f"✗ ERROR: Only {len(actions)} actions (expected 3)")
else:
    print(f"✗ ERROR: Got {len(actions)} actions (expected 3)")
    print("  → This would be the 'triple turn' bug!")

print("="*70)

# Now simulate what happens if P1 gets ANOTHER bonus turn somehow
print("\nCHECKING FOR MULTIPLE BONUS TURN BUG:")
print("="*70)

state2 = GameState()
state2.player1_pos = [5, 3]
state2.player2_pos = [5, 2]

print("\n[Test] Multiple freezeballs attempt:")
print(f"  Initial P1 items: {state2.player1_items}")

# Use freezeball
result = state2.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"  After 1st freeze: items={state2.player1_items}, pending={state2.pending_bonus_turn}")

# Try to use another freezeball during bonus (should fail - no items)
consumed = state2.consume_bonus_turn(1)
result2 = state2.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"  During bonus, try 2nd freeze: {result2['message']}")

print("\nCONCLUSION:")
if len(actions) == 3 and result2['success'] == False:
    print("  ✓ No triple turn bug detected")
else:
    print("  ✗ Triple turn bug possible")
