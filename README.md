# Snowball Fight: AI vs AI Game Simulation

A Python-based AI vs AI competitive game inspired by the classic Java-based button phone game "Snowball Fight". Two autonomous AI agents battle each other **simultaneously** using different decision-making algorithms.

## Project Overview

This project implements a two-player AI vs AI snowball fighting game where:
- **Player 1** uses the **Minimax algorithm** with Alpha-Beta pruning for optimal decision-making
- **Player 2** uses the **Monte Carlo Tree Search (MCTS)** algorithm for exploration-based decision-making
- **Both agents act simultaneously** without turn alternation
- **Attack cooldown system**: 2-step cooldown (≈2 seconds) between consecutive attacks
- **Free movement**: Agents can move at any time without cooldown

### Game Features

- **Simultaneous Gameplay**: Both players act at the same time, not alternating turns
- **Attack Cooldown**: 2-step cooldown between attacks (prevents spam)
- **Free Movement**: Move anytime without cooldown restriction
- **Actions Available**:
  - Move Left/Right (horizontal positioning)
  - Move Forward/Backward (1 block max, vertical movement)
  - Aim for better accuracy
  - Throw Snowball
  - Use Special Items (MedKit for healing, Freezeball for effects)
  
- **Game State Tracking**:
  - Player positions on the field
  - Health Points (HP) for each player
  - Snowball availability
  - Distance between players
  - Special items inventory

- **Winning Conditions**:
  - Deplete opponent's HP to 0
  - Have higher HP when max turns reached

## Project Structure

```
Snowball Fight/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── game_state.py        # Game state and logic
│   ├── minimax_agent.py     # Minimax AI implementation
│   ├── mcts_agent.py        # MCTS AI implementation
│   ├── game.py              # Main game orchestration
│   └── gui.py               # Pygame GUI
├── main.py                  # Entry point with menu system
├── .venv/                   # Python virtual environment
└── README.md               # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher

### Step 1: Clone/Navigate to Project
```bash
cd "e:\Snowball Fight"
```

### Step 2: Activate Virtual Environment
```bash
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies
If not already installed:
```bash
pip install pygame numpy
```

## Running the Game

### Visual GUI Game (Default)
```bash
python play.py
```

This starts the **visual game** with animated sprites, real-time action display, and simultaneous gameplay where both agents act at the same time. Use SPACE to pause, UP/DOWN to adjust speed, Q to quit.

### Console Output (Text-Based Alternative)
```bash
cd src
python game.py
```

This runs a text-based version showing all actions and cooldowns in console.

### Using the Menu System
```bash
python main.py
```

This opens an interactive menu where you can choose different game modes and configurations.

## Simultaneous Gameplay System

### How It Works

Instead of alternating turns, both agents **decide and execute actions at the same time**:

```
Step 1:
  P1 decides → THROW_SNOWBALL
  P2 decides → MOVE_LEFT
  
  Both actions execute simultaneously!
  P1 attacks while P2 moves to dodge

Step 2:
  P1 cannot attack (2-step cooldown active = 1 step remaining)
  P2 can attack
  
  P1 defaults to AIM (waiting for cooldown)
  P2 can throw snowball

Step 3:
  P1 cooldown expired → can attack again
  P2 on cooldown
```

### Attack Cooldown

- **Duration**: 2 steps (approximately 2 seconds)
- **Triggered by**: THROW_SNOWBALL or USE_FREEZEBALL actions
- **Effect**: Prevents attacking until cooldown expires
- **During cooldown**: Agent defaults to AIM action or movement

### Movement

- **No cooldown**: Agents can move every step
- **Directions**: LEFT, RIGHT, FORWARD (toward opponent), BACKWARD (away)
- **Limits**: Maximum 1 block per direction
- **Purpose**: Dodge incoming attacks or position for better aim

## Game Controls (Console)

The console displays all agents' actions with timestamps and cooldown status.

## Algorithm Implementations

Both algorithms work identically in the simultaneous gameplay system, with the addition of attack cooldown constraints.

### Minimax Algorithm (Player 1)

**Characteristics:**
- Explores the game tree to a fixed depth
- Uses Alpha-Beta pruning to eliminate unnecessary branches
- Evaluates positions based on heuristics
- Optimal decision-making for zero-sum games
- **In simultaneous mode**: Respects 2-step attack cooldown

**Heuristic Evaluation:**
- Health advantage (our HP - opponent HP) × 10
- Proximity bonus (closer to opponent) × 5
- Resource advantage (snowballs) × 3
- Position advantage (center control) × 2

**Configuration:**
- Search depth: 2-3 (adjustable)
- Attack cooldown: 2 steps between attacks

### Monte Carlo Tree Search (Player 2)

**Characteristics:**
- Uses random simulations (playout) to evaluate positions
- Balances exploration and exploitation with UCB1 formula
- Does not require explicit game tree evaluation
- Adaptive to complex game states
- **In simultaneous mode**: Respects 2-step attack cooldown

**Algorithm Phases:**
1. **Selection**: Use UCB1 to select most promising path
2. **Expansion**: Add unvisited node to tree
3. **Simulation**: Random playout from expanded node
4. **Backpropagation**: Update statistics of visited nodes

**UCB1 Formula:**
```
UCB1 = Exploitation + Exploration
     = (Win/Visits) + C × sqrt(ln(Parent Visits) / Visits)
```

**Configuration:**
- Simulations per turn: 300-500 (adjustable)
- Attack cooldown: 2 steps between attacks

