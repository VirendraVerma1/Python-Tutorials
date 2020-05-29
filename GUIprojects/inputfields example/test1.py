import tkinter
from tkinter import *

#functions
def get_data():
    Label(master,text="First Name =").grid(row=4,column=0)
    Label(master,text=str(if_fn.get())).grid(row=4,column=1)
    Label(master,text="Last Name =").grid(row=5,column=0)
    Label(master,text=str(if_ln.get())).grid(row=5,column=1)

master=Tk()
master.title('Input example')

Label(master,text="Form Page",fg = "light green",
		 bg = "dark green",
		 font = "Helvetica 16 bold italic",justify=LEFT,
          compound = LEFT,
          padx = 10).grid(row=0)


name_label=Label(master,text="First Name :").grid(row=1) 

lastname_label=Label(master,text="Last Name :").grid(row=2)
if_fn=Entry(master)
if_fn.grid(row=1,column=1)
if_ln=Entry(master)
if_ln.grid(row=2,column=1)

button=Button(master,text="OK",command=get_data).grid(row=3,column=1, padx=10,pady=10)


master.mainloop()
