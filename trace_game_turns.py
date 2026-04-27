#!/usr/bin/env python3
"""Trace the exact turn sequence to detect where the 3rd action comes from"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game.py import SnowballGame

print("="*70)
print("TURN-BY-TURN SEQUENCE TRACE")
print("="*70)

game = SnowballGame(agent1_type="mcts", agent2_type="mcts")

p1_action_count = 0
p2_action_count = 0
turn_log = []

# Play until someone uses a freezeball
freezeball_used = False
turn_limit = 50

for turn in range(turn_limit):
    # Manually trace
    game.state.advance_turn()
    
    # Get actions
    action_p1 = game.agent1.get_best_action(game.state)
    action_p2 = game.agent2.get_best_action(game.state)
    
    # Apply actions
    result_p1 = game.state.apply_action(1, action_p1)
    result_p2 = game.state.apply_action(2, action_p2)
    
    turn_log.append({
        'turn': turn,
        'p1_action': action_p1.name,
        'p1_result': result_p1['message'][:50],
        'p1_freezeball': result_p1.get('freeze_applied', False),
        'p1_bonus': result_p1.get('bonus_turn_granted', False),
        'p2_action': action_p2.name,
        'p2_result': result_p2['message'][:50],
        'p2_frozen': game.state.player2_frozen,
        'pending_bonus': game.state.pending_bonus_turn,
    })
    
    if result_p1.get('freeze_applied'):
        print(f"\n✓ Freezeball used by P1 at turn {turn}!")
        freezeball_used = True
        
        # Trace the next few turns
        print(f"\nSequence after freezeball:")
        print(f"  Turn {turn}: P1 uses freezeball")
        print(f"    - pending_bonus_turn: {game.state.pending_bonus_turn}")
        print(f"    - P2 frozen: {game.state.player2_frozen}")
        
        # Continue for next few turns
        for i in range(1, 5):
            if turn + i >= turn_limit:
                break
            game.state.advance_turn()
            
            next_p1_action = game.agent1.get_best_action(game.state)
            next_p2_action = game.agent2.get_best_action(game.state)
            
            next_p1_result = game.state.apply_action(1, next_p1_action)
            next_p2_result = game.state.apply_action(2, next_p2_action)
            
            print(f"  Turn {turn+i}: P1 {next_p1_action.name}, P2 {next_p2_action.name}")
            print(f"    - P1: {next_p1_result['message'][:60]}...")
            print(f"    - P2: {next_p2_result['message'][:60]}...")
            print(f"    - P2 frozen: {game.state.player2_frozen}, pending_bonus: {game.state.pending_bonus_turn}")
        
        break

print("\n" + "="*70)
if freezeball_used:
    print("Analysis: Check the sequence above to see if P1 gets more than 2 actions")
    print("in the immediate freeze-bonus window.")
else:
    print("No freezeball used in first 50 turns (unlikely but possible)")

print("="*70)
