"""Debug script to count total turns each player gets."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

# Track actions
p1_actions = []
p2_actions = []

print("=" * 70)
print("SIMULATING: P1 uses freezeball, then both play until one unfrozen")
print("=" * 70)

# P1 uses freezeball
result = state.apply_action(1, ActionType.USE_FREEZEBALL)
p1_actions.append("USE_FREEZEBALL")
print(f"\n1. P1 uses freezeball: {result['message']}")
print(f"   P1 pending_bonus_turn: {state.pending_bonus_turn}")
print(f"   P2 frozen: {state.player2_frozen}")

# P1 takes bonus action (assuming same turn in GUI)
state.consume_bonus_turn(1)
result = state.apply_action(1, ActionType.THROW_SNOWBALL)
p1_actions.append("THROW_SNOWBALL (BONUS)")
print(f"\n2. P1 takes bonus action: {result['message']}")

# P2 is frozen, so skips (but we simulate here)
print(f"\n3. P2 is frozen ({state.player2_frozen}), SKIPPED")
state.tick_frozen(2)
print(f"   P2 frozen now: {state.player2_frozen}")

# P1 normal turn
result = state.apply_action(1, ActionType.THROW_SNOWBALL)
p1_actions.append("THROW_SNOWBALL (NORMAL)")
print(f"\n4. P1 normal action: {result['message']}")

# P2 is still frozen, skips again
print(f"\n5. P2 is frozen ({state.player2_frozen}), SKIPPED")
state.tick_frozen(2)
print(f"   P2 frozen now: {state.player2_frozen}")

# Now P2 should act
result = state.apply_action(2, ActionType.THROW_SNOWBALL)
p2_actions.append("THROW_SNOWBALL")
print(f"\n6. P2 normal action: {result['message']}")

# P1 acts
result = state.apply_action(1, ActionType.THROW_SNOWBALL)
p1_actions.append("THROW_SNOWBALL")
print(f"\n7. P1 normal action: {result['message']}")

# P2 acts
result = state.apply_action(2, ActionType.THROW_SNOWBALL)
p2_actions.append("THROW_SNOWBALL")
print(f"\n8. P2 normal action: {result['message']}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"P1 actions ({len(p1_actions)}): {p1_actions}")
print(f"P2 actions ({len(p2_actions)}): {p2_actions}")
print(f"\nTotal P1 turns: {len(p1_actions)}")
print(f"Total P2 turns: {len(p2_actions)}")

if len(p1_actions) > 2:
    print(f"\n❌ ERROR: P1 got {len(p1_actions)} turns instead of 2!")
if len(p2_actions) < 2:
    print(f"\n⚠️  WARNING: P2 only got {len(p2_actions)} turns while frozen")
