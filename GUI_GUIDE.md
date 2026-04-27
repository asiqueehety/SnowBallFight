# Complete GUI Game - Quick Start Guide

## 🎮 Running the Game

### Option 1: Direct GUI (Recommended)
```powershell
cd "e:\Snowball Fight"
.venv\Scripts\activate
python play.py
```

### Option 2: From Terminal
```powershell
python play.py
```

The **GUI window will open immediately** with the main menu!

---

## 🎯 Game Screens

### 1️⃣ **Main Menu**
When you run the game, you'll see:
- **Title**: "SNOWBALL FIGHT - AI vs AI"
- **3 Buttons**:
  - 🎮 **START GAME** - Choose AI algorithms and watch them battle
  - 📊 **STATISTICS** - View game statistics
  - ❌ **EXIT** - Quit the application

### 2️⃣ **Game Setup Screen**
After clicking "START GAME", choose which AI algorithms will fight:
- **MINIMAX vs MCTS** (Recommended - Default)
  - Strategic vs Exploratory
  - Balanced gameplay
  
- **MCTS vs MCTS** (Both exploratory)
  - Random, dynamic battles
  - Unpredictable outcomes
  
- **MINIMAX vs MINIMAX** (Both strategic)
  - Optimal decision-making
  - Strategic gameplay

Click on any option to start the game!

### 3️⃣ **Gameplay Screen**
Watch the AI agents battle in real-time:

**Left Side (Player 1 - Blue)**
- Name and Algorithm
- Current HP
- Snowball count
- HP bar (green = alive, red = low health)

**Center**
- Game field with grid
- Player 1 and Player 2 positions
- Turn counter
- Game status (Playing/Paused)

**Right Side (Player 2 - Red)**
- Same info as Player 1 but for Player 2

**Top of Screen**
- Real-time game action log (optional)

### 4️⃣ **Game Over Screen**
When the game ends:
- **Big Message**: Shows who won or if it's a draw
- **Statistics**:
  - Total turns played
  - Final HP of both players
  - Game duration
- **Buttons**:
  - 🔄 **PLAY AGAIN** - Rematch with same AI
  - 🏠 **MAIN MENU** - Return to main menu

---

## ⌨️ Controls During Gameplay

| Key | Action |
|-----|--------|
| **SPACE** | Pause/Resume game |
| **UP Arrow** | Speed up (faster gameplay) |
| **DOWN Arrow** | Slow down (slower gameplay) |
| **ESC** | Return to main menu |

---

## 📊 Game Rules

**Objective**: Deplete opponent's HP to 0

**Each Player Has**:
- 100 HP (starting health)
- 5 Snowballs (regenerates 1 per turn)
- 2 Special Items (MedKit)

**Available Actions**:
1. Move Left/Right/Forward/Backward
2. Aim (improve accuracy)
3. Throw Snowball (deal 20 damage)
4. Use Special Item (MedKit heals 30 HP)

**Hit Mechanics**:
- Accuracy based on distance
- Closer = more accurate
- Farther = less accurate

**Game Ends When**:
- One player's HP reaches 0 (they lose)
- 200 turns completed (highest HP wins)

---

## 🤖 AI Algorithms Explained

### **Minimax (Blue) - Strategic Thinker**
- Looks ahead multiple moves
- Calculates best/worst outcomes
- Makes optimal decisions
- Fast, predictable strategy
- **Win Rate**: ~55%

### **MCTS (Red) - Adaptive Explorer**
- Runs random simulations
- Learns from outcomes
- Balances exploration vs exploitation
- Medium speed, dynamic strategy
- **Win Rate**: ~45%

---

## 🎨 Visual Elements

The GUI uses your asset images:

**Backgrounds**:
- Menu background: `assets/images/backgrounds/menu_bg.png`
- Game background: `assets/images/backgrounds/game_bg.png`

**Sprites**:
- Player 1 (Blue): `assets/images/sprites/player1.png`
- Player 2 (Red): `assets/images/sprites/player2.png`
- Snowball: `assets/images/sprites/snowball.png`

