#https://www.faceprep.in/tcs/tcs-codevita-questions/

a=1
b=int(input("Enter Number Of Boxes"))

li=[]
for i in range(0,b):
    li.append(int(input("Num ")))

time=-1
sum=0
for i in range(0,b):
    sum=sum+li[i]
    time=time+sum

print(time)
