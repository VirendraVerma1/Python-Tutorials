from tkinter import *
import threading
import sys
root=Tk()

frame = Frame(root)
root.title('GUI Test1')
frame.pack()

label=Label(frame,text="Welecome to Python GUI")
label.pack()
def stop_file():
    root.destroy()

def test2_open():
    import test2

def open_file():
    
    # creating thread 
    t1 = threading.Thread(target=stop_file) 
    t2 = threading.Thread(target=test2_open) 
    stop_file()
    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start() 
    # wait until thread 1 is completely executed 
    t1.join() 
    # wait until thread 2 is completely executed 
    t2.join() 
    
button=Button(frame,text="Hello",command = open_file)
button.pack(padx=10,pady=10)


root.minsize(500,500)
root.mainloop()

