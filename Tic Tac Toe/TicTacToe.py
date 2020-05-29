from tkinter import *
import random
import tkinter.messagebox
import time
#---------------------------variables declaration---------------------------
player="x"
points=[]  #for storing button preesed on bord
tactics1=[]
player_points=[]
com_points=[]
flag=0
com_step=4
strat1=[1,2,3]
strat2=[1,4,7]
strat3=[1,5,9]
strat4=[2,5,8]
strat5=[3,6,9]
strat6=[3,5,7]
strat7=[4,5,6]
strat8=[7,8,9]
#----------------------------functions--------------------------------------
def new_game():
    global com_step,player
    player = "x"
    points.clear()
    tactics1.clear()
    player_points.clear()
    com_points.clear()
    flag = 0
    com_step = 4

    #reset game photo
    button_1.configure(image=photo_1)
    button_2.configure(image=photo_2)
    button_3.configure(image=photo_3)
    button_4.configure(image=photo_4)
    button_5.configure(image=photo_5)
    button_6.configure(image=photo_6)
    button_7.configure(image=photo_7)
    button_8.configure(image=photo_8)
    button_9.configure(image=photo_9)

def set_player_symbol_O():
    global player
    player = "o"
    print(id(player))

def button1():
    global flag,points
    flag = 0
    length=len(points)
    for i in range(0,length):
        if(points[i]==1):
            flag=1

    if(flag!=1):
        button_1.configure(image=photo_11)
        points.append(1)
        player_points.append(1)
        com()
    else:
        print(points)

def button2():
    global flag,points
    flag = 0
    length=len(points)
    for i in range(0,length):
        if(points[i]==2):
            flag=1

    if(flag!=1):
        button_2.configure(image=photo_12)
        points.append(2)
        player_points.append(2)
        com()
    else:
        print(points)

def button3():
    global flag,points
    flag = 0
    length=len(points)
    for i in range(0,length):
        if(points[i]==3):
            flag=1

    if(flag!=1):
        button_3.configure(image=photo_13)
        points.append(3)
        player_points.append(3)
        com()
    else:
        print(points)

def button4():
    global flag,points
    flag = 0
    length=len(points)
    for i in range(0,length):
        if(points[i]==4):
            flag=1

    if(flag!=1):
        button_4.configure(image=photo_14)
        points.append(4)
        player_points.append(4)
        com()
    else:
        print(points)

def button5():
    global flag,points
    flag = 0
    length=len(points)
    for i in range(0,length):
        if(points[i]==5):
            flag=1

    if(flag!=1):
        button_5.configure(image=photo_15)
        points.append(5)
        player_points.append(5)
        com()
    else:
        print(points)

def button6():
    global flag,points
    flag = 0
    length=len(points)
    for i in range(0,length):
        if(points[i]==6):
            flag=1

    if(flag!=1):
        button_6.configure(image=photo_16)
        points.append(6)
        player_points.append(6)
        com()
    else:
        print(points)

def button7():
    global flag,points
    flag = 0
    length=len(points)
    for i in range(0,length):
        if(points[i]==7):
            flag=1

    if(flag!=1):
        button_7.configure(image=photo_17)
        points.append(7)
        player_points.append(7)
        com()
    else:
        print(points)

def button8():
    global flag,points
    flag = 0
    length=len(points)
    for i in range(0,length):
        if(points[i]==8):
            flag=1

    if(flag!=1):
        button_8.configure(image=photo_18)
        points.append(8)
        player_points.append(8)
        com()
    else:
        print(points)

def button9():
    global flag,points
    flag = 0
    length=len(points)
    for i in range(0,length):
        if(points[i]==9):
            flag=1

    if(flag!=1):
        button_9.configure(image=photo_19)
        points.append(9)
        player_points.append(9)
        com()
    else:
        print(points)


