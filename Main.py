from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import random


root = Tk()
root.title('Melodify')
root.iconbitmap(
    r'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/LOGO.ico')
root.geometry("900x500")
root.configure(background="#F7987F")
# initializing pygame mixer
pygame.mixer.init()


# grab song length and time info
def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos()/1000
    # slider_label.config(text=f'{int(melodify_slider.get())}/{int(current_time)}')
    # convert it to time format
    convert_curr_time = time.strftime('%M:%S', time.gmtime(current_time))
    # get current song
    current_song = song_box.curselection()
    song = song_box.get(current_song)
    song_path = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{song}.mp3'
    # load song length with mutagen
    song_mutagen = MP3(song_path)
    # get song lenght
    global song_length
    song_length = song_mutagen.info.length
    # converts to time format
    converted_song_length = time.strftime(
        '%H:%M:%S', time.gmtime(song_length))
    # increase current time by 1 sec
    current_time += 1
    if int(melodify_slider.get()) == int(song_length):
        status_bar.config(text=f'{converted_song_length} ')
    elif paused:
        pass
    elif int(melodify_slider.get()) == int(current_time):
        # update slider
        melodify_slider_position = int(song_length)
        melodify_slider.config(
            to=melodify_slider_position, value=int(current_time))
    else:
        # update slider
        melodify_slider_position = int(song_length)
        melodify_slider.config(to=melodify_slider_position,
                               value=int(melodify_slider.get()))
        # convert it to time format
        convert_curr_time = time.strftime(
            '%M:%S', time.gmtime(int(melodify_slider.get())))

        # output the time to status_bar
        status_bar.config(text=f'{convert_curr_time}/{converted_song_length} ')
        next_time = int(melodify_slider.get() + 1)
        melodify_slider.config(value=next_time)

    # checks if song and slider are the same
    if int(melodify_slider.get()) == int(song_length):
        # resets slider back to 0
        status_bar.config(text='')
        melodify_slider.config(value=0)

    # output the time to status_bar
    # status_bar.config(text=f'{convert_curr_time}/{converted_song_length} ')
    # update position slider to current song position
    # melodify_slider.config(value=int(current_time))

    # updates the time for the music
    status_bar.after(1000, play_time)


# Add a global variable to store the original order of songs
original_songs = []

# Modify the add_song and add_multiple_songs functions to update original_songs


