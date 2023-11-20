from tkinter import *
import pygame
from tkinter import filedialog


root = Tk()
root.title('Melodify')
root.iconbitmap(
    'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/Melodify.ico')
root.geometry("600x400")

# initializing pygame mixer
pygame.mixer.init()

# add song function


def add_song():
    # insert directory here in initialdir
    song = filedialog.askopenfilename(
        initialdir="", title="Choose a song", filetypes=(("mp3 files", "*.mp3"),))
    # removes the file address and .mp3 from song(needs directory here)
    ''''song = song.replace("", "")
    song = song.replace(".mp3", "")'''
    song_box.insert(END, song)

# play selected song


def play():
    song = song_box.get(ACTIVE)
    # needs directory here
    song = f''
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

# stop playing current song


def pause():
    pygame.mixer.music.pause()


# create playlist box
song_box = Listbox(root, bg="black", fg="green", width=90,
                   selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# define player control buttons images
back_btn_img = PhotoImage()
forward_btn_img = PhotoImage()
play_btn_img = PhotoImage()
pause_btn_img = PhotoImage()
stop_btn_img = PhotoImage()
repeat_btn_img = PhotoImage()

# create player control frame
control_frame = Frame(root)
control_frame.pack()

# create player control buttons
back_btn = Button(control_frame, image=back_btn_img, borderwidth=0)
forward_btn = Button(control_frame, image=forward_btn_img, borderwidth=0)
play_btn = Button(control_frame, image=play_btn_img,
                  borderwidth=0, command=play)
pause_btn = Button(control_frame, image=pause_btn_img,
                   borderwidth=0, command=pause)
stop_btn = Button(control_frame, image=stop_btn_img, borderwidth=0,)
repeat_btn = Button(control_frame, image=repeat_btn_img, borderwidth=0)

back_btn.grid(row=0, column=0, padx=10)
forward_btn.grid(row=0, column=1, padx=10)
play_btn.grid(row=0, column=2, padx=10)
pause_btn.grid(row=0, column=3, padx=10)
stop_btn.grid(row=0, column=4, padx=10)
repeat_btn.grid(row=0, column=5, padx=10)

# create menu
melodify_menu = Menu(root)
root.config(menu=melodify_menu)

# add song menu
add_song_menu = Menu(melodify_menu)
melodify_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)

root.mainloop()
