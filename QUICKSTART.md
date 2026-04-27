# Quick Start Guide: Snowball Fight AI vs AI

## 30-Second Setup

1. **Open PowerShell in the project folder** (right-click → Open PowerShell here)

2. **Activate the environment:**
   ```powershell
   .venv\Scripts\activate
   ```

3. **Run the game:**
   ```powershell
   python main.py
   ```

4. **Choose an option from the menu:**
   - Press `1` for GUI game (visual with pygame)
   - Press `2` for console game (text-based)
   - Press `3` for statistics (multiple matches)

## Fastest Test Run

Just want to see it work quickly? Run this:

```powershell
cd src
python game.py
```

You'll see a text-based game play out in the console with full move-by-move action.

## GUI Game Controls

When playing the visual version:
- **SPACE** = Pause/Resume
- **UP/DOWN** = Speed control
- **Q** = Quit

## File Structure

```
e:\Snowball Fight\
├── main.py                  ← Start here!
├── src/
│   ├── game_state.py       ← Game rules and logic
│   ├── minimax_agent.py    ← Smart AI #1
│   ├── mcts_agent.py       ← Smart AI #2
│   ├── game.py             ← Game coordinator
│   └── gui.py              ← Visual display
├── README.md               ← Full documentation
└── .venv/                  ← Python environment
```

## Understanding the Agents

### Minimax (Player 1 - Blue)
- **Strategy**: Looks ahead and picks the best move
- **Speed**: Fast
- **Style**: Conservative, optimal thinking

### MCTS (Player 2 - Red)
- **Strategy**: Tries many random scenarios and learns
- **Speed**: Medium
- **Style**: Adaptive, exploratory

## Running Different Matchups

Edit `main.py` or use the menu to try:
- Minimax vs Minimax (both using strategy)
- MCTS vs MCTS (both using exploration)
- Minimax vs MCTS (default)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Virtual environment not activating | Try: `.venv\Scripts\Activate.ps1` |
| pygame not found | Run: `pip install pygame` |
| Game too slow | Press UP arrow key in GUI mode |
| GUI doesn't appear | Try console mode first with `python game.py` |

## Example Commands

```powershell
# Test single game
cd src
python game.py

# Run GUI
cd ..
python main.py
# Then select option 1

# Run 10 matches and get stats
python main.py
# Then select option 3
# Then enter: 10

# Quick test with different agents
cd src
python -c "from game import SnowballGame; g = SnowballGame('mcts', 'mcts'); g.play_full_game()"
```

## Next Steps

1. ✅ **Run the game** - See AI agents battle
2. 📊 **Run statistics** - See win rates (menu option 3)
3. 🎨 **Try GUI** - Watch visual gameplay (menu option 1)
4. ⚙️ **Adjust parameters** - Edit difficulty in `src/game_state.py`
5. 📚 **Study algorithms** - Read code in `minimax_agent.py` and `mcts_agent.py`

## Sample Output

```
Turn 1 - Player 1's Action
====================================================
P1: pos=[0, 2], HP=100, snowballs=5
P2: pos=[9, 2], HP=100, snowballs=5

Action taken: MOVE_RIGHT (Time: 0.234s)
Result: Player 1 moved right

[Minimax-P1] Nodes explored: 1847, Best score: 45.5

...

GAME OVER!
WINNER: Player 1 (MINIMAX)
Total turns: 80
Total game time: 1.767 seconds
```

## Ready? Let's Go! 🎮

```powershell
cd "e:\Snowball Fight"
.venv\Scripts\activate
python main.py
```

Enjoy the AI battle! ❄️⛄
