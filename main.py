import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame, os
from mutagen.mp3 import MP3
import time

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")
# Initialize Pygame
pygame.init()
pygame.mixer.init()

class MusicPlayer(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        # Basic setup
        self.title("Music Player")
        self.geometry("800x780")
        
        # Set the Icon of the window
        self.iconbitmap('graphics/widgets/mp3.ico')
        
        # Will Split up the window in 2 frames
        self.player_frame = ctk.CTkFrame(master = self,
                                        border_width = 5, 
                                        border_color = '#282828')
        self.player_frame.place(x = 0, y = 0, relwidth = 0.6, relheight = 1)
        
        # Check wether it was paused or because track ended
        self.status = 'QUEUE_EMPTY'    
        
        # FRAME 1
        # Create a white canvas to show the Image of the played music video
        self.image_played_mp4 = ctk.CTkCanvas(master = self.player_frame, bg = '#2B2B2B', width = 300, height = 300, highlightthickness = 0)
        self.image_played_mp4.place(relx = 0.5, rely = 0.08, anchor = 'n')
    
        self.image_canvas = self.convert_image('graphics/widgets/groove_music_player.png', size = (300,300))
        self.image_played_mp4.create_image(0, 0, image = self.image_canvas, anchor='nw')
        
        # The label of the played track
        self.played_track = ctk.CTkLabel(master = self.player_frame, text = 'Currently no song in Queue', fg_color = '#343638', corner_radius = 32)
        self.played_track.place(relx = 0.5, rely = 0.5, anchor ='n')
        
        # The progress to see the length of the song
        self.song_duration_bar = ctk.CTkProgressBar(master = self.player_frame, 
                                                    width = 300, 
                                                    height = 10, 
                                                    corner_radius = 32, 
                                                    border_color = '#343638', 
                                                    border_width = 3)
        self.song_duration_bar.place(relx = 0.5, rely = 0.6, anchor ='n')
        # When initialized set to 0
        self.song_duration_bar.set(0)
        
        # Place the label for the time passed of the sound
        self.time_passed_lbl = ctk.CTkLabel(master = self.player_frame, text = f'00:00')
        self.time_passed_lbl.place(relx = 0.07, rely = 0.588)
        
        # Place the label for the total time of a song
        self.time_full_lbl = ctk.CTkLabel(master = self.player_frame, text = f'00:00')
        self.time_full_lbl.place(relx = 0.86, rely = 0.588)
        
        # Creating the buttoms for the Music player
        self.bw_tk_img = self.convert_image('graphics/buttons/backward.png', size = (64,64))
        self.previous_song = tk.Button(master = self.player_frame, image = self.bw_tk_img, borderwidth = 0, highlightthickness = 0, bg = '#2B2B2B', activebackground = '#2B2B2B', command = self.previous_song) 
        self.previous_song.place(relx = 0.2, rely = 0.7, anchor ='n')
        
        self.pause_tk_img = self.convert_image('graphics/buttons/pause.png', size = (64,64))
        self.pause_song_btn = tk.Button(master = self.player_frame, image = self.pause_tk_img, borderwidth = 0, highlightthickness = 0, bg = '#2B2B2B', activebackground = '#2B2B2B', command = self.pause_song)
        self.pause_song_btn.place(relx = 0.4, rely = 0.7, anchor ='n')

        self.play_tk_img = self.convert_image('graphics/buttons/play.png', size = (64,64))
        self.play_song_btn = tk.Button(master = self.player_frame, image = self.play_tk_img, borderwidth = 0, highlightthickness = 0, bg = '#2B2B2B', activebackground = '#2B2B2B', command = self.play_song)
        self.play_song_btn.place(relx = 0.6, rely = 0.7, anchor ='n')

        self.fw_tk_img = self.convert_image('graphics/buttons/forward.png', size = (64,64))
        self.next_song_btn = tk.Button(master = self.player_frame, image = self.fw_tk_img, borderwidth = 0, highlightthickness = 0, bg = '#2B2B2B', activebackground = '#2B2B2B', command = self.next_song)
        self.next_song_btn.place(relx = 0.8, rely = 0.7, anchor ='n')
        
        # Slider for the song adjustment 
        self.adjust_volume = ctk.CTkSlider(master = self.player_frame, from_ = 0, to = 100, command = self.set_volume)
        self.adjust_volume.place(relx = 0.5, rely = 0.85, anchor ='n')
        # Use the starting value of the slider as initial value for the volume
        pygame.mixer.music.set_volume(self.adjust_volume.get() / 100)
        
        # Do not waant a label on the button so use Tkinter Buttons
        self.image_vol_up = self.convert_image('graphics/buttons/volume_up.png', size = (48,48))
        self.vol_up_label = tk.Label(master = self.player_frame, image = self.image_vol_up, borderwidth = 0, highlightthickness = 0, bg = '#2B2B2B', activebackground = '#2B2B2B')
        self.vol_up_label.place(relx = 0.8, rely = 0.86, anchor ='center')
        
        self.image_vol_down = self.convert_image('graphics/buttons/volume_down.png', size = (48,48))
        self.vol_down_label = tk.Label(master = self.player_frame, image = self.image_vol_down, borderwidth = 0, highlightthickness = 0, bg = '#2B2B2B', activebackground = '#2B2B2B')
        self.vol_down_label.place(relx = 0.2, rely = 0.86, anchor ='center')
        
        # FRAME 2
        # Use the initial directory
        self.music_dir = os.getcwd()
        # Define the position on the master window
        self.playlist_frame = ctk.CTkFrame(master = self,
                                           border_width = 5, 
                                           border_color = '#2B2B2B',
                                           fg_color = '#A53712')
        self.playlist_frame.place(relx = 0.6, y = 0, relwidth = 0.4, relheight = 1)
        
        self.image_playlist = ctk.CTkImage(dark_image = Image.open("graphics/widgets/playlist.png"), size = (32, 32))
        # Add Simple title to the Frame 
        self.title_label = ctk.CTkLabel(master = self.playlist_frame, 
                                        text = 'Playlist\t', 
                                        corner_radius = 10, 
                                        fg_color = '#F8F8F8',
                                        text_color = '#920000',
                                        image = self.image_playlist,
                                        compound = "right",
                                        font = (None, 22, 'bold')
                                        )
        self.title_label.place(relx = 0.5, rely = 0.01, anchor = 'n', relwidth = 0.8, relheight = 0.08)
        
        # Need to get a view of all the songs in the selected directory
        # If u want to use a function parse it onto the Class want to have the button to have
        
        self.scrollable_frame_btn = ScrollableBtnFrame(
                                        master = self.playlist_frame,
                                        music_directory = self.music_dir,
                                        play_song = self.button_frame_event)
        
        self.scrollable_frame_btn.place(relx = 0.1, rely= 0.1, relwidth = 0.8, relheight = 0.7)
        
        # Add a figure to the button
        self.image_folder = ctk.CTkImage(dark_image = Image.open('graphics/buttons/folder.png'), size = (32, 32))
        # Need to add a button to select the folder
        self.music_folder_btn = ctk.CTkButton(master = self.playlist_frame, 
                                           text = "Select Music folder", 
                                           corner_radius = 10,
                                           fg_color = '#616365',
                                           border_color = '#23272B',
                                           hover_color = '#B9D3F1',
                                           border_width = 3,
                                           hover = True,
                                           image = self.image_folder,
                                           command = self.select_folder)
        self.music_folder_btn.place(relx = 0.5, rely = 0.85, anchor = 'n', relwidth = 0.8, relheight = 0.08)
        
    def select_folder(self):
        filepath = filedialog.askdirectory(initialdir = f"{self.music_dir}", title = "Directory containing Music")
        self.music_dir = filepath
        # Call the method to update the scrollable frame with the new directory
        self.scrollable_frame_btn.create_playlist(music_directory = self.music_dir)
    
    def button_frame_event(self, song):
        # Want to connect the full path
        self.path_to_song = os.path.join(self.music_dir, song)

        # Load in the music as Pygame
        pygame.mixer.music.load(self.path_to_song)
        # Save the currently played song
        self.currently_playing = song
        # Set the label to the song currently playing
        self.played_track.configure(text = f'{song[:-4]}') 
        
        # Get the audio in seconds 
        self.audio = MP3(self.path_to_song)

        self.convert_total_time = time.strftime("%M:%S", time.gmtime(self.audio.info.length))
        
        # Keeps increasing since due to the time played >> Change the label as well
        self.time_full_lbl.configure(text = f'{self.convert_total_time}')
        
        # Play the music using Pygame
        pygame.mixer.music.play()
        # Once start playing the first song >> want to make sure it is kept in a loop and goes to the next song
        self.music_play_time()
        self.change_color_button()
        self.get_time_song()
     
    def pause_song(self):
        # Pause the currenlty playing song
        pygame.mixer.music.pause()
        # Set the status on paused
        self.status = 'PAUSE'
    
    def play_song(self):
        # Play the song which has been paused
        pygame.mixer.music.unpause()
        # Set the status to unpaused 
        self.status = 'UNPAUSE'
        
    def next_song(self):
        # Get the index of the currenlty playing song
        index = self.scrollable_frame_btn.song_list.index(self.currently_playing)
        # If the index is lower then then length of the list -1, then increase the index with one to get the next song in the list
        if index < len(self.scrollable_frame_btn.song_list) - 1: next_song_to_play = self.scrollable_frame_btn.song_list[index + 1]
        # Else jsut start back from the first song
        else: next_song_to_play = self.scrollable_frame_btn.song_list[0]
        
        # Set the status to next song playing
        self.status = 'NEXT'
        # Call the function to change the song to play
        self.button_frame_event(song = next_song_to_play)
    
    def previous_song(self):
        # Get the index of the currenlty playing song
        index = self.scrollable_frame_btn.song_list.index(self.currently_playing)
        # If the index is lower then then length of the list -1, then increase the index with one to get the next song in the list
        if index != 0 : prev_song_to_play = self.scrollable_frame_btn.song_list[index - 1]
        # Else jsut start back from the first song
        else: prev_song_to_play = self.scrollable_frame_btn.song_list[len(self.scrollable_frame_btn.song_list) - 1]
        
        # Set the status to Prev song started
        self.status = 'PREV'
        # Call the function to change the song to play
        self.button_frame_event(song = prev_song_to_play)
        
    # Slider upon moving returns a value to the function. So what can do >> give an argument in the function that prints the value for the volume
    def set_volume(self, value):
        # Divide by 100 since the value for volume is expected to be between 0 - 1
        vol_val = value / 100
        # Set the volume using the pygame music
        pygame.mixer.music.set_volume(vol_val)
    
    # Check if there is any song playing
    def music_play_time(self):
        self.action = pygame.mixer.music.get_busy()
        # If nothing is playing and the action of the music was set to Pause
        if not self.action and self.status != 'PAUSE':
            # If the song is finished playing want to get the next song
            self.next_song()
        # If True then do nothing since it is still playing or was not playing or ended. 
        else: 
            pass
        
        # This makes sure the function is constanly ran on repeat
        self.after(1000, self.music_play_time)
    
    def get_time_song(self):
        # Get the time in ms played
        self.time_played_ms = pygame.mixer.music.get_pos()
        # Converty to seconds how much has been passed
        self.convert_min_sc = time.strftime("%M:%S", time.gmtime(self.time_played_ms / 1000))
        # Keeps increasing since due to the time played >> Change the label as well
        self.time_passed_lbl.configure(text = f'{self.convert_min_sc}')
        
        # Call the function to update the progressbar
        self.progressbar_set_time()
        
        self.after(500, self.get_time_song)
    
    def progressbar_set_time(self):
        
        # Get the length of the video in seconds
        self.audio.info.length
        
        # get the estimated time in ms
        self.time_played_seconds = round(self.time_played_ms / 1000, 0)
        
        # Get the estimated time in seconds
        self.value_progressbar = self.time_played_seconds / self.audio.info.length
        # Set the value for the Progressbar
        self.song_duration_bar.set(self.value_progressbar)
    
    def change_color_button(self):
        # Get the index of the currenlty playing song
        index = self.scrollable_frame_btn.song_list.index(self.currently_playing)
        
        for i, button in enumerate(self.scrollable_frame_btn.button_list):
           
            if index == i: 
                button.configure(fg_color = "#F1DF76")
            else:
                button.configure(fg_color = '#B3AEAD')

        self.after(1000, self.change_color_button)
    
    # Simple function to convert the images to display
    def convert_image(self, image, size):
        
        self.read_img = Image.open(image)
        self.tk_image = ImageTk.PhotoImage(self.read_img.resize(size, Image.Resampling.LANCZOS))
        return self.tk_image

# Create an new class explicit for the scrollable frame
class ScrollableBtnFrame(ctk.CTkScrollableFrame):
    
    def __init__(self, master, music_directory, play_song):
        super().__init__(master)
        
        # Only want to have one column to use
        self.grid_columnconfigure(index = 0, weight = 1)
        # The folder to the music directory
        self.music_directory = music_directory
        # Undefined number of buttons to press
        self.button_list = []
        # Creating the playlist
        self.create_playlist(self.music_directory)
        # Parse the function which is used in the main class to play the song
        self.playsong = play_song
    
    # Create the button for each song in the playlist
    def create_playlist(self, music_directory):
        # Clear the existing list of any buttons
        for btn in self.button_list:
            btn.destroy()
        
        # Get all the songs in the folder selected
        self.songs_to_play = os.listdir(music_directory)
        # Update the directory folder to the selected location
        self.music_directory = music_directory
        
        # List of buttons containing all the songs
        self.button_list = []
        # List with all the song names
        self.song_list = []
        # Add the play button image
        self.play_btn_img = ctk.CTkImage(dark_image = Image.open('graphics/widgets/song.png'), size = (32, 32))
        
        for i, song in enumerate(self.songs_to_play):
            splitted_ext = os.path.splitext(song)

            if splitted_ext[1] == '.mp3':
                song_button = ctk.CTkButton(master = self, 
                                            text = song[:-4], 
                                            width = 350, 
                                            height = 50, 
                                            corner_radius = 10,
                                            fg_color = '#B3AEAD',
                                            border_color = '#495766',
                                            border_width = 3,
                                            hover_color = '#ABC4E2',
                                            image = self.play_btn_img,
                                            compound = "left",
                                            anchor = "w",
                                            text_color = '#2B2B2B',
                                            command = lambda song = song:  self.playsong(song))
                song_button.grid(row = i, column = 0, padx = 3, pady = 2)
                self.button_list.append(song_button)   
                self.song_list.append(song)     


if __name__ == "__main__":
    mp = MusicPlayer()
    mp.mainloop()