import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
import pygame
import random
import time
from pathlib import Path
import os
from Player.Winner_Tracker import GameTracker
import clipboard
import pandas as pd
from mutagen.mp3 import MP3


# Modified heavily from code at: https://www.codespeedy.com/build-a-music-player-with-tkinter-and-pygame-in-python/
def get_song_length(song_path):
    audio = MP3(song_path)
    total_length = audio.info.length
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    return f'{song_path} ~ {timeformat}'


# Defining SBPlayer Class
class SBPlayer(tk.Canvas):

    def __init__(self, root, simulation=False):
        self.root = root
        self.simulation = simulation
        super().__init__(root, width=400, height=400)
        # self.pack()

        # Title of the window
        self.root.title("SongoBingoPlayer by DJ AV")
        # Window Geometry
        self.root.geometry("1200x600")
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()
        # Setting up Music End event
        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)

        # Get Game directory from User
        self.game_path = Path(askdirectory(title='Select Songs Folder'))  # shows dialog box and return the path
        # self.game_path = Path("D:/TechWork/DJAV/SongoBingo/Files/GeneratedGames/Games_200508_IN/Game_200508_IN_1")
        self.songs_path = self.game_path / 'Songs'
        self.cards_path = self.game_path / 'Cards'

        # Init GameTracker
        self.tracker = GameTracker(self.game_path)

        # Fetch Songs from XLSX if simulated, or folder if using actual files
        if self.simulation:
            df = pd.read_excel(self.game_path / 'SongList.xlsx')
            unplayed_tracks = df['Song Sequence']
        else:
            unplayed_tracks = os.listdir(self.songs_path)

        self.songs_played_count = 0

        border = 3
        horz_center = 600

        # Create Frame for status logging
        logger_frame = LabelFrame(self.root, text="Game Play Log", font=("times new roman", 15, "bold"),
                                  bg="PeachPuff4", fg="white", bd=border, relief=FLAT)
        logger_frame.place(x=600, y=75, width=600, height=525)

        # Insert scrollbars
        scroll_y = Scrollbar(logger_frame, orient=VERTICAL)
        scroll_x = Scrollbar(logger_frame, orient=HORIZONTAL)

        # Insert Playlist listbox
        self.loglist = Listbox(logger_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, selectbackground="gold",
                               selectmode=SINGLE, font=("times new roman", 12, "bold"),
                               bg="PeachPuff2", fg="black", bd=border, relief=FLAT)
        # Applying Scrollbar to listbox
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.loglist.yview)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_x.config(command=self.loglist.xview)
        self.loglist.pack(fill=BOTH, expand=1)
        self.loglist.bindtags((self, root, "all"))

        # Create Button Frame
        self.buttonframe = LabelFrame(self.root, text="Controls", font=("times new roman", 15, "bold"),
                                      bg="coral", fg="white", bd=border, relief=FLAT)
        self.buttonframe.place(x=600, y=0, width=215, height=75)

        # Insert Play Button
        self.playbtn = Button(self.buttonframe, text="PLAY", command=self.play_song,
                              width=25, height=25, font=("times new roman", 16, "bold"),
                              fg="navyblue", bg="gold", relief=FLAT)

        # Creating a photoimage object to use image
        self.playbtn.img = PhotoImage(file="Assets/Play.png")
        # raise
        self.playbtn.config(image=self.playbtn.img)
        # self.playbtn.pack(side=TOP)
        self.playbtn.grid(row=0, column=0, padx=10, pady=10)

        # Inserting Stop Button
        self.stopbtn = Button(self.buttonframe, text="STOP", command=self.stop_song,
                              width=25, height=25, font=("times new roman", 16, "bold"),
                              fg="navyblue", bg="gold", relief=RAISED)

        # Creating a photoimage object to use image
        self.stopbtn.img = PhotoImage(file="Assets/Stop.png")
        # raise
        self.stopbtn.config(image=self.stopbtn.img)
        self.stopbtn.grid(row=0, column=2, padx=10, pady=10)

        # Inserting Pause Button
        self.pausebtn = Button(self.buttonframe, text="PAUSE", command=self.pause_song,
                               width=25, height=25, font=("times new roman", 16, "bold"),
                               fg="navyblue", bg="gold", relief=RAISED)
        # Creating a photoimage object to use image
        self.pausebtn.img = PhotoImage(file="Assets/Pause.png")
        # raise
        self.pausebtn.config(image=self.pausebtn.img)
        self.pausebtn.grid(row=0, column=1, padx=10, pady=5)

        # Inserting Add Song Button
        self.addsongbtn = Button(self.buttonframe, text="ADD SONG", command=self.add_song,
                               width=25, height=25, font=("times new roman", 16, "bold"),
                               fg="navyblue", bg="gold", relief=RAISED)
        # Creating a photoimage object to use image
        self.addsongbtn.img = PhotoImage(file="Assets/Add.png")
        # raise
        self.addsongbtn.config(image=self.addsongbtn.img)
        # self.addsongbtn.pack(side=TOP)

        self.addsongbtn.grid(row=0, column=3, padx=10, pady=5)

        # Creating Unplayed Songs Frame
        unplayed_songs_frame = LabelFrame(self.root, text="Playlist", font=("times new roman", 15, "bold"),
                                          bg="goldenrod", fg="white", bd=border, relief=FLAT)
        unplayed_songs_frame.place(x=0, y=0, width=600, height=600)
        # Insert scrollbar
        scroll_y = Scrollbar(unplayed_songs_frame, orient=VERTICAL)
        scroll_x = Scrollbar(unplayed_songs_frame, orient=HORIZONTAL)

        # Insert Playlist listbox
        self.unplaylist = ReOrderListbox(unplayed_songs_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set,
                                         selectbackground="gold", selectforeground="red", selectmode=SINGLE, font=("calibri light", 12, "bold"),
                                         bg="light goldenrod", fg="black", bd=border, relief=FLAT)
        # Applying Scrollbar to listbox
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.unplaylist.yview)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_x.config(command=self.unplaylist.xview)
        self.unplaylist.pack(side=LEFT, fill=BOTH, expand=1)

        # # Creating Played Songs frame
        # played_songs_frame = LabelFrame(self.root, text="Status", font=("times new roman", 15, "bold"),
        #                                 bg="grey", fg="white", bd=border, relief=FLAT)
        # played_songs_frame.place(x=850, y=0, width=350, height=75)
        #
        # # Insert scrollbar
        # scroll_y = Scrollbar(played_songs_frame, orient=VERTICAL)
        # scroll_x = Scrollbar(played_songs_frame, orient=HORIZONTAL)
        #
        # # Insert Playlist listbox
        # self.playlist = Listbox(played_songs_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set,
        #                         selectbackground="gold",selectmode=SINGLE, font=("times new roman", 12, "bold"),
        #                         bg="silver", fg="navyblue", bd=border, relief=FLAT)
        # # Applying Scrollbar to listbox
        # scroll_y.pack(side=RIGHT, fill=Y)
        # scroll_y.config(command=self.playlist.yview)
        # scroll_x.pack(side=BOTTOM, fill=X)
        # scroll_x.config(command=self.playlist.xview)
        # self.playlist.pack(side=LEFT, fill=BOTH, expand=1)
        # self.playlist.bindtags((self, root, "all"))

        # Creating Track Frame for Song label & status label
        self.trackframe = Label(self.root, text="Status", font=("times new roman", 15, "bold"), bg="black",
                                fg="white", bd=5, relief=GROOVE)
        # Creating a photoimage object to use image
        self.trackframe.img = PhotoImage(file="Assets/Logo.png")
        # raise
        self.trackframe.config(image=self.trackframe.img)
        self.trackframe.place(x=815, y=0, width=385, height=75)

        # # Inserting Song Track Label
        # songtrack = Label(trackframe, textvariable=self.track, width=20, font=("times new roman", 24, "bold"),
        #                   bg="grey", fg="gold").grid(row=0, column=0, padx=10, pady=5)
        # Inserting Status Label
        # trackstatus = Label(trackframe, textvariable=self.status, font=("times new roman", 24, "bold"), bg="grey",
        #                     fg="gold").grid(row=0, column=1, padx=10, pady=5)

        # Set up key and mouse bindings
        self.root.bind("<X>", self.play_key)
        self.root.bind("<x>", self.play_key)
        self.root.bind("<Return>", self.play_key)
        self.root.bind("<C>", self.pause_key)
        self.root.bind("<c>", self.pause_key)
        self.root.bind("<V>", self.stop_key)
        self.root.bind("<v>", self.stop_key)
        self.unplaylist.bind('<Double-1>', self.play_key)

        # # Set directory to Songs folder
        os.chdir(self.songs_path)
        # print(self.songs_path)
        # raise
        # Insert Shuffled Songs into Unplayed list
        random.shuffle(unplayed_tracks)
        for track in unplayed_tracks:
            if self.simulation:
                self.unplaylist.insert(END, track)
            else:
                song_with_time = get_song_length(track)
                self.unplaylist.insert(END, song_with_time)
        self.unplaylist.selection_set(first=0)
        print('Ready to play SONGBOLA!')

    # Defining Play Song Function
    def play_song(self):
        song_played = self.unplaylist.get(ACTIVE)
        self.unplaylist.selection_clear(ACTIVE, END)
        # Displaying Selected Song title
        self.track.set(song_played)
        self.playbtn.configure(relief='sunken')
        # Displaying Status
        self.status.set("Playing")

        # Put the song played on clipboard
        song_played = song_played.split(' ~ ')[0]
        clipboard.copy(song_played.replace('.mp3', ''))

        if self.simulation:
            time.sleep(0.25)
            self.process_song_end()
            self.playbtn.config(relief=SUNKEN)
        else:
            # Loading Selected Song
            pygame.mixer.music.load(song_played)
            # Playing Selected Song
            pygame.mixer.music.play()
            self.check_event()

    def check_event(self):
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:
                if self.status.get() == 'Playing':
                    self.process_song_end()
        self.root.after(100, self.check_event)

    def stop_song(self):
        # Displaying Status
        self.status.set("Stopped")
        self.playbtn.configure(relief=RAISED)
        self.pausebtn.configure(relief=RAISED)
        # Stopped Song
        pygame.mixer.music.stop()

    def pause_song(self):
        if self.status.get() == 'Playing':
            self.status.set("Paused")
            pygame.mixer.music.pause()
            self.pausebtn.configure(relief=SUNKEN)
        else:
            self.status.set("Playing")
            pygame.mixer.music.unpause()
            self.pausebtn.configure(relief=RAISED)

    def process_song_end(self):
        self.playbtn.configure(relief=RAISED)
        # Get index of song
        idx = self.unplaylist.get(0, END).index(self.track.get())
        # Mark it selected
        self.unplaylist.selection_set(idx)
        # Clean up song name
        song_played = self.unplaylist.get(idx).replace('.mp3', '')
        song_played = song_played.split(' ~ ')[0]

        # Insert song into Played Songs list
        # self.playlist.insert(END, song_played)
        # self.playlist.yview(END)

        # Update log
        self.loglist.insert(END, f'~ Song {self.songs_played_count:02} played: {song_played}')
        self.loglist.yview(END)

        # Evaluate Winners if any
        if GameTracker.valid_song_played(self.tracker, song_played, self.loglist):
            self.songs_played_count += 1

        # Remove song from Unplayed Songs list
        # self.unplaylist.delete(idx)

        # Change selected song to next
        # self.unplaylist.selection_clear(0, END)
        if idx + 1 < self.unplaylist.size():
            # self.unplaylist.selection_set(idx + 1)
            self.unplaylist.activate(idx + 1)
            # Play next song
            if not self.simulation:
                self.play_song()
        # else:
        #     self.loglist.insert(END, f'~~~ GAME OVER ~~~')

    def play_key(self, event):
        # print(f'Pressed {repr(event.char)}')
        self.play_song()

    def pause_key(self, event):
        # print(f'Pressed {repr(event.char)}')
        self.pause_song()

    def stop_key(self, event):
        # print(f'Pressed {repr(event.char)}')
        self.stop_song()

    def add_song(self):
        filename = tk.filedialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("Music files", "*.mp3"), ("all files", "*.*")))
        if filename != '':
            self.unplaylist.insert(END, filename)


