import math


#a=int(input("Enter number of points = "))
#di={}
#for i in range(0,a):
#    print("Point "+str(i))
#    di[i]={}
#    di[i]['x']=int(input("Enter x coordinate of "+str(i)+" = "))
#    di[i]['y']=int(input("Enter y coordinate of "+str(i)+" = "))
#    di[i]['z']=int(input("Enter z coordinate of "+str(i)+" = "))

a=3
di={}
di[0]={}
di[1]={}
di[2]={}
di[0]['x']=1
di[0]['y']=1
di[0]['z']=10
di[1]['x']=2
di[1]['y']=1
di[1]['z']=10
di[2]['x']=0
di[2]['y']=1
di[2]['z']=9

x=0
y=0
z=0
distancex=pow((di[2]['x']-di[1]['x']),2)
distancey=pow((di[2]['y']-di[1]['y']),2)
distancez=pow((di[2]['z']-di[1]['z']),2)
print(math.sqrt(distancex+distancey+distancez))
#for i in range(0,a):
    
