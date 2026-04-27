"""Test the freezeball action prevention logic."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

print("=" * 70)
print("TEST: P1 FREEZE SHOULD PREVENT EXTRA ACTIONS")
print("=" * 70)

# Simulate the GUI phase logic manually
p1_actions = []
p2_actions = []
freezeball_active = None  # Track which player used freezeball

print("\n1. P1 uses FREEZEBALL")
result = state.apply_action(1, ActionType.USE_FREEZEBALL)
freezeball_active = 1
p1_actions.append("FREEZEBALL")
state.consume_bonus_turn(1)

print("2. P1 uses BONUS")
result = state.apply_action(1, ActionType.THROW_SNOWBALL)
p1_actions.append("BONUS")
print(f"   P2 frozen: {state.player2_frozen}")

print("\n3. P2 turn (should skip - frozen)")
p2_frozen = state.player2_frozen
if p2_frozen > 0:
    state.tick_frozen(2)
    print(f"   P2 SKIPPED (was frozen={p2_frozen + 1})")
    print(f"   P2 frozen now: {state.player2_frozen}")

# Key check: should P1 get another action now?
print("\n4. P1 turn again (CHECK FIX):")
p2_frozen_check = state.player2_frozen
if freezeball_active == 1 and p2_frozen_check > 0:
    print(f"   ❌ P1 used freeze + bonus, P2 still frozen={p2_frozen_check}")
    print(f"   ✓ Should NOT allow P1 normal action")
    print(f"   → Go to IDLE instead")
elif freezeball_active == 1 and p2_frozen_check == 0:
    print(f"   ✓ P2 unfrozen, now allow P1 to act normally")
    result = state.apply_action(1, ActionType.THROW_SNOWBALL)
    p1_actions.append("NORMAL")
else:
    print(f"   Normal case")
    result = state.apply_action(1, ActionType.THROW_SNOWBALL)
    p1_actions.append("NORMAL")

print("\n5. P2 can now use freezeball")
freezeball_active = None  # Clear when switching players
result = state.apply_action(2, ActionType.USE_FREEZEBALL)
freezeball_active = 2
p2_actions.append("FREEZEBALL")
state.consume_bonus_turn(2)

print("6. P2 uses BONUS")
result = state.apply_action(2, ActionType.THROW_SNOWBALL)
p2_actions.append("BONUS")
print(f"   P1 frozen: {state.player1_frozen}")

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)
print(f"P1 actions in freeze window: {p1_actions}")
print(f"P2 actions in freeze window: {p2_actions}")

if len(p1_actions) == 2 and len(p2_actions) == 2:
    print("\n✅ BALANCED: Both get exactly 2 actions!")
elif len(p1_actions) > 2:
    print(f"\n❌ UNBALANCED: P1 got {len(p1_actions)} instead of 2")
elif len(p2_actions) > 2:
    print(f"\n❌ UNBALANCED: P2 got {len(p2_actions)} instead of 2")
