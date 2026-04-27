"""Trace exact turn sequence and action counts."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType
from minimax_agent import MinimaxAgent
from mcts_agent import MCTSAgent

state = GameState()
p1_agent = MinimaxAgent(player_id=1, depth=2)
p2_agent = MCTSAgent(player_id=2, iterations=100)

print("=" * 70)
print("EXACT TURN SEQUENCE - WHO ACTS WHEN")
print("=" * 70)

action_sequence = []
action_count = {'p1': 0, 'p2': 0}

max_rounds = 5

for round_num in range(max_rounds):
    if state.check_game_over():
        break
    
    print(f"\n{'='*70}")
    print(f"ROUND {round_num}")
    print(f"{'='*70}")
    
    # P1 turn
    print(f"\n[P1's turn sequence]")
    p1_round_actions = 0
    
    if not state.check_game_over():
        p1_frozen = state.player1_frozen
        if p1_frozen > 0:
            print(f"  P1 FROZEN (counter={p1_frozen}), skips")
            state.tick_frozen(1)
            p1_round_actions += 1
        else:
            actions_p1 = state.get_legal_actions(1)
            if ActionType.USE_FREEZEBALL in actions_p1 and action_count['p1'] == 0:
                action_p1 = ActionType.USE_FREEZEBALL
                print(f"  P1 Action 1: USE FREEZEBALL")
                action_count['p1'] += 1
                p1_round_actions += 1
                action_sequence.append(('P1', 'FREEZEBALL'))
            else:
                action_p1 = p1_agent.get_best_action(state)
                print(f"  P1 Action 1: {action_p1.name}")
                action_count['p1'] += 1
                p1_round_actions += 1
                action_sequence.append(('P1', action_p1.name))
            
            result = state.apply_action(1, action_p1)
            
            # Check for bonus
            if result.get('bonus_turn_granted') and state.pending_bonus_turn == 1:
                state.consume_bonus_turn(1)
                actions_p1_bonus = state.get_legal_actions(1)
                action_p1_bonus = p1_agent.get_best_action(state)
                print(f"  P1 Action 2 (BONUS): {action_p1_bonus.name}")
                action_count['p1'] += 1
                p1_round_actions += 1
                action_sequence.append(('P1', f'{action_p1_bonus.name} [BONUS]'))
                result = state.apply_action(1, action_p1_bonus)
    
    # P2 turn
    print(f"\n[P2's turn sequence]")
    p2_round_actions = 0
    
    if not state.check_game_over():
        p2_frozen = state.player2_frozen
        if p2_frozen > 0:
            print(f"  P2 FROZEN (counter={p2_frozen}), skips")
            state.tick_frozen(2)
            p2_round_actions += 1
            action_sequence.append(('P2', 'SKIPPED [FROZEN]'))
        else:
            actions_p2 = state.get_legal_actions(2)
            if ActionType.USE_FREEZEBALL in actions_p2 and action_count['p2'] == 0:
                action_p2 = ActionType.USE_FREEZEBALL
                print(f"  P2 Action 1: USE FREEZEBALL")
                action_count['p2'] += 1
                p2_round_actions += 1
                action_sequence.append(('P2', 'FREEZEBALL'))
            else:
                action_p2 = p2_agent.get_best_action(state)
                print(f"  P2 Action 1: {action_p2.name}")
                action_count['p2'] += 1
                p2_round_actions += 1
                action_sequence.append(('P2', action_p2.name))
            
            result = state.apply_action(2, action_p2)
            
            # Check for bonus
            if result.get('bonus_turn_granted') and state.pending_bonus_turn == 2:
                state.consume_bonus_turn(2)
                actions_p2_bonus = state.get_legal_actions(2)
                action_p2_bonus = p2_agent.get_best_action(state)
                print(f"  P2 Action 2 (BONUS): {action_p2_bonus.name}")
                action_count['p2'] += 1
                p2_round_actions += 1
                action_sequence.append(('P2', f'{action_p2_bonus.name} [BONUS]'))
                result = state.apply_action(2, action_p2_bonus)
    
    print(f"\nRound {round_num} summary: P1 did {p1_round_actions} action(s), P2 did {p2_round_actions} action(s)")

print("\n" + "=" * 70)
print("FULL ACTION SEQUENCE")
print("=" * 70)
for i, (player, action) in enumerate(action_sequence, 1):
    print(f"{i:2d}. {player}: {action}")

print("\n" + "=" * 70)
print("TOTALS")
print("=" * 70)
print(f"P1 total actions: {action_count['p1']}")
print(f"P2 total actions: {action_count['p2']}")
print(f"\nP1 should get: 2 (freeze + bonus) + normal actions")
print(f"P2 should get: 2 (freeze + bonus) + normal actions")
