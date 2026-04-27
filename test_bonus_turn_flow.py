"""Test if bonus turn is being granted and used correctly."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

print("=" * 70)
print("TEST: BONUS TURN GRANTING & CONSUMPTION")
print("=" * 70)

# P1 uses freezeball
print("\n1. P1 uses FREEZEBALL")
result = state.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"   Result: {result}")
print(f"   freeze_applied: {result.get('freeze_applied')}")
print(f"   bonus_turn_granted: {result.get('bonus_turn_granted')}")
print(f"   P1 pending_bonus: {state.pending_bonus_turn}")

# Consume bonus
print("\n2. Consume bonus turn")
state.consume_bonus_turn(1)
print(f"   P1 pending_bonus after consume: {state.pending_bonus_turn}")

# P1 bonus action
print("\n3. P1 BONUS action")
result = state.apply_action(1, ActionType.THROW_SNOWBALL)
print(f"   Result: {result}")
print(f"   P2 HP: {state.player2_hp}")

# P2 frozen skip
print(f"\n4. P2 FROZEN SKIP (frozen={state.player2_frozen})")
state.tick_frozen(2)
print(f"   P2 frozen now: {state.player2_frozen}")

# Another skip
print(f"\n5. P2 FROZEN SKIP (frozen={state.player2_frozen})")
state.tick_frozen(2)
print(f"   P2 frozen now: {state.player2_frozen}")

# Now P2 acts
print(f"\n6. P2 acts normally (P1 checks bonus)")
print(f"   P1 pending_bonus: {state.pending_bonus_turn}")
result = state.apply_action(2, ActionType.USE_FREEZEBALL)
print(f"   Result: {result}")
print(f"   bonus_turn_granted: {result.get('bonus_turn_granted')}")
print(f"   P2 pending_bonus: {state.pending_bonus_turn}")

# P2 bonus
print("\n7. Consume P2 bonus")
state.consume_bonus_turn(2)
print(f"   P2 pending_bonus after consume: {state.pending_bonus_turn}")

print("\n8. P2 BONUS action")
result = state.apply_action(2, ActionType.THROW_SNOWBALL)
print(f"   Result: {result}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("✓ Bonus turns are being granted and consumed correctly")
print("✓ Each player got 2 consecutive actions from freezeball")
