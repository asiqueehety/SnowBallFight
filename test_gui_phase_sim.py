"""Test GUI phase transitions with freezeball to catch inconsistency."""
import sys
sys.path.insert(0, 'src')

from game_state import GameState, ActionType
import time

state = GameState()

print("=" * 70)
print("GUI PHASE SIMULATION - NORMAL MOVE CONSISTENCY")
print("=" * 70)

# Simulate the GUI's phase logic manually (simplified)
class SimpleGUI:
    def __init__(self):
        self.anim_phase = "idle"
        self.freezeball_active_player = None
        self.action_sequence = []
        
    def update(self):
        """Simulate one frame update of the GUI logic."""
        
        # Handle idle phase
        if self.anim_phase == "idle":
            state.advance_turn()
            self.anim_phase = "player_1_act"
            return
        
        # Parse current phase
        parts = self.anim_phase.split("_")
        if len(parts) < 2:
            return
            
        current_player = int(parts[1]) if parts[1].isdigit() else None
        if current_player is None:
            return
        
        is_bonus = len(parts) > 2 and parts[2] == "bonus"
        
        # Check if frozen
        frozen = state.player1_frozen if current_player == 1 else state.player2_frozen
        if frozen > 0 and not is_bonus:
            # Frozen skip
            self.action_sequence.append(f"P{current_player} FROZEN SKIP (counter={frozen})")
            state.tick_frozen(current_player)
            if current_player == 1:
                self.anim_phase = "player_2_act"
            else:
                self.anim_phase = "idle"
            return
        
        # Check for freezeball prevention (NEW LOGIC)
        opponent_frozen = state.player2_frozen if current_player == 1 else state.player1_frozen
        if self.freezeball_active_player == current_player and opponent_frozen > 0 and not is_bonus:
            # This player used freezeball and opponent still frozen - prevent normal action
            self.action_sequence.append(f"P{current_player} HELD (freezeball active, opponent frozen={opponent_frozen})")
            if current_player == 1:
                self.anim_phase = "player_2_act"
            else:
                self.anim_phase = "idle"
            return
        
        # Execute action
        if is_bonus:
            action = ActionType.THROW_SNOWBALL
            self.action_sequence.append(f"P{current_player} BONUS action")
        else:
            # Alternate between freeze and normal
            if current_player == 1 and len(self.action_sequence) == 0:
                action = ActionType.USE_FREEZEBALL
                self.freezeball_active_player = 1
                self.action_sequence.append(f"P{current_player} FREEZE")
            elif current_player == 2 and len([a for a in self.action_sequence if 'FREEZE' in a and 'P2' in a]) == 0:
                action = ActionType.USE_FREEZEBALL
                self.freezeball_active_player = 2
                self.action_sequence.append(f"P{current_player} FREEZE")
            else:
                action = ActionType.THROW_SNOWBALL
                self.action_sequence.append(f"P{current_player} NORMAL action")
        
        result = state.apply_action(current_player, action)
        
        # Handle bonus turn grant
        bonus_granted = result.get('bonus_turn_granted', False)
        if bonus_granted and not is_bonus:
            state.consume_bonus_turn(current_player)
            self.anim_phase = f"player_{current_player}_bonus"
            return
        
        # Phase transition (this is where my fix applies)
        if is_bonus:
            if current_player == 1:
                self.anim_phase = "player_2_act"
                if state.player2_frozen == 0:
                    self.freezeball_active_player = None
            else:
                self.anim_phase = "player_1_act"
                if state.player1_frozen == 0:
                    self.freezeball_active_player = None
        elif current_player == 1:
            p2_frozen = state.player2_frozen
            if self.freezeball_active_player == 1 and p2_frozen > 0:
                self.anim_phase = "idle"  # PREVENT extra P1 action
            else:
                self.anim_phase = "player_2_act"
                if p2_frozen == 0:
                    self.freezeball_active_player = None
        else:  # P2 done
            p1_frozen = state.player1_frozen
            if self.freezeball_active_player == 2 and p1_frozen > 0:
                self.anim_phase = "idle"  # PREVENT extra P2 action
            else:
                self.anim_phase = "idle"
                if p1_frozen == 0:
                    self.freezeball_active_player = None

# Run simulation
gui = SimpleGUI()

print("\n--- Simulating 15 phase updates ---")
for update in range(15):
    print(f"\nUpdate {update}: Phase='{gui.anim_phase}'")
    gui.update()
    print(f"  → Actions so far: {gui.action_sequence[-1] if gui.action_sequence else 'none'}")
    print(f"  → Next phase: '{gui.anim_phase}'")
    print(f"  → P1 frozen={state.player1_frozen}, P2 frozen={state.player2_frozen}")
    
    if update >= 12:  # Stop after first few action cycles
        break

print("\n" + "=" * 70)
print("ACTION SEQUENCE")
print("=" * 70)
for i, action in enumerate(gui.action_sequence):
    print(f"{i+1}. {action}")

# Count P1 and P2 actions in freeze window
p1_count = len([a for a in gui.action_sequence if 'P1' in a and update < 8])
p2_count = len([a for a in gui.action_sequence if 'P2' in a and update < 8])

print("\n" + "=" * 70)
print("CONSISTENCY CHECK")
print("=" * 70)
print(f"P1 actions: {p1_count}")
print(f"P2 actions: {p2_count}")

# Check for the bug: P1 getting extra action after bonus while P2 frozen
p1_actions_after_freeze = []
found_p1_freeze = False
for action in gui.action_sequence:
    if 'P1 FREEZE' in action:
        found_p1_freeze = True
    elif found_p1_freeze and 'P1' in action and 'NORMAL' in action:
        p1_actions_after_freeze.append(action)

if p1_actions_after_freeze:
    print(f"\n⚠️ P1 NORMAL actions after freeze: {len(p1_actions_after_freeze)}")
    for action in p1_actions_after_freeze:
        print(f"   - {action}")
    if len(p1_actions_after_freeze) > 1:
        print("\n❌ INCONSISTENCY: P1 got extra actions while P2 frozen!")
    else:
        print("\n✓ P1 got 1 normal action (might be allowed)")
else:
    print("\n✓ NO P1 NORMAL actions after freeze - CONSISTENT!")
