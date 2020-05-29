from tkinter import *
import time
import threading
import math

#variable initialization area-----------------------------------------------
files = [] #creates list to replace your actual inputs for troubleshooting purposes
button = [] #creates list to store the buttons ins
temp_names=[]#storing button id to identify
d=0
start_point=0
final_point=0
travel=0
distance_from_player_points=[]
distance_point_name=[]

#function area--------------------------------------------------------------

def set_player():
    global start_point
    button[0].configure(text="P")
    start_point=0
    statusbar['text']="set final destination point"

def button_pressed(i):
    global final_point,travel
    if(final_point==0):
        #travel=0
        button[i].configure(text="#")
        final_point=i
        statusbar['text'] = "final point set"
    else:
        #travel=0
        button[final_point].configure(text=".")
        button[i].configure(text="#")
        final_point = i
        statusbar['text'] = "new final point has been set"

def stop_travel():
    global travel
    travel=0
    statusbar['text'] = "travel has been stopped"

def start_travel():
    global final_point,travel
    if(final_point>=1):
        travel=1
        statusbar['text'] = "travelling..."
        thread1 = threading.Thread(target=travel_path, name='thread1')
        thread1.start()
    else:
        statusbar['text'] = "please set destination point"



def travel_path():
    global travel,final_point,start_point,distance_from_player_points,distance_point_name
    player_row=0
    player_column=0
    adjacent_points=[]
    distance_from_adjacent=[]
    #travel starts
    while(travel):
        c=0
        #get points
        for i in range(0,len(button)):
            if(button[i].cget("text")=="P"):
                #get player row and column
                player_row = button[i].grid_info()['row']
                player_column = button[i].grid_info()['column']
            if (button[i].cget("text") == "#"):
                # get player row and column
                final_row = button[i].grid_info()['row']
                final_column = button[i].grid_info()['column']

        #storing distance from player
        for i in range(0, len(button)):
            if(button[i].cget("text")!="P" and button[i].cget("text") != "#"):
                #get and store all distance
                row = button[i].grid_info()['row']
                column = button[i].grid_info()['column']
                distance_from_player_points.append(math.sqrt((row - player_row) ** 2 + (column - player_column) ** 2))
                distance_point_name.append(i)

        #getting distance from destination to player
        distance=math.sqrt((final_row-player_row)**2+(final_column-player_column)**2)


        #sorting distance_from_player_points
        n=len(distance_from_player_points)
        for i in range(n):
            for j in range(0, n - i - 1):
                if distance_from_player_points[j] > distance_from_player_points[j + 1]:
                    distance_from_player_points[j], distance_from_player_points[j + 1] = distance_from_player_points[j + 1], distance_from_player_points[j]
                    distance_point_name[j], distance_point_name[j + 1] = distance_point_name[j + 1], distance_point_name[j]

        #storing adjacent points in an array
        for i in range(4):
            id=distance_point_name[i]
            row = button[id].grid_info()['row']
            column = button[id].grid_info()['column']
            adjacent_points.append(distance_point_name[i])
            distance_from_adjacent.append(math.sqrt((final_row - row) ** 2 + (final_column-column) ** 2))

            # sorting distance_from_adjacent
            n = len(distance_from_adjacent)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if distance_from_adjacent[j] > distance_from_adjacent[j + 1]:
                        distance_from_adjacent[j], distance_from_adjacent[j + 1] = distance_from_adjacent[j + 1], distance_from_adjacent[j]
                        adjacent_points[j], adjacent_points[j + 1] = adjacent_points[j + 1],adjacent_points[j]

        print(distance_point_name)
        print(distance_from_player_points)
        print(distance_from_adjacent)
        print(adjacent_points)
        print(distance)
        #replace from minimul position
        temp_start_point=adjacent_points[0]
        button[temp_start_point].configure(text="P")
        button[start_point].configure(text=".")
        start_point=temp_start_point
        print(start_point)

        #check if reach to destination or not
        if(distance==1):
            button[start_point].configure(text=".")
            button[final_point].configure(text="P")
            start_point=final_point
            travel=0

        #clearing all array
        distance_from_adjacent.clear()
        adjacent_points.clear()
        distance_from_player_points.clear()
        distance_point_name.clear()

        #time.sleep(.001)

#initialization area-----starts--------------------------------------------------
root=Tk()
root.title("Pathfinder")

top_frame=Frame(root)
top_frame.pack()

name_label=Label(top_frame,text="Pathfinder")
name_label.grid(row=0,column=0)

set_player_button=Button(top_frame,text="Set Player",command=set_player)
set_player_button.grid(row=0,column=1)

start_button=Button(top_frame,text="Start",command=start_travel)
start_button.grid(row=0,column=3)

stop_button=Button(top_frame,text="Stop",command=stop_travel)
stop_button.grid(row=0,column=5)

#status bar
statusbar=Label(root,text="Welcome to Pathfinder",relief=SUNKEN,anchor=W)
statusbar.pack(side=BOTTOM,fill=X)
#---status bar ends

#frame starts from here
frame=Frame(root)
frame.pack()

for i in range(1,20):
    for j in range(1,50):
        files.append("Button" + str(i) + str(i))
        temp_names.append(d)
        button.append(Button(frame,text=".",width=1,height=1,command=lambda c=d: button_pressed(temp_names[c])))
        button[d].grid(row=i,column=j)
        d=d+1



#initialization area ------ends--------------------------------------------------




root.mainloop()
