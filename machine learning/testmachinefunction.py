from tkinter import *

#variable initialization
files=[]
temp_names=[]
label_points=[]
d=0

#functions--area-------------------------
def plot():
    print("save")
    label_points.configure(text='s').grid(row=3,column=23)
# -------------initialization section-----------------------
root=Tk()
root.title("Machine learning functions")

#----frame 1 or input frame--------
frame1=Frame(root)
frame1.pack()

name_label=Label(frame1,text="Supervised machine learning")
name_label.grid(row=0,column=1)

label_coordinate=Label(frame1,text="Enter Coordinates ")
label_coordinate.grid(row=1,column=1)

label_xcoordinate=Label(frame1,text="X:")
label_xcoordinate.grid(row=1,column=2)

input_x_coordinates=Entry(frame1)
input_x_coordinates.grid(row=1,column=3)

label_ycoordinate=Label(frame1,text="Y:")
label_ycoordinate.grid(row=1,column=4)

input_y_coordinates=Entry(frame1)
input_y_coordinates.grid(row=1,column=5)


label_labelcoordinate=Label(frame1,text="Label:")
label_labelcoordinate.grid(row=1,column=6)

input_label_coordinates=Entry(frame1)
input_label_coordinates.grid(row=1,column=7)

enter_coordinate_button=Button(frame1,text="Save",command=plot)
enter_coordinate_button.grid(row=1,column=8)

#-----frame 2 or graph frame--------
frame2=Frame(root)
frame2.pack()

for i in range(1,25):
    for j in range(1,50):
        files.append("Button" + str(i) + str(i))
        temp_names.append(d)
        label_points.append(Label(frame2,text=".",width=1,height=1))
        label_points[d].grid(row=i,column=j)
        d=d+1



root.mainloop()
