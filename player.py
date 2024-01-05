from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

#Initialize Pygame
pygame.mixer.init()

#Create function to Deal with Time
def play_time():
    #Check to see if song is stopped
    if stopped:
        return

    #Grab current song time
    current_time = pygame.mixer.music.get_pos()/1000
    #Convert song time from mili seconds to time format
    converted_current_time = time.strftime('%H:%M:%S',time.gmtime(current_time))

     #Find Current Song Length
    song = playlist_box.get(ACTIVE)
    #Reconstruct song path from song name
    song = f'D:/Rahul Noronha/Projects/Miscellaneous/PythonMP3Player/audio/{song}.mp3'
    song_mut = MP3(song)
    global converted_song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%H:%M:%S',time.gmtime(song_length))

    #Check to see if song is over
    if int(song_slider.get()==int(song_length)):
        stop()

    elif paused:
        #Check to see if paused, if so pass
        pass
    else:
        #Move slider along 1 second at a time
        next_time = int(song_slider.get())+1

        #output new time value to slider #Set slider length to song length
        song_slider.config(to=song_length, value=next_time)

        #Convert slider position to time format
        converted_current_time = time.strftime('%H:%M:%S',time.gmtime(int(song_slider.get())))

        #Output slider
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')


    #Add Current time to status bar
    if(current_time>=0):
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
    
    #Create loop to check the time every second
    status_bar.after(1000, play_time)

   

#Create function to add one song to playlist
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files","*.mp3"),))
    #Strip out directory structure and .mp3 from song title
    song = song.replace("D:/Rahul Noronha/Projects/Miscellaneous/PythonMP3Player/audio/","")
    song = song.replace(".mp3","")
    #Add to end of Playlist
    playlist_box.insert(END, song)

#Create function to add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files","*.mp3"),))
    #Strip out directory structure and .mp3 from song list by looping through song list
    for song in songs:
        song = song.replace("D:/Rahul Noronha/Projects/Miscellaneous/PythonMP3Player/audio/","")
        song = song.replace(".mp3","")
        #Add to end of Playlist
        playlist_box.insert(END, song)

#Create function to delete one song from playlist
def delete_song():
    #Delete highlighted song from menu
    playlist_box.delete(ANCHOR)

#Create function to delete all songs from playlist
def delete_all_songs():
    #Delete all songs
    playlist_box.delete(0, END)

#Create Play Function
def play():
    global stopped
    global paused
    stopped = False
    paused = False
    song = playlist_box.get(ACTIVE)
    #Reconstruct song path from song name
    song = f'D:/Rahul Noronha/Projects/Miscellaneous/PythonMP3Player/audio/{song}.mp3'

    #Load song with pygame mixer
    pygame.mixer.music.load(song)
    #Play song with pygame mixer
    pygame.mixer.music.play(loops=0)

    #Get Song time
    play_time()

#Create Stop Function
global stopped
stopped = False
def stop():
    global paused
    #Stop the song
    pygame.mixer.music.stop()
    #Clear Playlist Bar
    playlist_box.selection_clear(ACTIVE)
    paused = False
    #Reset time after stop is clicked
    status_bar.config(text="Time Elapsed: 00:00:00")

    #Set slider to zero
    song_slider.config(value=0)

    #Set stop variable to true
    global stopped
    stopped = True

#Create paused variable
global paused
paused = False
#Create PauseFunction
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        #Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #Pause
        pygame.mixer.music.pause()
        paused = True

#Create function to play the next song
def next_song():
    #Reset slider position and status bar
    status_bar.config(text="Time Elapsed: 00:00:00")
    song_slider.config(value=0)
    global paused
    paused = False
    #Get number of items in playlist

    #Get current song number
    next_one = playlist_box.curselection()
    #Add one to the current song number
    next_one = next_one[0]+1

    #Get length of Playlist
    playlist_len = len(playlist_box.get(0,END))

    #If song is at the last song, go back to first song on clicking Forward button
    if (next_one>playlist_len-1):
        next_one=0

    #Grab the song title from the playlist
    song = playlist_box.get(next_one)
    #Reconstruct song path from song name
    song = f'D:/Rahul Noronha/Projects/Miscellaneous/PythonMP3Player/audio/{song}.mp3'
    #Load song with pygame mixer
    pygame.mixer.music.load(song)
    #Play song with pygame mixer
    pygame.mixer.music.play(loops=0)

    #Clear active bar in Playlist
    playlist_box.select_clear(0,END)

    #Move Active bar to next song
    playlist_box.activate(next_one)

    #Set Active bar to next song
    playlist_box.selection_set(next_one, last=None)

#Create function to play the previous song
def previous_song():
    #Reset slider position and status bar
    status_bar.config(text="Time Elapsed: 00:00:00")
    song_slider.config(value=0)
    global paused
    paused = False
    #Get current song number
    next_one = playlist_box.curselection()
    #Remove one from  the current song number
    next_one = next_one[0]-1

    #Get length of Playlist
    playlist_len = len(playlist_box.get(0,END))

    #If song is at the first, go back to last song on clicking Previous button
    if (next_one<0):
        next_one=playlist_len-1

    #Grab the song title from the playlist
    song = playlist_box.get(next_one)
    #Reconstruct song path from song name
    song = f'D:/Rahul Noronha/Projects/Miscellaneous/PythonMP3Player/audio/{song}.mp3'
    #Load song with pygame mixer
    pygame.mixer.music.load(song)
    #Play song with pygame mixer
    pygame.mixer.music.play(loops=0)

    #Clear active bar in Playlist
    playlist_box.select_clear(0,END)

    #Move Active bar to next song
    playlist_box.activate(next_one)

    #Set Active bar to next song
    playlist_box.selection_set(next_one, last=None)

#Create volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

#Create slide function for song positioning
def slide(x):
    song = playlist_box.get(ACTIVE)
    #Reconstruct song path from song name
    song = f'D:/Rahul Noronha/Projects/Miscellaneous/PythonMP3Player/audio/{song}.mp3'

    #Load song with pygame mixer
    pygame.mixer.music.load(song)
    #Play song with pygame mixer
    pygame.mixer.music.play(loops=0, start=song_slider.get())


#Create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

#Create volume slider frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

#Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, length=125, command=volume, value=0.5)
volume_slider.pack(pady=10)

#Create Song Slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, command=slide, value=0)
song_slider.grid(row=2, column=0, pady=20)

#Create playlist box
playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)

#Define Button Images for Controls
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')

#create Button Frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

#Create Play/Stop and other Buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Create Add Song menu dropdowns
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
#Add One Song to Playlist
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
#Add Many Songs to Playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

#Create Delete Song menu dropdowns
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song from Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs from Playlist", command=delete_all_songs)

#Create Status Bar
status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#Temporary Label
my_label = Label(root, text="")
my_label.pack(pady=20)
root.mainloop()