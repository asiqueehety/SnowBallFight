"""Test GUI phase transitions for bonus turns with actual update logic."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType

state = GameState()

class GUISimulator:
    def __init__(self):
        self.anim_phase = "idle"
        self.freezeball_active_player = None
        self.action_count = 0
        self.events = []
        
    def step(self):
        """Simulate one update step."""
        self.action_count += 1
        
        if self.anim_phase == "idle":
            state.advance_turn()
            self.anim_phase = "player_1_act"
            self.events.append(f"Step {self.action_count}: IDLE→P1_ACT")
            return
        
        parts = self.anim_phase.split("_")
        if len(parts) < 2:
            self.anim_phase = "idle"
            return
        
        try:
            current_player = int(parts[1])
        except:
            self.anim_phase = "idle"
            return
        
        is_bonus = len(parts) > 2 and parts[2] == "bonus"
        
        # Frozen check
        frozen = state.player1_frozen if current_player == 1 else state.player2_frozen
        if frozen > 0 and not is_bonus:
            self.events.append(f"Step {self.action_count}: P{current_player} FROZEN SKIP")
            state.tick_frozen(current_player)
            if current_player == 1:
                self.anim_phase = "player_2_act"
            else:
                self.anim_phase = "idle"
            return
        
        # Freezeball prevention check
        opponent_frozen = state.player2_frozen if current_player == 1 else state.player1_frozen
        if self.freezeball_active_player == current_player and opponent_frozen > 0 and not is_bonus:
            self.events.append(f"Step {self.action_count}: P{current_player} PREVENTED (freeze + opponent_frozen={opponent_frozen})")
            if current_player == 1:
                self.anim_phase = "player_2_act"
            else:
                self.anim_phase = "idle"
            return
        
        # Determine action
        if is_bonus:
            action = ActionType.THROW_SNOWBALL
            action_name = "BONUS"
        elif len([e for e in self.events if "FREEZE" in e]) < 2:
            action = ActionType.USE_FREEZEBALL
            action_name = "FREEZE"
        else:
            action = ActionType.THROW_SNOWBALL
            action_name = "NORMAL"
        
        # Execute
        result = state.apply_action(current_player, action)
        bonus_granted = result.get('bonus_turn_granted', False)
        
        self.events.append(f"Step {self.action_count}: P{current_player} {action_name}{' [bonus_granted]' if bonus_granted else ''}")
        
        # Phase transition logic (from gui_fixed.py)
        bonus_granted_check = result.get('bonus_turn_granted') and state.pending_bonus_turn == current_player
        
        if bonus_granted_check and not is_bonus:
            self.events[-1] += " → ENTER_BONUS_PHASE"
            state.consume_bonus_turn(current_player)
            self.anim_phase = f"player_{current_player}_bonus"
        elif is_bonus:
            self.events[-1] += " → EXIT_BONUS"
            if current_player == 1:
                self.anim_phase = "player_2_act"
                if state.player2_frozen == 0:
                    self.freezeball_active_player = None
            else:
                self.anim_phase = "player_1_act"
                if state.player1_frozen == 0:
                    self.freezeball_active_player = None
        elif current_player == 1:
            if self.freezeball_active_player == 1 and opponent_frozen > 0:
                self.anim_phase = "player_2_act"
                self.events[-1] += " → P2_ACT (due to freeze prevention)"
            else:
                self.anim_phase = "player_2_act"
                if opponent_frozen == 0:
                    self.freezeball_active_player = None
                self.events[-1] += " → P2_ACT"
        else:
            self.anim_phase = "idle"
            if state.player1_frozen == 0:
                self.freezeball_active_player = None
            self.events[-1] += " → IDLE"
        
        # Track freezeball use
        if bonus_granted:
            self.freezeball_active_player = current_player

# Run simulation
gui = GUISimulator()

print("=" * 70)
print("BONUS TURN GUI SIMULATION")
print("=" * 70)
print()

for i in range(25):
    gui.step()

print("\nEvent Sequence:")
for event in gui.events:
    print(f"  {event}")

print("\n" + "=" * 70)
print("ANALYSIS")
print("=" * 70)

freeze_count = len([e for e in gui.events if "FREEZE" in e])
bonus_count = len([e for e in gui.events if "BONUS" in e])
enter_bonus = len([e for e in gui.events if "ENTER_BONUS" in e])

print(f"\nFREEZE actions: {freeze_count}")
print(f"BONUS actions: {bonus_count}")
print(f"BONUS phases entered: {enter_bonus}")

if enter_bonus >= 2:
    print("\n✓ Both players entered bonus phases")
elif enter_bonus == 1:
    print("\n⚠️ Only ONE player entered bonus phase")
else:
    print("\n❌ NO bonus phases were entered!")

if bonus_count >= 2:
    print("✓ Both players executed bonus actions")
else:
    print(f"❌ Only {bonus_count} bonus actions executed")