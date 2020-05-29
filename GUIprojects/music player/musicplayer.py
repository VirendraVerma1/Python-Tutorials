from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from ttkthemes import themed_tk as tk
import os
import time
import tkinter.messagebox
import threading

#variables
playlist=[]
index=0
pause=FALSE
mute=FALSE
play=FALSE
repeat="none"
song_over=FALSE

#-------------------------------------------functions area--------------------------------
def about_us():
    tkinter.messagebox.showinfo("Music Player","I are anonymous you do not have to know about me.")

def add_playlist():
    global filename_path
    global index
    filename_path=filedialog.askopenfilename()
    filename=os.path.basename(filename_path)
    listbox.insert(index,filename)
    listbox.pack()
    playlist.insert(index,filename_path)
    index+=1
    statusbar['text']=filename+" is added to your playlist"

def del_playlist():
    if listbox.curselection():
        selected_song=listbox.curselection()
        selected_song=int(selected_song[0])
        statusbar['text'] = playlist[selected_song] + " is deleted to your playlist"
        listbox.delete(selected_song)
        playlist.pop(selected_song)
    else:
        tkinter.messagebox.showinfo("Music Player", "Please Select the song to delete")

def set_volume(val):
    global volume
    volume=float(val)/100
    mixer.music.set_volume(volume)

def repeat_song():
    global repeat
    if repeat=='none':
        repeat='current'
        repeat_button.configure(image=photo_repeatcurrent)
    elif(repeat=='current'):
        repeat='all'
        repeat_button.configure(image=photo_repeatall)
    else:
        repeat='none'
        repeat_button.configure(image=photo_repeatnone)

def mute_song():
    global mute,volume
    if mute==FALSE: #make unmute
        scale.set(0)
        mixer.music.set_volume(0)
        mute = TRUE
        mute_button.configure(image=photo_mute)
        statusbar['text'] = filename + " has been muted"
    else: # make mute
        if volume:
            scale.set(volume*100)
            mixer.music.set_volume(volume)
        else:
            scale.set(70)
            mixer.music.set_volume(.7)
        mute=FALSE
        mute_button.configure(image=photo_unmute)
        statusbar['text'] = filename + " has been unmuted"

def get_current_duration(ttime):
    global pause,timeformat,song_over,repeat
    x=0
    while x<=ttime and mixer.music.get_busy():
        if pause:
            continue
        else:
            mins, secs = divmod(x, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttime_label['text'] = timeformat
            x += 1
            time.sleep(1)
    x+=1
    if(x>=ttime):
        if(repeat=='current'):
            play_song()
        elif(repeat=='all'):
            play_song()

def get_total_duration():
    global playlist,filename_path,filename,selected_song
    selected_song = listbox.curselection()
    selected_song = int(selected_song[0])
    filename_path = playlist[selected_song]
    filename = os.path.basename(filename_path)
    title_label['text']="Now Playing "+filename
    file_data=os.path.splitext(filename_path)
    if file_data[1]=='.mp3':
        audio=MP3(filename_path)
        total_length=audio.info.length
    else:
        a=mixer.Sound(filename_path)
        total_length=a.get_length()
    mins,secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:02d}:{:02d}'.format(mins,secs)
    totaltime_label['text']=timeformat
    thread1=threading.Thread(target=get_current_duration,args=(total_length,))
    thread1.start()

def play_song():
    global filename_path,pause,play
    if pause:
        mixer.music.unpause()
    else:
        if listbox.curselection():
            selected_song = listbox.curselection()
            selected_song = int(selected_song[0])
            filename_path = playlist[selected_song]
            filename=os.path.basename(filename_path)
            mixer.music.load(filename_path)
            mixer.music.play()
            statusbar['text'] = "Now Playing "+filename
            pause=FALSE
            play = TRUE
            get_total_duration()
        else:
            tkinter.messagebox.showinfo("Music Player", "Please Select the song to play")

def pause_song():
    global pause
    mixer.music.pause()
    pause=TRUE
    statusbar['text'] = filename + " has been paused"