def com():
    global points,com_step
    enable = 0


    # check if player wins
    length=len(player_points)
    flag=0

    for i in range(0,length):
        if(1 in player_points and 2 in player_points and 3 in  player_points):
            flag=1
        if (1 in player_points and 4 in player_points and 7 in player_points):
            flag = 1
        if (1 in player_points and 5 in player_points and 9 in player_points):
            flag = 1
        if (3 in player_points and 5 in player_points and 7 in player_points):
            flag = 1
        if (2 in player_points and 5 in player_points and 8 in player_points):
            flag = 1
        if (3 in player_points and 6 in player_points and 9 in player_points):
            flag = 1
        if (4 in player_points and 5 in player_points and 6 in player_points):
            flag = 1
        if (7 in player_points and 8 in player_points and 9 in player_points):
            flag = 1
    if(flag==1):
        tkinter.messagebox.showinfo("Tic Tac Toe", "You Won")
        time.sleep(2)
        new_game()
        enable=1

    #do com step

    # get random number
    n = 1
    random_value_copy=0
    random_value=0
    while (n > 0 and com_step != 0 and enable == 0):
        random_value = random.randint(1, 9)
        length = len(points)
        flag = 0
        for i in range(0, length):
            if (random_value == points[i]):
                flag = 1

        if (flag != 1):
            n = 0
    random_value_copy=random_value

    #check for player and make decesion
    temp=0
    length=len(player_points)
    for i in range(0,length):

        # now going for offence

        # -------1 strat------
        counter = 0
        for j in range(0, len(strat1)):
            if (strat1[j] in com_points):
                counter = counter + 1
            else:
                if (strat1[j] in points):
                    temp = 0
                else:
                    temp = strat1[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----2 strat
        counter = 0
        for j in range(0, len(strat2)):
            if (strat2[j] in com_points):
                counter = counter + 1
            else:
                if (strat2[j] in points):
                    temp = 0
                else:
                    temp = strat2[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----3 strat
        counter = 0
        for j in range(0, len(strat3)):
            if (strat3[j] in com_points):
                counter = counter + 1
            else:
                if (strat3[j] in points):
                    temp = 0
                else:
                    temp = strat3[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----4 strat
        counter = 0
        for j in range(0, len(strat4)):
            if (strat4[j] in com_points):
                counter = counter + 1
            else:
                if (strat4[j] in points):
                    temp = 0
                else:
                    temp = strat4[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----5 strat
        counter = 0
        for j in range(0, len(strat5)):
            if (strat5[j] in com_points):
                counter = counter + 1
            else:
                if (strat5[j] in points):
                    temp = 0
                else:
                    temp = strat5[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----6 strat
        counter = 0
        for j in range(0, len(strat6)):
            if (strat6[j] in com_points):
                counter = counter + 1
            else:
                if (strat6[j] in points):
                    temp = 0
                else:
                    temp = strat6[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----7 strat
        counter = 0
        for j in range(0, len(strat7)):
            if (strat7[j] in com_points):
                counter = counter + 1
            else:
                if (strat7[j] in points):
                    temp = 0
                else:
                    temp = strat7[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break
        # ----8 strat
        counter = 0
        for j in range(0, len(strat8)):
            if (strat8[j] in com_points):
                counter = counter + 1
            else:
                if (strat8[j] in points):
                    temp = 0
                else:
                    temp = strat8[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break


        #-----checking for defensive
        #-------1 strat------
        counter = 0
        for j in range(0,len(strat1)):
            if(strat1[j] in player_points):
                counter=counter+1
            else:
                if (strat1[j] in points):
                    temp = 0
                else:
                    temp = strat1[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        #----2 strat
        counter = 0
        for j in range(0, len(strat2)):
            if (strat2[j] in player_points):
                counter = counter + 1
            else:
                if (strat2[j] in points):
                    temp = 0
                else:
                    temp = strat2[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----3 strat
        counter = 0
        for j in range(0, len(strat3)):
            if (strat3[j] in player_points):
                counter = counter + 1
            else:
                if (strat3[j] in points):
                    temp = 0
                else:
                    temp = strat3[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----4 strat
        counter = 0
        for j in range(0, len(strat4)):
            if (strat4[j] in player_points):
                counter = counter + 1
            else:
                if (strat4[j] in points):
                    temp = 0
                else:
                    temp = strat4[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----5 strat
        counter = 0
        for j in range(0, len(strat5)):
            if (strat5[j] in player_points):
                counter = counter + 1
            else:
                if (strat5[j] in points):
                    temp = 0
                else:
                    temp = strat5[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----6 strat
        counter = 0
        for j in range(0, len(strat6)):
            if (strat6[j] in player_points):
                counter = counter + 1
            else:
                if (strat6[j] in points):
                    temp = 0
                else:
                    temp = strat6[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----7 strat
        counter = 0
        for j in range(0, len(strat7)):
            if (strat7[j] in player_points):
                counter = counter + 1
            else:
                if (strat7[j] in points):
                    temp = 0
                else:
                    temp = strat7[j]
        if (counter == 2 and temp != 0):
            random_value_copy = temp
            break

        # ----8 strat
        counter = 0
        for j in range(0, len(strat8)):
            if (strat8[j] in player_points):
                counter = counter + 1
            else:
                if(strat8[j] in points):
                    temp=0
                else:
                    temp = strat8[j]
        if (counter == 2 and temp !=0):
            random_value_copy = temp
            break





    if(random_value_copy):
        random_value=random_value_copy


    if(com_step!=0 and enable==0):
        points.append(random_value)
        com_points.append(random_value)
        com_step =com_step-1
        if(random_value==1):
            button_1.configure(image=photo_21)
        elif(random_value==2):
            button_2.configure(image=photo_22)
        elif (random_value == 3):
            button_3.configure(image=photo_23)
        elif (random_value == 4):
            button_4.configure(image=photo_24)
        elif (random_value == 5):
            button_5.configure(image=photo_25)
        elif (random_value == 6):
            button_6.configure(image=photo_26)
        elif (random_value == 7):
            button_7.configure(image=photo_27)
        elif (random_value == 8):
            button_8.configure(image=photo_28)
        elif (random_value == 9):
            button_9.configure(image=photo_29)

    # check if com wins
    length = len(com_points)
    flag = 0
    enable = 0
    for i in range(0, length):
        if (1 in com_points and 2 in com_points and 3 in com_points):
            flag = 1
        if (1 in com_points and 4 in com_points and 7 in com_points):
             flag = 1
        if (1 in com_points and 5 in com_points and 9 in com_points):
            flag = 1
        if (3 in com_points and 5 in com_points and 7 in com_points):
            flag = 1
        if (2 in com_points and 5 in com_points and 8 in com_points):
            flag = 1
        if (3 in com_points and 6 in com_points and 9 in com_points):
            flag = 1
        if (4 in com_points and 5 in com_points and 6 in com_points):
            flag = 1
        if (7 in com_points and 8 in com_points and 9 in com_points):
            flag = 1
    if (flag == 1):
        tkinter.messagebox.showinfo("Tic Tac Toe", "You Lose")
        time.sleep(2)
        new_game()
        enable = 1


    #check if all points completed
    if(len(points)==9):
        tkinter.messagebox.showinfo("Tic Tac Toe", "Match Draw")
        time.sleep(2)
        new_game()


#            program starts from here
#---------------------initialization---------------------------
root=Tk()
root.title("Tic Tac Toe")
root.iconbitmap(r"res/tictaktoe.ico")
root.configure(background='black')

menubar=Menu(root)
root.config(menu=menubar)

# fot new menu
subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Game",menu=subMenu)
subMenu.add_command(label="New",command=new_game)
subMenu.add_command(label="Resume")
subMenu.add_command(label="Exit",command=root.destroy)

#for player menu
subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Player",menu=subMenu)
subMenu.add_command(label="Set X")
subMenu.add_command(label="Set O",command=set_player_symbol_O)


frame=Frame(root)
frame.pack()
frame.configure(background='black')
title_label=Label(frame,text="TIC TAC TOE")
title_label.pack()

#game start
game_frame=Frame(root)
game_frame.pack()
game_frame.configure(background='black')

j=1
k=1
"""
for i in range(0, 9):
    if(k==4):
        j=j+1
        k=1
    #  button

    button_i=Button(game_frame,text=" ",command=lambda: button(i),width=20,height=10)
    button_i.grid(row=(j+2),column=(k+2),padx=2)
    k = k + 1
"""

#-----------button 1-------------
photo_1=PhotoImage(file="res\Blank1.png")
if(player=="x"):
    photo_11 = PhotoImage(file="res\XOne.png")
else:
    photo_11 = PhotoImage(file="res\OOne.png")
photo_21 = PhotoImage(file="res\O1.png")
button_1=Button(game_frame,image=photo_1,command=button1)
button_1.grid(row=2,column=2,padx=10)
#-----------button 2-------------
photo_2=PhotoImage(file="res\Blank2.png")
photo_12 = PhotoImage(file="res\XTwo.png")
photo_22 = PhotoImage(file="res\O2.png")
button_2=Button(game_frame,image=photo_2,command= button2)
button_2.grid(row=2,column=3,padx=10)
#-----------button 3-------------
photo_3=PhotoImage(file="res\Blank3.png")
photo_13 = PhotoImage(file="res\XThree.png")
photo_23 = PhotoImage(file="res\O3.png")
button_3=Button(game_frame,image=photo_3,command=button3)
button_3.grid(row=2,column=4,padx=10)

#-----------button 4-------------
photo_4=PhotoImage(file="res\Blank4.png")
photo_14 = PhotoImage(file="res\XFour.png")
photo_24 = PhotoImage(file="res\O4.png")
button_4=Button(game_frame,image=photo_4,command=button4)
button_4.grid(row=3,column=2,padx=10)
#-----------button 5-------------
photo_5=PhotoImage(file="res\Blank5.png")
photo_15 = PhotoImage(file="res\XFive.png")
photo_25 = PhotoImage(file="res\O5.png")
button_5=Button(game_frame,image=photo_5,command= button5)
button_5.grid(row=3,column=3,padx=10)
#-----------button 6-------------
photo_6=PhotoImage(file="res\Blank6.png")
photo_16 = PhotoImage(file="res\XSix.png")
photo_26 = PhotoImage(file="res\O6.png")
button_6=Button(game_frame,image=photo_6,command= button6)
button_6.grid(row=3,column=4,padx=10)

#-----------button 7-------------
photo_7=PhotoImage(file="res\Blank7.png")
photo_17 = PhotoImage(file="res\XSeven.png")
photo_27 = PhotoImage(file="res\O7.png")
button_7=Button(game_frame,image=photo_7,command=button7)
button_7.grid(row=4,column=2,padx=10)
#-----------button 8-------------
photo_8=PhotoImage(file="res\Blank8.png")
photo_18 = PhotoImage(file="res\XEight.png")
photo_28 = PhotoImage(file="res\O8.png")
button_8=Button(game_frame,image=photo_8,command= button8)
button_8.grid(row=4,column=3,padx=10)
#-----------button 9-------------
photo_9=PhotoImage(file="res\Blank9.png")
photo_19 = PhotoImage(file="res\XNine.png")
photo_29 = PhotoImage(file="res\O9.png")
button_9=Button(game_frame,image=photo_9,command=button9)
button_9.grid(row=4,column=4,padx=10)

root.mainloop()
