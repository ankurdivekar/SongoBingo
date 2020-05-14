# Importing Required Modules & libraries
import tkinter as tk
from Player.GUI_Builder import SBPlayer

simulate_music_files = False

# Creating TK Container
root = tk.Tk()
player = SBPlayer(root, simulate_music_files)
player.focus_set()

# Root Window Looping
root.mainloop()
