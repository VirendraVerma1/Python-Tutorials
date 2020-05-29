import tkinter
from tkinter import *
root = Tk()
root.geometry("500x500")
root.title("Insert title")
root.configure(background='#CCCCFF')

for i in range(10):
    Frame(root, width=20, height=20, background='#CCCCFF').grid(row=0, column=i)

for j in range(10):
    Frame(root, width=20, height=20, background='#CCCCFF').grid(column=0, row=j)

label1 = Label(root, text = "Insert title", font = ("Rockwell", 12))
label2 = Label(root, text = "Name", font = ("Rockwell", 25))
label1.configure(background='#CCCCFF')
label2.configure(background = '#CCCCFF')
label1.grid(row = 8, column = 3)
label2.grid(row = 9, column = 3)
root.mainloop()
