"""Watch a full game and count actions."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType
from minimax_agent import MinimaxAgent
from mcts_agent import MCTSAgent

state = GameState()
p1_agent = MinimaxAgent(player_id=1, depth=2)
p2_agent = MCTSAgent(player_id=2, iterations=100)

action_log = {'p1': 0, 'p2': 0}
max_rounds = 10

print("=" * 70)
print("PLAYING FULL GAME - COUNTING ACTIONS")
print("=" * 70)

for round_num in range(max_rounds):
    if state.check_game_over():
        break
    
    print(f"\n[ROUND {round_num}]")
    
    # P1 turn
    if not state.check_game_over():
        actions_p1 = state.get_legal_actions(1)
        if ActionType.USE_FREEZEBALL in actions_p1 and action_log['p1'] == 0:
            # P1 uses freezeball on first chance
            action_p1 = ActionType.USE_FREEZEBALL
            print(f"  P1: Using freezeball")
            action_log['p1'] += 1
        else:
            action_p1 = p1_agent.get_best_action(state)
            print(f"  P1: {action_p1.name}")
            action_log['p1'] += 1
        
        result = state.apply_action(1, action_p1)
        
        # P1 bonus turn if granted
        if result.get('bonus_turn_granted') and state.pending_bonus_turn == 1:
            state.consume_bonus_turn(1)
            actions_p1_bonus = state.get_legal_actions(1)
            action_p1_bonus = p1_agent.get_best_action(state)
            print(f"  P1 BONUS: {action_p1_bonus.name}")
            action_log['p1'] += 1
            result = state.apply_action(1, action_p1_bonus)
    
    # P2 turn
    if not state.check_game_over():
        p2_frozen = state.player2_frozen
        if p2_frozen > 0:
            print(f"  P2: FROZEN (counter={p2_frozen}), skipped")
            state.tick_frozen(2)
        else:
            actions_p2 = state.get_legal_actions(2)
            if ActionType.USE_FREEZEBALL in actions_p2 and action_log['p2'] == 0:
                action_p2 = ActionType.USE_FREEZEBALL
                print(f"  P2: Using freezeball")
                action_log['p2'] += 1
            else:
                action_p2 = p2_agent.get_best_action(state)
                print(f"  P2: {action_p2.name}")
                action_log['p2'] += 1
            
            result = state.apply_action(2, action_p2)
            
            # P2 bonus turn if granted
            if result.get('bonus_turn_granted') and state.pending_bonus_turn == 2:
                state.consume_bonus_turn(2)
                actions_p2_bonus = state.get_legal_actions(2)
                action_p2_bonus = p2_agent.get_best_action(state)
                print(f"  P2 BONUS: {action_p2_bonus.name}")
                action_log['p2'] += 1
                result = state.apply_action(2, action_p2_bonus)

print("\n" + "=" * 70)
print(f"TOTAL ACTIONS - P1: {action_log['p1']}, P2: {action_log['p2']}")
print("=" * 70)

# Count bonus-related actions (freezeball + bonus actions)
print("\nNote: Each player gets freeze + 1 bonus = 2 'advanced' actions max")
print("Then normal actions in subsequent rounds")
