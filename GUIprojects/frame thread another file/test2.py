from tkinter import *

counter = 0 
def counter_label(label):
  counter = 0
  def count():
    global counter
    counter += 1
    label.config(text=str(counter))
    label.after(1000, count)
  count()
 
 
root = Tk()
root.title('GUI Counter')
root.title("Counting Seconds")
label = Label(root, fg="dark green")
label.pack()
counter_label(label)
button = Button(root, text='Stop', width=25, command=root.destroy)
button.pack()


root.mainloop()
