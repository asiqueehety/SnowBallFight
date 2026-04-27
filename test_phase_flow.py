"""Simulate exact GUI phase flow."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

print("=" * 70)
print("SIMULATING EXACT GUI PHASE FLOW")
print("=" * 70)

# Simulate the exact phase sequence
phase = "player_1_act"
turn_count = {'1': 0, '2': 0}

for step in range(10):
    print(f"\nStep {step}: Phase = {phase}")
    
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
        print(f"  P{player} BONUS ACTION: {result.get('message', '')[:40]}...")
        phase = "player_2_act" if player == 1 else "idle"
        turn_count[str(player)] += 1
    elif player == 1 and turn_count['1'] == 0:
        # P1 first action - use freezeball
        result = state.apply_action(player, ActionType.USE_FREEZEBALL)
        print(f"  P{player} FREEZEBALL: {result.get('message', '')[:40]}...")
        bonus_granted = result.get('bonus_turn_granted', False)
        
        if bonus_granted and state.pending_bonus_turn == player:
            state.consume_bonus_turn(player)
            phase = f"player_{player}_bonus"
            turn_count[str(player)] += 1
        else:
            phase = "player_2_act" if player == 1 else "idle"
            turn_count[str(player)] += 1
    else:
        # Normal action
        result = state.apply_action(player, ActionType.THROW_SNOWBALL)
        print(f"  P{player} NORMAL ACTION: {result.get('message', '')[:40]}...")
        phase = "player_2_act" if player == 1 else "idle"
        turn_count[str(player)] += 1

print("\n" + "=" * 70)
print("TURN COUNTS")
print("=" * 70)
print(f"P1 turns: {turn_count['1']}")
print(f"P2 turns: {turn_count['2']}")

if turn_count['1'] > 2:
    print(f"\n❌ ERROR: P1 got {turn_count['1']} turns instead of 2!")
