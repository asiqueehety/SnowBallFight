"""Trace the EXACT phase flow in GUI to find the 3-turn bug."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

print("=" * 70)
print("PHASE FLOW TRACE - P1 USES FREEZEBALL")
print("=" * 70)

# Simulate phases manually following GUI logic
phase = "idle"
phases = []

for step in range(10):
    phases.append(phase)
    print(f"\nStep {step}: phase='{phase}'")
    
    if phase == "idle":
        state.advance_turn()
        phase = "player_1_act"
        print("  → Transition: idle → player_1_act")
        continue
    
    # Parse phase
    parts = phase.split("_")
    if len(parts) < 2:
        break
    
    try:
        current_player = int(parts[1])
    except:
        break
    
    is_bonus = len(parts) > 2 and parts[2] == "bonus"
    
    # Check frozen
    frozen = state.player1_frozen if current_player == 1 else state.player2_frozen
    print(f"  Player: {current_player}, is_bonus: {is_bonus}, frozen: {frozen}")
    
    if frozen > 0 and not is_bonus:
        print(f"  → P{current_player} is frozen, skip and tick")
        state.tick_frozen(current_player)
        if current_player == 1:
            phase = "player_2_act"
        else:
            phase = "idle"
        print(f"  → Transition: {parts[1]}_act → {phase}")
        continue
    
    # Execute action
    if is_bonus:
        print(f"  → P{current_player} BONUS action (THROW)")
        result = state.apply_action(current_player, ActionType.THROW_SNOWBALL)
        # FIX: After bonus action, go to opponent's turn (so they can use freezeball)
        if current_player == 1:
            phase = "player_2_act"
            print(f"  → Transition: player_1_bonus → player_2_act")
        else:
            phase = "player_1_act"
            print(f"  → Transition: player_2_bonus → player_1_act")
    elif current_player == 1 and step == 1:
        # P1 uses freezeball
        print(f"  → P1 uses FREEZEBALL")
        result = state.apply_action(1, ActionType.USE_FREEZEBALL)
        bonus_granted = result.get('bonus_turn_granted', False)
        print(f"  → Bonus granted: {bonus_granted}")
        if bonus_granted and state.pending_bonus_turn == 1:
            state.consume_bonus_turn(1)
            phase = "player_1_bonus"
            print(f"  → Transition: player_1_act → player_1_bonus")
        else:
            phase = "player_2_act"
    else:
        print(f"  → P{current_player} normal action")
        result = state.apply_action(current_player, ActionType.AIM)
        if current_player == 1:
            phase = "player_2_act"
            print(f"  → Transition: player_1_act → player_2_act")
        else:
            phase = "idle"
            print(f"  → Transition: player_2_act → idle")

print("\n" + "=" * 70)
print("PHASE SEQUENCE")
print("=" * 70)
for i, p in enumerate(phases):
    print(f"{i}: {p}")
