from tkinter import *
import time
root=Tk()
root.title("Image test 1")

frame=Frame(root)
frame.pack()

canvas=Canvas(root,width=800,height=800)
canvas.pack()

img=PhotoImage(file="a.png")
x=100
rc1=canvas.create_image(20,100,anchor=NW,image=img)
for x in range(100):
    
    time.sleep(.1)
    canvas.move(rc1, x,20)
    canvas.update()
root.mainloop()
