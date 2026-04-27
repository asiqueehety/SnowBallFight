"""
Direct GUI Launcher for Snowball Fight
Run this to start the game with complete GUI interface
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the fixed GUI
from gui_fixed import CompleteGameGUI

if __name__ == "__main__":
    print("="*70)
    print("SNOWBALL FIGHT: AI vs AI Game")
    print("="*70)
    gui = CompleteGameGUI()
    gui.run()
