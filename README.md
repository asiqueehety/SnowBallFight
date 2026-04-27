# Snowball Fight: AI vs AI Game Simulation

A Python-based AI vs AI competitive game inspired by the classic Java-based button phone game "Snowball Fight". Two autonomous AI agents battle each other using different decision-making algorithms.

## Project Overview

This project implements a two-player AI vs AI snowball fighting game where:
- **Player 1** uses the **Minimax algorithm** with Alpha-Beta pruning for optimal decision-making
- **Player 2** uses the **Monte Carlo Tree Search (MCTS)** algorithm for exploration-based decision-making

### Game Features

- **2D Turn-based Gameplay**: Players alternate turns on a fixed 2D field
- **Actions Available**:
  - Move Left/Right/Forward/Backward
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

### Method 1: Using the Menu System (Recommended)
```bash
python main.py
```

This opens an interactive menu where you can:
1. Play GUI Game (Minimax vs MCTS with visual display)
2. Play Console Game (Text-based output)
3. Run Multiple Matches & Statistics
4. Custom Match (Choose your own agent combinations)
5. Exit

### Method 2: Direct Console Game
```bash
cd src
python game.py
```

### Method 3: Direct GUI Game
```bash
cd src
python gui.py
```

## Game Controls (GUI Mode)

| Key | Action |
|-----|--------|
| SPACE | Pause/Resume |
| UP | Increase game speed |
| DOWN | Decrease game speed |
| Q | Quit game |

## Algorithm Implementations

### Minimax Algorithm (Player 1)

**Characteristics:**
- Explores the game tree to a fixed depth
- Uses Alpha-Beta pruning to eliminate unnecessary branches
- Evaluates positions based on heuristics
- Optimal decision-making for zero-sum games

**Heuristic Evaluation:**
- Health advantage (our HP - opponent HP) × 10
- Proximity bonus (closer to opponent) × 5
- Resource advantage (snowballs) × 3
- Position advantage (center control) × 2

**Configuration:**
- Search depth: 2-3 (adjustable)
- Time complexity: O(b^d) where b=branching factor, d=depth

### Monte Carlo Tree Search (Player 2)

**Characteristics:**
- Uses random simulations (playout) to evaluate positions
- Balances exploration and exploitation with UCB1 formula
- Does not require explicit game tree evaluation
- Adaptive to complex game states

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
- Exploration constant: 1.41 (sqrt(2))

## Game Statistics

Sample match statistics (Minimax vs MCTS):
- **Average turns per game**: 15-30
- **Win rate (Minimax)**: ~55-60%
- **Win rate (MCTS)**: ~40-45%
- **Average game duration**: 2-5 seconds

## Customization

### Adjusting AI Difficulty

Edit `src/game.py` or `src/gui.py`:

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
MAX_TURNS = 200           # Maximum turns before draw
HIT_DAMAGE = 20           # Damage per successful hit
```

## Key Features

✅ **Two Different AI Algorithms**: Compare Minimax vs MCTS strategies
✅ **Visual GUI**: Watch agents battle in real-time with pygame
✅ **Detailed Logging**: Console output shows all actions and decisions
✅ **Batch Testing**: Run multiple matches and collect statistics
✅ **Configurable**: Adjust AI difficulty and game parameters
✅ **Educational**: Great for learning about game AI algorithms

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
SNOWBALL FIGHT: MINIMAX vs MCTS
============================================================

Turn 1 - Player 1's Action
====================================================
P1: pos=[0, 2], HP=100, snowballs=5
P2: pos=[9, 2], HP=100, snowballs=5

Action taken: MOVE_RIGHT (Time: 0.234s)
Result: Player 1 moved right

[Minimax-P1] Nodes explored: 1847, Best score: 45.5, Action: MOVE_RIGHT

...

GAME OVER!
WINNER: Player 1 (MINIMAX)
Total turns: 18
Total game time: 4.523 seconds
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