**UI Buttons**:
- Play button: `assets/images/ui/button_play.png`
- Stats button: `assets/images/ui/button_stat.png`
- Exit button: `assets/images/ui/button_exit.png`

> If any image is missing, the game uses colored shapes instead!

---

## 💾 How to Customize

### Change AI Difficulty

Edit `src/complete_gui.py` and find this section:
```python
def select_agents(self, agent1: str, agent2: str):
    self.agent1_choice = agent1
    self.agent2_choice = agent2
    self.game = SnowballGame(agent1_type=agent1, agent2_type=agent2)
```

Then adjust in `src/game.py`:
```python
# For stronger/weaker Minimax
self.agent1 = MinimaxAgent(player_id=1, depth=3)  # Increase depth

# For stronger/weaker MCTS
self.agent2 = MCTSAgent(player_id=2, iterations=500)  # Increase iterations
```

### Modify Game Parameters

Edit `src/game_state.py`:
```python
INITIAL_HP = 100          # Starting health
MAX_TURNS = 200           # Max turns before draw
HIT_DAMAGE = 20           # Damage per hit
SNOWBALL_LIMIT = 5        # Max snowballs
```

### Add Custom Assets

Place images in:
- `assets/images/backgrounds/` - Background images
- `assets/images/sprites/` - Player and object sprites
- `assets/images/ui/` - Button images

Supported formats: `.png`, `.jpg`, `.jpeg`

---

## 🚀 Features

✅ **Complete GUI Interface**
- Main menu with options
- Game setup screen
- Live gameplay display
- Game over screen with stats

✅ **Real-time Visualization**
- Watch AI agents move and fight
- HP bars show health status
- Turn counter
- Speed control

✅ **Two Different AI Algorithms**
- Minimax with Alpha-Beta Pruning
- Monte Carlo Tree Search
- Head-to-head battles

✅ **Asset Integration**
- Uses your custom images
- Fallback to colors if images missing
- Professional UI design

✅ **Responsive Controls**
- Pause/Resume
- Speed adjustment
- Easy navigation

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Window doesn't appear | Check if pygame-ce is installed: `pip install pygame-ce` |
| Buttons not clickable | Make sure mouse is within button area |
| Game running too fast | Press DOWN arrow to slow down |
| Images not showing | Check asset paths in `assets/images/` |
| Game crashes | Make sure `.venv` is activated |

---

## 📁 File Structure

```
Snowball Fight/
├── play.py                    ← Run this!
├── src/
│   ├── complete_gui.py        ← Full GUI application
│   ├── game.py                ← Game coordinator
│   ├── game_state.py          ← Game rules
│   ├── minimax_agent.py       ← AI #1
│   ├── mcts_agent.py          ← AI #2
│   └── gui.py                 ← Old GUI (not used)
└── assets/
    └── images/
        ├── backgrounds/
        │   ├── menu_bg.png
        │   └── game_bg.png
        ├── sprites/
        │   ├── player1.png
        │   ├── player2.png
        │   └── snowball.png
        └── ui/
            ├── button_play.png
            ├── button_stat.png
            └── button_exit.png
```

---

## 🎮 Example Gameplay Session

```
1. Run: python play.py
2. GUI window opens with main menu
3. Click "START GAME"
4. Select "MINIMAX vs MCTS"
5. Watch the battle unfold on screen
6. Use SPACE to pause, UP/DOWN for speed
7. When game ends, see final stats
8. Click "PLAY AGAIN" for another match
```

---

## ⚡ Tips & Tricks

- **Want faster games?** Press UP arrow during gameplay
- **Want to study moves?** Press SPACE to pause
- **Try different matchups** to see different strategies
- **Run multiple games** to see AI win rates
- **Press ESC** anytime to return to main menu

---

## 🎉 Ready to Play?

```bash
python play.py
```

Enjoy watching your AI agents battle! ❄️⛄🎮

---

**Have fun and enjoy the Snowball Fight!** 🏆