def stop_song():
    global pause
    mixer.music.stop()
    pause=FALSE
    totaltime_label['text'] = "00:00"
    statusbar['text'] = filename + " has been stopped"
    play=FALSE

def on_closing():
    if play:
        stop_song()
    root.destroy()

#program starts from here

root=tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
root.title("Music Player")
root.iconbitmap(r"res/musicicon.ico")
#------------------------------------------------status bar---------------------------------------------------------
statusbar=Label(root,text="Welcome to music player",relief=SUNKEN,anchor=W)
statusbar.pack(side=BOTTOM,fill=X)

#------------------------------------------------menubar  starts from here---------------------------------------------
menubar=Menu(root)
mixer.init()
root.config(menu=menubar)

# fot file menu
subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open",command=add_playlist)
subMenu.add_command(label="Exit",command=root.destroy)

#for help menu
subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us",command=about_us)

#------------------------------------------------------menubar ends  here---------------------------------------------

#-----------------------------------------------------left frame strats from here-----------------------------
frame_left=Frame(root)
frame_left.pack(padx=50,pady=100,side=LEFT)

info_label=ttk.Label(frame_left,text="Your Play List")
info_label.pack()

listbox=Listbox(frame_left)
listbox.pack()

add_button=ttk.Button(frame_left,text="Add",command=add_playlist)
add_button.pack(side=LEFT)

del_button=ttk.Button(frame_left,text="Del",command=del_playlist)
del_button.pack(side=LEFT)

#-----------------------------------------------------left frame ends here-----------------------------

#------------------------------------------------------right frame starts from here-----------------------
frame_right=Frame(root)
frame_right.pack(padx=20,pady=50)

title_label=ttk.Label(frame_right,text="Now Playing ")
title_label.grid(row=0,column=2)

currenttime_label=ttk.Label(frame_right,text="--:--")
currenttime_label.grid(row=2,column=0)

totaltime_label=ttk.Label(frame_right,text="--:--")
totaltime_label.grid(row=2,column=4)

#-------------------------------------------------------frame 2---------------------
down2_frame=Frame(root)
down2_frame.pack()

photo_play=PhotoImage(file="res\play.png")
play_button=ttk.Button(down2_frame,image=photo_play,command=play_song)
play_button.grid(row=0,column=0,padx=10)

photo_pause=PhotoImage(file="res\pause.png")
pause_button=ttk.Button(down2_frame,image=photo_pause,command=pause_song)
pause_button.grid(row=0,column=2,padx=10)

photo_stop=PhotoImage(file="res\stop.png")
stop_button=ttk.Button(down2_frame,image=photo_stop,command=stop_song)
stop_button.grid(row=0,column=4,padx=10)

#-----------------------------------------------------frame3-------------------------

down3_frame=Frame(root)
down3_frame.pack(padx=20,pady=30)

photo_rewind=PhotoImage(file="res\evind.png")
rewind_button=ttk.Button(down3_frame,image=photo_rewind,command=play_song)
rewind_button.pack(side=LEFT)

photo_repeatnone=PhotoImage(file="res\erepeatnone.png")
photo_repeatcurrent=PhotoImage(file="res\erepeatcurrent.png")
photo_repeatall=PhotoImage(file="res\erepeatall.png")
repeat_button=ttk.Button(down3_frame,image=photo_repeatnone,command=repeat_song)
repeat_button.pack(side=LEFT)

photo_mute=PhotoImage(file="res/mute.png")
photo_unmute=PhotoImage(file="res/unmute.png")
mute_button=ttk.Button(down3_frame,image=photo_mute,command=mute_song)
mute_button.pack(side=LEFT)

#using scale widget
scale=ttk.Scale(down3_frame,orient=HORIZONTAL ,from_=0 ,to=100,command=set_volume)
scale.set(70)
scale.pack(padx=10,pady=25)

#------------------------------------------------------right frame starts from here-----------------------
root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()