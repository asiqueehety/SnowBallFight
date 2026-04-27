"""Simulate GUI phase transitions with the fix."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

print("=" * 70)
print("GUI PHASE SIMULATION (with bonus->idle fix)")
print("=" * 70)

# Simulate the exact phase sequence with the fix
phase = "idle"
turn_count = {'1': 0, '2': 0}
phase_sequence = []

for step in range(15):
    print(f"\nStep {step}: Phase = {phase}")
    phase_sequence.append(phase)
    
    if phase == "idle":
        state.advance_turn()
        phase = "player_1_act"
        print("  → Starting new round")
        continue
    
    # Extract player from phase
    if "player_1" in phase:
        player = 1
    elif "player_2" in phase:
        player = 2
    else:
        break
    
    is_bonus = "bonus" in phase
    
    # Check if frozen
    frozen = state.player1_frozen if player == 1 else state.player2_frozen
    
    if frozen > 0 and not is_bonus:
        print(f"  P{player} FROZEN (counter={frozen}), SKIP")
        state.tick_frozen(player)
        
        if player == 1:
            phase = "player_2_act"
        else:
            phase = "idle"
        continue
    
    # Execute action
    if is_bonus:
        # Bonus action
        result = state.apply_action(player, ActionType.THROW_SNOWBALL)
        print(f"  P{player} BONUS ACTION: THROW")
        turn_count[str(player)] += 1
        
        # FIX: After bonus action, go to idle (not next player)
        phase = "idle"
        
    elif player == 1 and turn_count['1'] == 0:
        # P1 first action - use freezeball
        result = state.apply_action(player, ActionType.USE_FREEZEBALL)
        print(f"  P{player} FREEZEBALL")
        bonus_granted = result.get('bonus_turn_granted', False)
        
        if bonus_granted and state.pending_bonus_turn == player:
            state.consume_bonus_turn(player)
            phase = f"player_{player}_bonus"
            turn_count[str(player)] += 1
        else:
            phase = "player_2_act"
            turn_count[str(player)] += 1
    else:
        # Normal action
        result = state.apply_action(player, ActionType.THROW_SNOWBALL)
        print(f"  P{player} NORMAL ACTION: THROW")
        
        if player == 1:
            phase = "player_2_act"
        else:
            phase = "idle"
        turn_count[str(player)] += 1

print("\n" + "=" * 70)
print("PHASE SEQUENCE")
print("=" * 70)
for i, p in enumerate(phase_sequence):
    print(f"{i:2d}. {p}")

print("\n" + "=" * 70)
print("TURN COUNTS")
print("=" * 70)
print(f"P1 turns: {turn_count['1']}")
print(f"P2 turns: {turn_count['2']}")

if turn_count['1'] <= 2:
    print(f"\n✓ P1 correctly got {turn_count['1']} turns (freeze + bonus or skip)")
else:
    print(f"\n❌ ERROR: P1 got {turn_count['1']} turns instead of max 2 in window")
