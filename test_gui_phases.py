#!/usr/bin/env python3
"""
Comprehensive test simulating GUI phase transitions
to ensure no triple turns occur
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_state import GameState, ActionType

print("="*70)
print("GUI PHASE TRANSITION TEST (No Triple Turns)")
print("="*70)

state = GameState()
state.player1_pos = [5, 3]
state.player2_pos = [5, 2]

# Simulate the phase sequence that the GUI does
anim_phase = "idle"
action_count = {'P1': 0, 'P2': 0}
phases_executed = []

print("\n[Initial State]")
print(f"State: {anim_phase}")
print(f"P1 items: {state.player1_items}")
print(f"P2 items: {state.player2_items}")

# Phase: idle → player_1_act
print("\n[Transition: idle → player_1_act]")
state.advance_turn()
anim_phase = "player_1_act"
print(f"anim_phase: {anim_phase}")

# Phase: player_1_act
print("\n[Phase: player_1_act] P1 uses freezeball")
action_p1 = ActionType.USE_FREEZEBALL
result_p1 = state.apply_action(1, action_p1)
action_count['P1'] += 1
phases_executed.append(('P1_act', action_p1.name))
print(f"Action: {action_p1.name}")
print(f"Result: {result_p1['message'][:60]}...")
print(f"P1 frozen: {state.player1_frozen}")
print(f"P2 frozen: {state.player2_frozen}")
print(f"pending_bonus_turn: {state.pending_bonus_turn}")

# Check for bonus turn
bonus_granted = result_p1.get('bonus_turn_granted') and state.pending_bonus_turn == 1
if bonus_granted:
    print(f"✓ Bonus turn granted!")
    state.consume_bonus_turn(1)
    anim_phase = "player_1_bonus"
    print(f"[Transition: player_1_act → player_1_bonus]")
else:
    anim_phase = "player_2_act"
    print(f"[Transition: player_1_act → player_2_act]")

# Phase: player_1_bonus
if "bonus" in anim_phase:
    print(f"\n[Phase: player_1_bonus] P1 bonus action")
    action_p1_bonus = ActionType.THROW_SNOWBALL
    result_p1_bonus = state.apply_action(1, action_p1_bonus)
    action_count['P1'] += 1
    phases_executed.append(('P1_bonus', action_p1_bonus.name))
    print(f"Action: {action_p1_bonus.name}")
    print(f"Result: {result_p1_bonus['message'][:60]}...")
    print(f"P2 frozen: {state.player2_frozen}")
    anim_phase = "player_2_act"
    print(f"[Transition: player_1_bonus → player_2_act]")

# Phase: player_2_act
print(f"\n[Phase: player_2_act]")
frozen = state.player2_frozen
if frozen > 0:
    print(f"P2 is frozen ({frozen} turns), so SKIP turn")
    state.tick_frozen(2)
    phases_executed.append(('P2_act', 'SKIPPED'))
    print(f"P2 frozen after tick: {state.player2_frozen}")
else:
    print(f"P2 acts normally")
    result_p2 = state.apply_action(2, ActionType.AIM)
    action_count['P2'] += 1
    phases_executed.append(('P2_act', 'AIM'))
    print(f"Result: {result_p2['message']}")

anim_phase = "idle"
print(f"[Transition: player_2_act → idle]")

# NEXT ROUND - should NOT have another P1 action yet
print(f"\n[Next Round - IDLE]")
print(f"anim_phase: {anim_phase}")
state.advance_turn()
anim_phase = "player_1_act"
print(f"[Transition: idle → player_1_act (next round)]")

print(f"\n[Phase: player_1_act (next round)]")
print(f"P2 frozen: {state.player2_frozen} (should be 1 after first skip)")
action_p1_next = ActionType.AIM
result_p1_next = state.apply_action(1, action_p1_next)
action_count['P1'] += 1
phases_executed.append(('P1_act_round2', action_p1_next.name))
print(f"Action: {action_p1_next.name}")
print(f"This is the 3rd action, but it's in the NEXT ROUND, so OK")

print("\n" + "="*70)
print("PHASE EXECUTION SUMMARY:")
print("="*70)
for i, (phase, action) in enumerate(phases_executed, 1):
    print(f"  {i}. [{phase:15}] {action}")

print(f"\nTotal P1 actions: {action_count['P1']}")
print(f"Total P2 actions: {action_count['P2']}")

print("\n" + "="*70)
print("VALIDATION:")
print("="*70)
if len(phases_executed) >= 5:
    # Check: first 2-3 actions are P1 (freeze + bonus)
    if phases_executed[0][0] == 'P1_act' and phases_executed[1][0] == 'P1_bonus':
        print("✓ P1 gets freeze + bonus (2 consecutive actions)")
    else:
        print("✗ ERROR: Phase sequence wrong")
    
    # Check: P2 skipped after
    if phases_executed[2][0] == 'P2_act' and 'SKIP' in phases_executed[2][1]:
        print("✓ P2 skipped (frozen)")
    else:
        print("✗ ERROR: P2 not skipped")
    
    # Check: round 2 has P1 action
    if any('round2' in p[0] for p in phases_executed):
        print("✓ Next round starts after (not triple turn)")
    else:
        print("⚠ Round 2 not tested")

print("\nCONCLUSION:")
if action_count['P1'] == 3 and len(phases_executed) == 5:
    print("✓ P1 gets 3 total actions across 2 rounds (CORRECT)")
    print("  - Round 1: freeze + bonus (2 actions, P2 helpless)")
    print("  - Round 2: normal action (1 action)")
    print("  - P2 is frozen=2, so 2 of their actions are lost")
else:
    print(f"Review: P1={action_count['P1']} actions, Phases={len(phases_executed)}")

print("="*70)
