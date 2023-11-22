from tkinter import *
import pygame
from tkinter import filedialog


root = Tk()
root.title('Melodify')
root.iconbitmap(
    r'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/LOGO.ico')
root.geometry("600x400")
root.configure(background="light blue")
# initializing pygame mixer
pygame.mixer.init()


# add song function
def add_song():
    # way to browse songs
    song = filedialog.askopenfilename(
        initialdir="Melodify/gui/audio", title="Choose a song", filetypes=(("mp3 files", "*.mp3"),))
    # removes the file address and .mp3 from song
    song = song.replace(
        "C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)


def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


# def deletion_selection():
    # selected_indices = song_box.curselection()
    # Delete each selected item in reverse order to avoid index issues
    # for i in reversed(selected_indices):
    #    song_box.delete(i)
    # pygame.mixer.music.stop()


def delete_multiple_song():
    song_box.delete(0, END)
    pygame.mixer.music.stop()

# multiple songs


def add_multiple_songs():
    # same shit
    songs = filedialog.askopenfilenames(
        initialdir="Melodify/gui/audio", title="Choose some songs", filetypes=(("mp3 files", "*.mp3"),))
    # looping and replacing directory
    for song in songs:
        song = song.replace(
            "C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)


# play selected song
def play():
    song = song_box.get(ACTIVE)
    # needs directory here
    song = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)


# global thing (can be used in and out of the function stuff)
global paused
paused = False


# pauses the current music
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


# play next song
def next():
    # grabs the tuple number of current song
    next_song = song_box.curselection()
    # adds one to current tuple number
    next_song = next_song[0]+1
    size = song_box.size()
    if next_song == size:
        next_song = next_song - size
    # adds thedirectory back to the file
    song = song_box.get(next_song)
    song = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # clear the selection bar
    song_box.selection_clear(0, END)
    # activate new selection bar
    song_box.activate(next_song)
    # set the selection bar to next song
    song_box.selection_set(next_song, last=None)


# play previous song
def back():
    # grabs the tuple number of current song
    prev_song = song_box.curselection()
    # subtracts one to current tuple number
    prev_song = prev_song[0]-1
    size = song_box.size()
    if prev_song == -1:
        prev_song = prev_song + size
    # adds the directory and .mp3 back to the file
    song = song_box.get(prev_song)
    song = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # clear the selection bar
    song_box.selection_clear(0, END)
    # activate new selection bar
    song_box.activate(prev_song)
    # set the selection bar to next song
    song_box.selection_set(prev_song, last=None)


# loop all song


def loop():
    pass

# loop 1 song


def loop1():
    pass


# create playlist box
song_box = Listbox(root, bg="black", fg="green", width=90,
                   selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# define player control buttons images
back_btn_img = PhotoImage(file='c:Melodify\gui\images\BACK.png')
next_btn_img = PhotoImage(file='c:Melodify\gui\images\\NEXT.png')
play_btn_img = PhotoImage(file='c:Melodify\gui\images\PLAY.png')
pause_btn_img = PhotoImage(file='c:Melodify\gui\images\PAUSE.png')
loop_btn_img = PhotoImage(file='c:Melodify\gui\images\LOOP.png')
loop1_btn_img = PhotoImage(
    file='c:Melodify\gui\images\LOOP 1.png')

# create player control frame
control_frame = Frame(root, bg="light blue")
control_frame.pack()

# create player control buttons
back_btn = Button(control_frame, image=back_btn_img,
                  borderwidth=0, bg="light blue", command=back)
next_btn = Button(control_frame, image=next_btn_img,
                  borderwidth=0, command=next)
play_btn = Button(control_frame, image=play_btn_img,
                  borderwidth=0, command=play)
pause_btn = Button(control_frame, image=pause_btn_img,
                   borderwidth=0, command=lambda: pause(paused))
loop_btn = Button(control_frame, image=loop_btn_img,
                  borderwidth=0, command=loop)
loop1_btn = Button(control_frame, image=loop1_btn_img,
                   borderwidth=0, command=loop1)


back_btn.grid(row=0, column=0, padx=10)
play_btn.grid(row=0, column=1, padx=10)
pause_btn.grid(row=0, column=2, padx=10)
next_btn.grid(row=0, column=3, padx=10)
loop_btn.grid(row=0, column=4, padx=10)
loop1_btn.grid(row=0, column=5, padx=10)

# create menu
melodify_menu = Menu(root)
root.config(menu=melodify_menu)

# add song menu
add_song_menu = Menu(melodify_menu)
melodify_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
add_song_menu.add_command(
    label="Add Multiple Songs to Playlist", command=add_multiple_songs)

# delete song menu
delete_song_menu = Menu(melodify_menu)
melodify_menu.add_cascade(label="Delete Songs", menu=delete_song_menu)
delete_song_menu.add_command(
    label="Remove a Song from playlist", command=delete_song)
delete_song_menu.add_command(
    label="Remove Multiple from playlist", command=delete_multiple_song)

root.mainloop()
