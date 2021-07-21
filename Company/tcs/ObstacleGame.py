#https://www.tcscodevita.com/CodevitaV8/samplequestion.jsp

#num=int(input())

#GETTING INPUT
"""
li=[]
for i in range(0,num):
    print("Array")
    l=[]
    for j in range(0,num):
        n=str(input())
        l.append(n)
    li.append(l)
"""

num=4
li=[['A','S','L','D'],['T','R','W','R'],['R','M','S','R'],['W','R','R','M']]

    
t=1
x=0
y=0
current_x=0
current_y=0

obstacle=['S','T','W','L']
Route_x=0
Route_y=0

while(t>0):
    arountObstacle=[]
    #get next route
    for i in range(-1,2):
        for j in range(-1,2):
            x=i
            y=j
            if((current_x+x>=0 and current_x-x<num)and(current_y+y>=0 and current_y-y<num)):
                print("In Range")
                print(li[x][y])
                
                for k in range(0,len(obstacle)):
                    if(li[x][y]==obstacle[k]):
                        arountObstacle.append(li[x][y])

                if(li[x][y]=='R'):
                    Route_x=x
                    Route_y=y
                    
                    #print(li[x][y])

            
            
                
    current_x=Route_x
    current_y=Route_y
    print(current_x)
    print(current_y)
    print("Current Position")
    print(li[current_x][current_y])
    print(arountObstacle)
    input()