## Game Statistics

Sample match statistics (Minimax vs MCTS with simultaneous gameplay):
- **Average steps per game**: 100-200 (more steps due to simultaneous execution)
- **Average game duration**: 2-5 seconds
- **Win rate (Minimax)**: ~50-60% (depending on AI parameters)
- **Win rate (MCTS)**: ~40-50% (depending on AI parameters)

**Note:** Games have more steps than turn-based versions because agents act simultaneously and must respect attack cooldowns, resulting in strategic waiting periods where they move or aim instead of attacking.

## Customization

### Adjusting Attack Cooldown

Edit `src/game_state.py` and search for where cooldowns are set (around lines 189, 217):
```python
# Change this value to adjust cooldown duration (in steps)
self.player1_attack_cooldown = 2  # 2 steps = ~2 seconds
self.player2_attack_cooldown = 2
```

- `2` = Normal cooldown (~2 seconds between attacks)
- `1` = Faster attacks (less waiting)
- `3` = Slower attacks (more strategic)

### Adjusting AI Difficulty

Edit `src/game.py` or `src/game_state.py`:

```python
# For Minimax
self.agent1 = MinimaxAgent(player_id=1, depth=3)  # Increase depth for stronger AI

# For MCTS
self.agent2 = MCTSAgent(player_id=2, iterations=500)  # Increase iterations for stronger AI
```

### Modifying Game Parameters

Edit `src/game_state.py`:

```python
FIELD_WIDTH = 10          # Game field width
FIELD_HEIGHT = 5          # Game field height
INITIAL_HP = 100          # Starting health points
MAX_TURNS = 200           # Maximum steps before draw
HIT_DAMAGE = 20           # Damage per successful hit
```

## Key Features

✅ **Simultaneous Gameplay**: Both agents act at the same time without turn alternation
✅ **Attack Cooldown System**: 2-step cooldown between attacks prevents spam
✅ **Free Movement**: Move at any time without cooldown restrictions
✅ **Two Different AI Algorithms**: Compare Minimax vs MCTS strategies
✅ **Detailed Logging**: Console output shows all actions with timestamps and cooldowns
✅ **Configurable**: Adjust AI difficulty, cooldown duration, and game parameters
✅ **Educational**: Great for learning about game AI algorithms and simultaneous game design

## Performance Metrics

The project tracks:
- Decision-making time per turn
- Nodes explored during search
- Win/loss statistics
- Game duration and turn counts
- HP progression over time

## Example Output

```
============================================================
# MINIMAX vs MCTS
# Both agents act simultaneously
============================================================

STEP 1 (Turn 0)
Turn 0 (Step 1)
P1: pos=[5, 4], HP=100, snowballs=5, items={'freezeball': 1, 'medkit': 1}, frozen=0
P2: pos=[5, 0], HP=100, snowballs=5, items={'freezeball': 1, 'medkit': 1}, frozen=0

--- Both agents act simultaneously ---
[Minimax-P1] THROW_SNOWBALL
[MCTS-P2]    MOVE_LEFT

P1: THROW_SNOWBALL -> P1 aimed STRAIGHT, threw 4.0! P2 HIT! -20 HP
P2: MOVE_LEFT     -> Player 2 shifted LEFT
HP: P1=100 | P2=80
Attack Cooldowns: P1=2 | P2=0

============================================================
STEP 2 (Turn 1)
--- Both agents act simultaneously ---
[Minimax-P1] AIM (on cooldown)
[MCTS-P2]    THROW_SNOWBALL

P1: AIM            -> Player 1 aimed/waited
P2: THROW_SNOWBALL -> P2 aimed STRAIGHT, threw 4.0! P1 dodged!
HP: P1=100 | P2=80
Attack Cooldowns: P1=1 | P2=2

...

GAME OVER!
WINNER: Player 1 (MINIMAX)
Total steps: 145
Final HP: P1=85, P2=0
```

## Troubleshooting

### "pygame not found" error
```bash
pip install pygame
```

### "ModuleNotFoundError" in game
Make sure you're running from the correct directory and the virtual environment is activated.

### GUI not displaying
- Ensure pygame is installed: `pip install pygame`
- Check your display settings
- Try the console version first

### Game running too fast/slow
Use UP/DOWN arrow keys to adjust speed in GUI mode, or modify `game_speed` variable in `gui.py`.

## Future Enhancements

Potential improvements:
- [ ] Add reinforcement learning agent
- [ ] Implement Q-Learning AI
- [ ] Add neural network-based agent
- [ ] Tournament mode (multiple agents)
- [ ] Advanced statistics and graphs
- [ ] Sound effects and animations
- [ ] Network multiplayer (human vs AI)
- [ ] Different difficulty levels

## References

**Minimax Algorithm:**
- Russell & Norvig, "Artificial Intelligence: A Modern Approach"
- Alpha-Beta Pruning optimization

**Monte Carlo Tree Search:**
- Browne et al., "A Survey of Monte Carlo Tree Search Methods"
- UCB1 bandit algorithm

## Author

Developed as an AI Laboratory project focusing on game-playing algorithms and agent-based simulation.

## License

MIT License - Feel free to use and modify for educational purposes.

## Support

For issues or questions, review:
1. The console output for detailed game logs
2. The algorithm implementations in minimax_agent.py and mcts_agent.py
3. Game parameters in game_state.py

---

**Enjoy watching your AI agents battle! 🎮**