class ReOrderListbox(tk.Listbox):
    # A tk listbox with drag'n'drop reordering of entries.
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.MULTIPLE
        kw['activestyle'] = 'none'
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.get_state, add='+')
        self.bind('<Button-1>', self.set_current, add='+')
        self.bind('<B1-Motion>', self.shift_selection)
        self.curIndex = None
        self.curState = None

    def set_current(self, event):
        # gets the current index of the clicked item in the listbox
        self.curIndex = self.nearest(event.y)

    def get_state(self, event):
        # checks if the clicked item in listbox is selected
        i = self.nearest(event.y)
        self.curState = 1

    def shift_selection(self, event):
        # shifts item up or down in listbox
        i = self.nearest(event.y)
        if self.curState == 1:
            self.selection_set(self.curIndex)
        else:
            self.selection_clear(self.curIndex)
        if i < self.curIndex:
            # Moves up
            x = self.get(i)
            selected = self.selection_includes(i)
            self.delete(i)
            self.insert(i + 1, x)
            if selected:
                self.selection_set(i + 1)
            self.curIndex = i
        elif i > self.curIndex:
            # Moves down
            x = self.get(i)
            selected = self.selection_includes(i)
            self.delete(i)
            self.insert(i - 1, x)
            if selected:
                self.selection_set(i - 1)
            self.curIndex = i
