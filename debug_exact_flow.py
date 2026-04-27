#!/usr/bin/env python3
"""
Simulate the EXACT GUI phase flow to find where 4 turns come from
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_state import GameState, ActionType

print("="*70)
print("EXACT GUI PHASE SIMULATION")
print("="*70)

state = GameState()
state.player1_pos = [5, 3]
state.player2_pos = [5, 2]

anim_phase = "idle"
actions_log = []

def simulate_phase():
    """Simulate one phase update from the GUI"""
    global anim_phase, state, actions_log
    
    # ── IDLE: start a new round ────────────────────────────────
    if anim_phase == "idle":
        state.advance_turn()
        anim_phase = "player_1_act"
        print(f"[PHASE: idle] → player_1_act")
        return

    # ── Parse current phase ────────────────────────────────────
    parts = anim_phase.split("_")
    try:
        current_player = int(parts[1])
    except (IndexError, ValueError):
        anim_phase = "idle"
        return

    is_bonus = len(parts) > 2 and parts[2] == "bonus"
    
    print(f"[PHASE: {anim_phase}] (is_bonus={is_bonus})")
    print(f"  P1 frozen={state.player1_frozen}, P2 frozen={state.player2_frozen}")

    # ── Check if this player is frozen and should be skipped ───
    frozen = state.player1_frozen if current_player == 1 else state.player2_frozen
    if frozen > 0 and not is_bonus:
        print(f"  → P{current_player} FROZEN, SKIP!")
        state.tick_frozen(current_player)
        if current_player == 1:
            anim_phase = "player_2_act"
        else:
            anim_phase = "idle"
        return

    # ── Execute the action ─────────────────────────────────────
    if current_player == 1:
        if anim_phase == "player_1_act" and state.pending_bonus_turn is None:
            # First P1 action - will it be freezeball?
            action = ActionType.USE_FREEZEBALL if state.player1_items.get('freezeball', 0) > 0 else ActionType.AIM
        else:
            action = ActionType.THROW_SNOWBALL
    else:
        action = ActionType.AIM
    
    result = state.apply_action(current_player, action)
    actions_log.append((current_player, action.name, state.player2_frozen))
    print(f"  → P{current_player}: {action.name}")
    print(f"  → P2 frozen now: {state.player2_frozen}")
    
    # ── Determine next phase ───────────────────────────────────
    bonus_granted = result.get('bonus_turn_granted') and state.pending_bonus_turn == current_player

    if bonus_granted and not is_bonus:
        state.consume_bonus_turn(current_player)
        anim_phase = f"player_{current_player}_bonus"
        print(f"  → Next: player_{current_player}_bonus")
    elif current_player == 1:
        anim_phase = "player_2_act"
        print(f"  → Next: player_2_act")
    else:
        anim_phase = "idle"
        print(f"  → Next: idle")

# Simulate phases
print("\n" + "="*70)
print("PHASE EXECUTION:")
print("="*70)

for i in range(20):  # Max 20 phases to prevent infinite loop
    print()
    simulate_phase()
    
    # Stop after we've cycled through freeze, bonus, skip, and normal play
    if len(actions_log) >= 7:
        print(f"\n[Stopping after {len(actions_log)} actions]")
        break

print("\n" + "="*70)
print("ACTIONS EXECUTED:")
print("="*70)

p1_count = 0
p2_count = 0
for player, action, p2_frozen_after in actions_log:
    print(f"  {len(actions_log) - len(actions_log) + 1}. P{player}: {action:20} (P2 frozen after={p2_frozen_after})")
    if player == 1:
        p1_count += 1
    else:
        p2_count += 1

print(f"\nTotal: P1={p1_count}, P2={p2_count}, Total={p1_count+p2_count}")

print("\n" + "="*70)
if p1_count + p2_count == 4 and p2_count == 0:
    print("✓ CORRECT: P1 got 4 (freeze+bonus + 2 normal), P2 got 0")
elif p1_count + p2_count > 4:
    print(f"✗ BUG: Got {p1_count+p2_count} total actions")
    print("  P2 should be skipped for 2 turns after freezeball!")
else:
    print(f"? Unclear result: P1={p1_count}, P2={p2_count}")

print("="*70)
