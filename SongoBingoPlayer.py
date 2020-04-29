# Importing Required Modules & libraries
from tkinter import *
from Player.GUI_Builder import MusicPlayer

# Creating TK Container
root = Tk()
# Passing Root to MusicPlayer Class
MusicPlayer(root)
# Root Window Looping
root.mainloop()
