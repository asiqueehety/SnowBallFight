"""Trace game phases and bonus turn detection."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

print("=" * 70)
print("PHASE TRACE: BONUS TURN DETECTION")
print("=" * 70)

class GameTracer:
    def __init__(self):
        self.phase = "idle"
        self.freezeball_active_player = None
        self.events = []
        self.turn_count = 0
        
    def update(self):
        """Simulate one update cycle."""
        self.turn_count += 1
        
        # Handle idle
        if self.phase == "idle":
            state.advance_turn()
            self.phase = "player_1_act"
            self.events.append(f"Turn {self.turn_count}: idle → player_1_act")
            return
        
        # Parse phase
        parts = self.phase.split("_")
        if len(parts) < 2:
            return
        
        try:
            current_player = int(parts[1])
        except (IndexError, ValueError):
            return
        
        is_bonus = len(parts) > 2 and parts[2] == "bonus"
        
        # Check frozen
        frozen = state.player1_frozen if current_player == 1 else state.player2_frozen
        if frozen > 0 and not is_bonus:
            state.tick_frozen(current_player)
            if current_player == 1:
                self.phase = "player_2_act"
            else:
                self.phase = "idle"
            self.events.append(f"Turn {self.turn_count}: P{current_player} frozen skip, go to next phase")
            return
        
        # Determine action
        if is_bonus:
            action = ActionType.THROW_SNOWBALL
            action_name = "BONUS throw"
        elif self.turn_count <= 3:
            action = ActionType.USE_FREEZEBALL
            action_name = "FREEZE"
        else:
            action = ActionType.THROW_SNOWBALL
            action_name = "normal throw"
        
        # Execute
        result = state.apply_action(current_player, action)
        bonus_granted = result.get('bonus_turn_granted', False)
        
        self.events.append(f"Turn {self.turn_count}: P{current_player}{' [BONUS]' if is_bonus else ''} {action_name} → P{2 if current_player == 1 else 1} HP={state.player2_hp if current_player == 1 else state.player1_hp}")
        
        # CHECK: Is there a pending bonus turn?
        pending = state.pending_bonus_turn
        self.events[-1] += f" | pending_bonus={pending}"
        
        if bonus_granted:
            self.freezeball_active_player = current_player
            state.consume_bonus_turn(current_player)
            self.events[-1] += " → BONUS PHASE"
            self.phase = f"player_{current_player}_bonus"
        elif is_bonus:
            if current_player == 1:
                self.phase = "player_2_act"
            else:
                self.phase = "idle"
            if state.player2_frozen == 0 if current_player == 1 else state.player1_frozen == 0:
                self.freezeball_active_player = None
            self.events[-1] += f" → to opponent"
        elif current_player == 1:
            opponent_frozen = state.player2_frozen
            if self.freezeball_active_player == 1 and opponent_frozen > 0:
                self.phase = "player_2_act"
                self.events[-1] += " (prevented - opponent frozen)"
            else:
                self.phase = "player_2_act"
                if opponent_frozen == 0:
                    self.freezeball_active_player = None
        else:
            self.phase = "idle"
            if state.player1_frozen == 0:
                self.freezeball_active_player = None

tracer = GameTracer()

print("\n--- Running 20 phases ---")
for i in range(20):
    tracer.update()

print("\n" + "=" * 70)
print("EVENT LOG")
print("=" * 70)
for event in tracer.events:
    print(event)

print("\n" + "=" * 70)
print("BONUS DETECTION SUMMARY")
print("=" * 70)
freeze_events = [e for e in tracer.events if "FREEZE" in e]
bonus_events = [e for e in tracer.events if "BONUS" in e]

print(f"\nFREEZE actions: {len(freeze_events)}")
for e in freeze_events:
    print(f"  {e}")

print(f"\nBONUS actions: {len(bonus_events)}")
for e in bonus_events:
    print(f"  {e}")

if len(bonus_events) >= 2:
    print(f"\n✓ Both freeze actions triggered BONUS phases")
else:
    print(f"\n❌ Missing bonus phases! Only {len(bonus_events)} bonus actions detected")
