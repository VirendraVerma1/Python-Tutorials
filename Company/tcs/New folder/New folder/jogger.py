
li=[10,25,50,75]
deg=[0,0,0,0]
speed=[1,2,3,4]
rot=[0,0,0,0]
time=90

import math
"""li = list(map(int,input().strip().split()))
deg = list(map(int,input().strip().split()))
speed = list(map(int,input().strip().split()))
rot = list(map(int,input().strip().split()))
time = int(input())"""



newangle=[]
#calculating time
for i in range(0,len(deg)):
    t=0
    if(rot[i]==1):
        t=speed[i]*time

    else:
        t=360-(speed[i]*time)

    newangle.append(t)

#print(newangle)
dis=0.0
radius=li[0]
li[0]=0
for i in range(0,len(deg)-1):
    #print(li[i+1],li[i],li[i+1]-li[i])
    if(newangle[i]==newangle[i+1]):
        dis+=li[i+1]-li[i]
    
    #when new angle on 0
    elif(newangle[i]==0 and newangle[i+1]==180):
        #print("0 180")
        dis+=li[i+1]-li[i]-radius*2
    elif(newangle[i]==0 and newangle[i+1]==90):
        #print("0 90")
        dis+=math.sqrt(math.pow((li[i+1]-li[i]-radius),2)+radius*radius)
    elif(newangle[i]==0 and newangle[i+1]==270):
        #print("0 270")
        dis+=math.sqrt(math.pow((li[i+1]-li[i]-radius),2)+radius*radius)
    elif(newangle[i]==0 and newangle[i+1]==0):
        #print("0 0")
        dis+=li[i+1]-li[i]

    #when new angle on 270
    elif(newangle[i]==270 and newangle[i+1]==180):
        #print("270 180")
        dis+=math.sqrt(math.pow((li[i+1]-li[i]-radius),2)+radius*radius)
    elif(newangle[i]==270 and newangle[i+1]==90):
        #print("270 90")
        dis+=math.sqrt(math.pow(float((li[i+1]-li[i])/2),2)+radius*radius)*2
    elif(newangle[i]==270 and newangle[i+1]==270):
        #print("270 270")
        dis+=li[i+1]-li[i]
    elif(newangle[i]==270 and newangle[i+1]==0):
        #print("270 0")
        dis+=math.sqrt(math.pow((li[i+1]-li[i]+radius),2)+radius*radius)
    
    #when new angle on 180
    elif(newangle[i]==180 and newangle[i+1]==180):
        #print("180 0")
        dis+=li[i+1]-li[i]
    elif(newangle[i]==180 and newangle[i+1]==90):
        #print("180 90")
        dis+=math.sqrt(math.pow((li[i+1]-li[i]+radius),2)+radius*radius)
    elif(newangle[i]==180 and newangle[i+1]==270):
        #print("180 270")
        dis+=math.sqrt(math.pow((li[i+1]-li[i]+radius),2)+radius*radius)
    elif(newangle[i]==180 and newangle[i+1]==0):
        #print("180 0")
        dis+=li[i+1]-li[i]+radius*2

    #when new angle on 90
    elif(newangle[i]==90 and newangle[i+1]==180):
        #print("90 180")
        dis+=math.sqrt(math.pow((li[i+1]-li[i]-radius),2)+radius*radius)
    elif(newangle[i]==90 and newangle[i+1]==90):
        #print("90 90")
        dis+=li[i+1]-li[i]
    elif(newangle[i]==90 and newangle[i+1]==270):
        #print("90 270")
        dis+=math.sqrt(math.pow(float((li[i+1]-li[i])/2),2)+radius*radius)*2
    elif(newangle[i]==90 and newangle[i+1]==0):
        #print("90 0")
        dis+=math.sqrt(math.pow((li[i+1]-li[i]+radius),2)+radius*radius)

print(round(dis))
