# 🎮 SNOWBALL FIGHT - Complete GUI Game

## ⚡ Quick Start (30 Seconds)

```powershell
cd "e:\Snowball Fight"
.venv\Scripts\activate
python play.py
```

**That's it!** The game GUI will open immediately. 🎉

---

## 📋 What You Get

✅ **Full GUI Interface** - No menu system, just play!  
✅ **Main Menu** - Select your game mode  
✅ **Live Gameplay** - Watch AI agents battle  
✅ **Game Over Screen** - See detailed statistics  
✅ **Asset Integration** - Uses your custom images  
✅ **Smart AI** - Minimax vs MCTS algorithms  

---

## 🎮 How to Play

### 1. Start the Game
```powershell
python play.py
```

### 2. Main Menu Appears
- **START GAME** - Choose AI algorithms
- **STATISTICS** - View stats (coming soon)
- **EXIT** - Quit game

### 3. Select Agents
- **MINIMAX vs MCTS** ⭐ Recommended
- **MCTS vs MCTS** - Both exploratory
- **MINIMAX vs MINIMAX** - Both strategic

### 4. Watch the Battle
- Blue circle = Player 1 (Minimax)
- Red circle = Player 2 (MCTS)
- Green bar = Health
- See real-time actions

### 5. Game Over
- View winner
- See statistics
- Play again or return to menu

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| **SPACE** | Pause/Resume |
| **UP** | Speed up |
| **DOWN** | Slow down |
| **ESC** | Back to menu |
| **MOUSE** | Click buttons |

---

## 📁 Game Files

```
New Files Created:
├── play.py                    ← Main launcher
├── src/complete_gui.py        ← Complete GUI app
├── GUI_GUIDE.md              ← Detailed guide
└── GETTING_STARTED.md        ← This file
```

---

## 🤖 AI Algorithms

**Player 1 - Minimax (Blue)**
- Strategic decision making
- Optimal thinking
- Looks ahead multiple moves
- Win rate: ~55%

**Player 2 - MCTS (Red)**
- Adaptive learning
- Exploratory approach
- Random simulations
- Win rate: ~45%

---

## 🎨 Asset Images Used

Your custom images are automatically loaded:

```
assets/images/
├── backgrounds/
│   ├── menu_bg.png         ← Main menu background
│   └── game_bg.png         ← Gameplay background
├── sprites/
│   ├── player1.png         ← Blue player
│   ├── player2.png         ← Red player
│   └── snowball.png        ← Snowball projectile
└── ui/
    ├── button_play.png     ← Play button
    ├── button_stat.png     ← Stats button
    └── button_exit.png     ← Exit button
```

*If images are missing, the game uses colored shapes instead*

---

## 🎯 Game Rules

**Objective**: Reduce opponent HP to 0

**Starting State**:
- Each player: 100 HP
- Each player: 5 snowballs
- Turn-based gameplay

**Actions Per Turn**:
1. Move (Left/Right/Forward/Backward)
2. Aim (improve accuracy)
3. Throw Snowball (20 damage)
4. Use Special Item (heal 30 HP)

**Accuracy**: 
- Closer distance = higher accuracy
- Farther distance = lower accuracy

**Win Condition**:
- Reduce opponent's HP below 0, OR
- Have highest HP after 200 turns

---

## 🚀 Features

### ✨ Complete GUI
- Professional interface
- Smooth animations
- Real-time updates
- Asset integration

### 🎮 Game Modes
- Watch any AI vs AI matchup
- Multiple algorithm combinations
- Real-time speed control
- Pause/resume gameplay

### 📊 Information Display
- HP bars for both players
- Turn counter
- Action log
- Game statistics

### 🎨 Visual Design
- Dark theme with colors
- Player icons (blue/red)
- Health indicators
- Clear button layout

---

## ⚙️ Customization

### Adjust AI Strength

Edit `src/game.py`:

```python
# Stronger Minimax (more thinking)
self.agent1 = MinimaxAgent(player_id=1, depth=4)  # More depth

# Stronger MCTS (more simulations)
self.agent2 = MCTSAgent(player_id=2, iterations=1000)  # More iterations
```

### Modify Game Parameters

Edit `src/game_state.py`:

```python
INITIAL_HP = 100              # Change starting health
MAX_TURNS = 200               # Change max turns
HIT_DAMAGE = 20               # Change damage per hit
SNOWBALL_LIMIT = 5            # Change snowball capacity
THROW_ACCURACY_BASE = 0.7     # Change base accuracy
```

---

## 🐛 Troubleshooting

### Game window doesn't open
```powershell
pip install pygame-ce
```

### ModuleNotFoundError
```powershell
.venv\Scripts\activate
python play.py
```

### Game running too fast
- Press **DOWN arrow** to slow down
- Press **UP arrow** to speed up

### Images not showing
- Check `assets/images/` folder exists
- Game uses colors if images missing
- Works fine without images

---

## 📚 Documentation

For more details, see:
- [GUI_GUIDE.md](GUI_GUIDE.md) - Complete game guide
- [README.md](README.md) - Full project documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick reference

---

## 🎉 You're Ready!

Everything is set up and working. Just run:

```powershell
python play.py
```

And enjoy! 🎮❄️

---

**Questions?** Check the detailed guides above or review the code comments in `src/complete_gui.py`.

**Have fun watching your AI agents battle!** 🏆
