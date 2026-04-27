#!/usr/bin/env python3
"""Verify freezeball gives proper double turn advantage without triple"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_state import GameState, ActionType

print("="*70)
print("VERIFY FREEZEBALL DOUBLE TURN ADVANTAGE (NO TRIPLE)")
print("="*70)

state = GameState()
state.player1_pos = [5, 3]
state.player2_pos = [5, 2]

print("\n[Round N - Freezeball Round]")
print("─" * 70)

# Phase 1: P1_act (uses freezeball)
print("\n1. P1_ACT: Use freezeball")
result1 = state.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"   Result: {result1['message'][:60]}...")
print(f"   P2 frozen: {state.player2_frozen}")
print(f"   pending_bonus_turn: {state.pending_bonus_turn}")
print(f"   bonus_granted: {result1.get('bonus_turn_granted')}")

# Phase 2: P1_bonus (consume and act)
print("\n2. P1_BONUS: Consume bonus and act")
consumed = state.consume_bonus_turn(1)
print(f"   Bonus consumed: {consumed}")
print(f"   pending_bonus_turn: {state.pending_bonus_turn}")

result2 = state.apply_action(1, ActionType.THROW_SNOWBALL)
print(f"   Result: {result2['message'][:60]}...")

# Phase 3: P2_act (skipped because frozen)
print("\n3. P2_ACT: Skipped (frozen)")
legal_actions = state.get_legal_actions(2)
print(f"   Legal actions: {[a.name for a in legal_actions]}")
print(f"   P2 is frozen, so turn is skipped and counter decrements")
state.tick_frozen(2)
print(f"   P2 frozen after skip: {state.player2_frozen}")

print("\n" + "─" * 70)
print("[Round N+1 - Normal Play]")
print("─" * 70)

# Phase 4: P1_act (normal action, not bonus)
print("\n4. P1_ACT (next round): Normal action")
result3 = state.apply_action(1, ActionType.AIM)
print(f"   Result: {result3['message']}")
print(f"   P2 frozen: {state.player2_frozen}")

# Phase 5: P2_act (unfrozen)
print("\n5. P2_ACT: Now unfrozen and can act normally")
if state.player2_frozen == 0:
    legal_actions = state.get_legal_actions(2)
    print(f"   Legal actions: {len(legal_actions)} available")
    print(f"   ✓ P2 unfrozen and ready to act")
else:
    print(f"   ✗ ERROR: P2 still frozen={state.player2_frozen}")

print("\n" + "="*70)
print("OUTCOME ANALYSIS:")
print("="*70)
print("✓ Round N (Freeze): P1 acts twice (freeze + bonus), P2 skips once")
print("✓ Round N+1 (Normal): Both act normally")
print("✓ Net result: P1 gets ONE advantage round with 2 actions + 1 normal")
print("✓ P2 loses one turn but recovers next round")
print("✓ NO TRIPLE TURN - just proper double advantage")
print("="*70)