def add_song():
    song = filedialog.askopenfilename(
        initialdir="Melodify/gui/audio", title="Choose a song", filetypes=(("mp3 files", "*.mp3"),))
    song = song.replace(
        "C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)
    original_songs.append(song)  # Add song to original_songs list


def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


def delete_multiple_song():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

    # selected_songs = song_box.curselection()
    # if selected_songs:  # Check if any songs are selected
    # Delete selected songs in reverse order to avoid index issues
    # for song_index in selected_songs[::-1]:
    # song_box.delete(song_index)
    # pygame.mixer.music.stop()


def add_multiple_songs():
    songs = filedialog.askopenfilenames(
        initialdir="Melodify/gui/audio", title="Choose some songs", filetypes=(("mp3 files", "*.mp3"),))
    for song in songs:
        song = song.replace(
            "C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)
        original_songs.append(song)  # Add song to original_songs list


# play selected song
def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    # needs directory here
    song = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # calls the play_time() to get song lenght
    play_time()


    # update slider
    # melodify_slider_position = int(song_length)
    # melodify_slider.config(to=melodify_slider_position, value=0)
global stopped
stopped = False


def stop():
    status_bar.config(text='')
    melodify_slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    status_bar.config(text='')
    global stopped
    stopped = True


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


# Modify the next() and back() functions to use original_songs after shuffling
# Modify the next() and back() functions to use shuffled song_box
def next():
    status_bar.config(text='')
    melodify_slider.config(value=0)
    current_song = song_box.get(ACTIVE)
    try:
        current_song_index = song_box.curselection()[0]
        next_song_index = (current_song_index + 1) % song_box.size()
        next_song = song_box.get(next_song_index)
        song = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{next_song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        song_box.selection_clear(0, END)
        song_box.activate(next_song_index)
        song_box.selection_set(next_song_index, last=None)
    except IndexError:
        pass


def back():
    status_bar.config(text='')
    melodify_slider.config(value=0)
    current_song = song_box.get(ACTIVE)
    try:
        current_song_index = song_box.curselection()[0]
        prev_song_index = (current_song_index - 1) % song_box.size()
        prev_song = song_box.get(prev_song_index)
        song = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{prev_song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        song_box.selection_clear(0, END)
        song_box.activate(prev_song_index)
        song_box.selection_set(prev_song_index, last=None)
    except IndexError:
        pass


loop_status = False  # Global variable to track loop status
current_song_index = 0  # Global variable to keep track of the current song index


def loop():
    global stopped, loop_status, current_song_index
    stopped = False

    # Check if looping is active
    if loop_status:
        song_count = song_box.size()

        # If the current song index is less than the total songs in the playlist
        if current_song_index < song_count:
            status_bar.config(text='')
            melodify_slider.config(value=0)
            song = song_box.get(current_song_index)
            song_path = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{song}.mp3'

            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(loops=0)

            # Get the duration of the current song
            play_time()
            # Set a timer to move to the next song after the current song finishes playing
            root.after(int(song_length) * 1000, next_song)

    else:
        pygame.mixer.music.stop()  # Stop playing if loop button is deactivated


def next_song():
    global current_song_index
    current_song_index += 1
    size = song_box.size()
    if current_song_index == size:
        current_song_index = current_song_index - size
    # clear the selection bar
    song_box.selection_clear(0, END)
    # activate new selection bar
    song_box.activate(current_song_index)
    # set the selection bar to next song
    song_box.selection_set(current_song_index, last=None)
    loop()  # Play the next song in the playlist


def toggle_loop():
    global loop_status, current_song_index
    if not loop_status:
        loop_status = True
        loop()
        loop_btn.config(relief="sunken")  # Change the button relief style
    else:
        loop_status = False
        loop_btn.config(relief="raised")  # Change the button relief style


def loop1():
    global stopped
    stopped = False
    status_bar.config(text='')
    melodify_slider.config(value=0)
    song = song_box.get(ACTIVE)
    song = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{song}.mp3'
    # Check if the loop button is active
    if loop_btn['relief'] == 'sunken':
        song = song_box.get(ACTIVE)
        song = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{song}.mp3'
        pygame.mixer.music.load(song)
        # Setting loops to -1 will make the song repeat indefinitely
        pygame.mixer.music.play(loops=-1)
    else:
        pygame.mixer.music.load(song)
        # If loop button is not active, play the song once
        pygame.mixer.music.play(loops=0)
    # calls the play_time() to get song length
    play_time()


def toggle_loop1():
    global loop_status, current_song_index
    if not loop_status:
        loop_status = True
        loop_btn.config(relief="sunken")  # Change the button relief style
        loop1()
    else:
        loop_status = False
        loop_btn.config(relief="raised")  # Change the button relief style


# Modify the shuffle() function to shuffle both song_box and original_songs
def shuffle():
    global original_songs, stopped
    stopped = False
    current_song = song_box.get(ACTIVE)

    temp_list = list(song_box.get(0, END))
    random.shuffle(temp_list)

    song_box.delete(0, END)
    for song in temp_list:
        song_box.insert(END, song)

    original_songs = temp_list
    # Reset the selection to the current song after shuffling
    if current_song in temp_list:
        index = temp_list.index(current_song)
        song_box.selection_clear(0, END)
        song_box.activate(index)
        song_box.selection_set(index, last=None)

    status_bar.config(text='')
    melodify_slider.config(value=0)


def slider(x):
    # slider_label.config(text=f'{int(melodify_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    # gets the song
    song = f'C:/Users/hp/OneDrive/Documents/GitHub/P3_Melodify/Melodify/gui/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(melodify_slider.get()))

# volume function


def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    # current_vol = pygame.mixer.music.get_volume()
    # slider_label.config(text=current_vol * 100)


def change_background(color):
    root.configure(background=color)
    master_frame.configure(background=color)
    control_frame.configure(background=color)
    back_btn.configure(background=color)
    next_btn.configure(background=color)
    play_btn.configure(background=color)
    loop1_btn.configure(background=color)
    loop_btn.configure(background=color)
    shuffle_btn.configure(background=color)


# Add global variables for font size and font family
current_font_size = 10
current_font_family = "Times"

# Function to change font size


def change_font_size(size):
    global current_font_size
    current_font_size = int(size)
    change_font((current_font_family, current_font_size))

# Function to change font family


def change_font_family(family):
    global current_font_family
    current_font_family = family
    change_font((current_font_family, current_font_size))

# Modify the change_font function to accept a tuple containing font family and size


def change_font(font):
    song_box.config(font=font)
    melodify_menu.config(font=font)
    # Add more widget configurations to change their fonts


master_frame = Frame(root, background="#F7987F")
master_frame.pack(pady=20)

# create playlist box
song_box = Listbox(master_frame, bg="black", fg="green", width=90,
                   selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)


# define player control buttons images
back_btn_img = PhotoImage(file='c:Melodify\gui\images\BACK.png')
next_btn_img = PhotoImage(file='c:Melodify\gui\images\\NEXT.png')
play_btn_img = PhotoImage(file='c:Melodify\gui\images\PLAY.png')
pause_btn_img = PhotoImage(file='c:Melodify\gui\images\PAUSE.png')
loop_btn_img = PhotoImage(file='c:Melodify\gui\images\LOOP.png')
loop1_btn_img = PhotoImage(
    file='c:Melodify\gui\images\LOOP 1.png')
shuffle_btn_img = PhotoImage(file='c:Melodify\gui\images\SHUFFLE.png')

# create player control frame
control_frame = Frame(master_frame, bg="#F7987F")
control_frame.grid(row=1, column=0, pady=20)

# volume frame
volume_frame = LabelFrame(master_frame, text='Volume')
volume_frame.grid(row=0, column=1, padx=20)

# create player control buttons
back_btn = Button(control_frame, image=back_btn_img,
                  borderwidth=0, bg="#F7987F", command=back)
next_btn = Button(control_frame, image=next_btn_img,
                  borderwidth=0, bg="#F7987F", command=next)
play_btn = Button(control_frame, image=play_btn_img,
                  borderwidth=0, bg="#F7987F", command=play)
pause_btn = Button(control_frame, image=pause_btn_img,
                   borderwidth=0, bg="#F7987F", command=lambda: pause(paused))
loop_btn = Button(control_frame, image=loop_btn_img,
                  borderwidth=0, bg="#F7987F", command=toggle_loop)
loop1_btn = Button(control_frame, image=loop1_btn_img,
                   borderwidth=0, bg="#F7987F", command=toggle_loop1)
shuffle_btn = Button(control_frame, image=shuffle_btn_img,
                     borderwidth=0, bg="#F7987F", command=shuffle)

loop_btn.grid(row=0, column=0, padx=10)
loop1_btn.grid(row=0, column=1, padx=10)
back_btn.grid(row=0, column=2, padx=10)
play_btn.grid(row=0, column=3, padx=10)
pause_btn.grid(row=0, column=4, padx=10)
next_btn.grid(row=0, column=5, padx=10)
shuffle_btn.grid(row=0, column=6, padx=10)

# create menu
melodify_menu = Menu(root)
root.config(menu=melodify_menu)


# add song menu
add_song_menu = Menu(melodify_menu, tearoff=False)
melodify_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
add_song_menu.add_command(
    label="Add Multiple Songs to Playlist", command=add_multiple_songs)

# delete song menu
delete_song_menu = Menu(melodify_menu, tearoff=False)
melodify_menu.add_cascade(label="Delete Songs", menu=delete_song_menu)
delete_song_menu.add_command(
    label="Remove a Song from playlist", command=delete_song)
delete_song_menu.add_command(
    label="Remove All from playlist", command=delete_multiple_song)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# background menu cascade
bg_menu = Menu(melodify_menu, tearoff=False)
melodify_menu.add_cascade(label="Change Background", menu=bg_menu)
# bg menu options
bg_menu.add_command(label="Light Blue",
                    command=lambda: change_background("light blue"))
bg_menu.add_command(label="Light Gray",
                    command=lambda: change_background("light gray"))
bg_menu.add_command(label="Change back to default",
                    command=lambda: change_background("#F7987F"))

# dark mode and light mode toggle tba

# Customize the font
custom_font_menu = Menu(melodify_menu, tearoff=False)
melodify_menu.add_cascade(label="Customize Font", menu=custom_font_menu)
# font size menu casscade thing
font_size_menu = Menu(custom_font_menu, tearoff=False)
custom_font_menu.add_cascade(label="Change Font Size", menu=font_size_menu)
# font size options
font_size_menu.add_command(label="10", command=lambda: change_font_size(10))
font_size_menu.add_command(label="12", command=lambda: change_font_size(12))
font_size_menu.add_command(label="14", command=lambda: change_font_size(14))
# font family menu cascade
font_menu = Menu(custom_font_menu, tearoff=False)
custom_font_menu.add_cascade(label="Change Font", menu=font_menu)
# font family options
font_menu.add_command(label="Times New Roman",
                      command=lambda: change_font_family("Times"))
font_menu.add_command(
    label="Helvetica", command=lambda: change_font_family("Helvetica"))


# position slider
melodify_slider = ttk.Scale(master_frame, from_=0, to=100,
                            orient=HORIZONTAL, value=0, command=slider, length=360)
melodify_slider.grid(row=2, column=0, pady=10)

# volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0,
                          orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

# slider label
# slider_label = Label(root, text=0)
# slider_label.pack(pady=10)
root.mainloop()
