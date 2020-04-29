from tkinter import *
from tkinter.filedialog import askdirectory
import pygame
import random
import os
from Player.Winner_Tracker import GameTracker
import clipboard
from mutagen.mp3 import MP3


# Modified heavily from code at: https://www.codespeedy.com/build-a-music-player-with-tkinter-and-pygame-in-python/

# Defining MusicPlayer Class
class MusicPlayer:

    # Constructor
    def __init__(self, root):
        self.root = root
        # Title of the window
        self.root.title("SongoBingo Player")
        # Window Geometry
        self.root.geometry("950x600+200+200")
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
        # self.game_path = askdirectory(title='Select Songs Folder')  # shows dialog box and return the path
        self.game_path = "D:/TechWork/DJAV/SongoBingo/Files/GeneratedGames/Games_200418_SG/Game_200418_SG_1"
        self.songs_path = self.game_path + '/Songs'
        self.cards_path = self.game_path + '/Cards'

        # Init GameTracker
        self.tracker = GameTracker(self.game_path)

        # Fetch Songs
        unplayed_tracks = os.listdir(self.songs_path)
        # Set directory to Songs folder
        os.chdir(self.songs_path)

        border = 3
        relief = FLAT

        # Create Frame for status logging
        logger_frame = LabelFrame(self.root, text="Game Play Log", font=("times new roman", 15, "bold"),
                                  bg="grey", fg="white", bd=border, relief=relief)
        logger_frame.place(x=400, y=200, width=550, height=400)

        # Insert scrollbar
        scroll_y = Scrollbar(logger_frame, orient=VERTICAL)

        # Insert Playlist listbox
        self.loglist = Listbox(logger_frame, yscrollcommand=scroll_y.set, selectbackground="gold",
                               selectmode=SINGLE, font=("times new roman", 12, "bold"),
                               bg="silver", fg="navyblue", bd=border, relief=relief)
        # Applying Scrollbar to listbox
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.loglist.yview)
        self.loglist.pack(fill=BOTH, expand=1)
        self.loglist.bindtags((self, root, "all"))

        # Create Button Frame
        buttonframe = LabelFrame(self.root, text="Controls", font=("times new roman", 15, "bold"),
                                 bg="grey", fg="white", bd=border, relief=relief)
        buttonframe.place(x=400, y=0, width=150, height=200)
        # Insert Play Button
        playbtn = Button(buttonframe, text="PLAY", command=self.play_song,
                         width=9, height=1, font=("times new roman", 16, "bold"),
                         fg="navyblue", bg="gold").grid(row=0, column=0, padx=10, pady=20)

        # Inserting Stop Button
        playbtn = Button(buttonframe, text="STOP", command=self.stop_song,
                         width=9, height=1, font=("times new roman", 16, "bold"),
                         fg="navyblue", bg="gold").grid(row=1, column=0, padx=10, pady=20)

        # Creating Unplayed Songs Frame
        unplayed_songs_frame = LabelFrame(self.root, text="Unplayed Songs", font=("times new roman", 15, "bold"),
                                          bg="grey", fg="white", bd=border, relief=relief)
        unplayed_songs_frame.place(x=0, y=0, width=400, height=600)

        # # Insert scrollbar
        scroll_y = Scrollbar(unplayed_songs_frame, orient=VERTICAL)

        # Insert Playlist listbox
        self.unplaylist = Listbox(unplayed_songs_frame, yscrollcommand=scroll_y.set, selectbackground="gold",
                                  selectmode=SINGLE, font=("times new roman", 12, "bold"),
                                  bg="silver", fg="navyblue", bd=border, relief=FLAT)
        # Applying Scrollbar to listbox
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.unplaylist.yview)
        self.unplaylist.pack(fill=BOTH, expand=1)

        # Insert Shuffled Songs into Unplayed list
        random.shuffle(unplayed_tracks)
        for track in unplayed_tracks:
            song_with_time = self.get_song_length(track)
            self.unplaylist.insert(END, song_with_time)

        # Creating Played Songs frame
        played_songs_frame = LabelFrame(self.root, text="Played Songs", font=("times new roman", 15, "bold"),
                                        bg="grey", fg="white", bd=border, relief=relief)
        played_songs_frame.place(x=550, y=0, width=400, height=200)

        # Insert scrollbar
        scroll_y = Scrollbar(played_songs_frame, orient=VERTICAL)

        # Insert Playlist listbox
        self.playlist = Listbox(played_songs_frame, yscrollcommand=scroll_y.set, selectbackground="gold",
                                selectmode=SINGLE, font=("times new roman", 12, "bold"),
                                bg="silver", fg="navyblue", bd=border, relief=relief)
        # Applying Scrollbar to listbox
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH, expand=1)
        self.playlist.bindtags((self, root, "all"))

    # Defining Play Song Function
    def play_song(self):
        song_played = self.unplaylist.get(ACTIVE)
        song_played = song_played.split(' ~ ')[0]
        # Displaying Selected Song title
        self.track.set(song_played)
        # Displaying Status
        self.status.set("Playing")
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
        # Stopped Song
        pygame.mixer.music.stop()

    def process_song_end(self):
        song_played = self.unplaylist.get(ACTIVE).replace('.mp3', '')
        song_played = song_played.split(' ~ ')[0]
        # Insert song into Played Songs list
        self.playlist.insert(END, song_played)
        self.playlist.yview(END)
        # Remove song from Unplayed Songs list
        self.unplaylist.delete(ANCHOR)
        self.loglist.insert(END, f'~ Song played: {song_played}')
        self.loglist.yview(END)
        clipboard.copy(song_played)
        GameTracker.song_played(self.tracker, song_played, self.loglist)

    def get_song_length(self, song_path):
        audio = MP3(song_path)
        total_length = audio.info.length
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        return f'{song_path} ~ {timeformat}'
