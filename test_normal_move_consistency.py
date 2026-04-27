"""Test normal move consistency through game phases."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

print("=" * 70)
print("TEST: NORMAL MOVE CONSISTENCY")
print("=" * 70)

# Track normal moves and freezeballs
moves_log = []

print("\n--- GAME FLOW 1: Normal moves only ---")
state = GameState()
for turn in range(4):
    player = 1 if turn % 2 == 0 else 2
    result = state.apply_action(player, ActionType.THROW_SNOWBALL)
    moves_log.append(f"Turn {turn}: P{player} normal throw → {result['message'][:30]}")
    print(f"Turn {turn}: P{player} normal throw → {result['message'][:50]}")

print("\n--- GAME FLOW 2: P1 freeze, then normal moves ---")
state = GameState()
moves_log.clear()

# P1 freezes
print("\n1. P1 FREEZE")
result = state.apply_action(1, ActionType.USE_FREEZEBALL)
print(f"   Result: {result['message'][:50]}")
moves_log.append("P1 freeze")
state.consume_bonus_turn(1)

# P1 bonus
print("2. P1 BONUS (after freeze)")
result = state.apply_action(1, ActionType.THROW_SNOWBALL)
print(f"   Result: {result['message'][:50]}")
moves_log.append("P1 bonus")
print(f"   P2 frozen counter: {state.player2_frozen}")

# P2 should skip (frozen)
print("3. P2 FROZEN SKIP")
if state.player2_frozen > 0:
    state.tick_frozen(2)
    print(f"   Skipped, P2 frozen now: {state.player2_frozen}")
    moves_log.append("P2 skip (frozen)")
else:
    print("   ERROR: P2 should be frozen!")

# P1 normal move - THIS IS WHERE INCONSISTENCY HAPPENS
print("4. P1 NORMAL MOVE (after freeze)")
try:
    result = state.apply_action(1, ActionType.THROW_SNOWBALL)
    print(f"   Result: {result['message'][:50]}")
    print(f"   ✓ P1 normal move succeeded")
    moves_log.append("P1 normal after freeze")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    moves_log.append("P1 normal FAILED")

# P2 normal move when unfrozen
print("5. P2 NORMAL MOVE (now unfrozen)")
if state.player2_frozen == 0:
    try:
        result = state.apply_action(2, ActionType.THROW_SNOWBALL)
        print(f"   Result: {result['message'][:50]}")
        print(f"   ✓ P2 normal move succeeded")
        moves_log.append("P2 normal after unfreeze")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        moves_log.append("P2 normal FAILED")
else:
    print(f"   ERROR: P2 still frozen ({state.player2_frozen}), can't move!")
    moves_log.append("P2 still frozen")

# P1 normal move again
print("6. P1 NORMAL MOVE (repeated)")
try:
    result = state.apply_action(1, ActionType.THROW_SNOWBALL)
    print(f"   Result: {result['message'][:50]}")
    print(f"   ✓ P1 normal move succeeded")
    moves_log.append("P1 normal 2nd")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    moves_log.append("P1 normal 2nd FAILED")

print("\n" + "=" * 70)
print("CONSISTENCY CHECK")
print("=" * 70)
for i, move in enumerate(moves_log):
    print(f"{i+1}. {move}")

failed = [m for m in moves_log if "FAILED" in m]
if failed:
    print(f"\n❌ INCONSISTENCY DETECTED: {len(failed)} moves failed")
    for f in failed:
        print(f"   - {f}")
else:
    print(f"\n✓ All moves succeeded - CONSISTENT!")
