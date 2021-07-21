
total=int(input("Total numeber "))
pos=int(input("Get Position "))
li=[]
for i in range(0,total):
    n=int(input("Number "))
    li.append(n)
"""
total=6
pos=3
li=[]
li.append(30)

li.append(20)
li.append(40)
li.append(80)
li.append(70)
li.append(60)
"""
li_copy=li
min=min(li)
minIndex=li.index(min)
max=max(li)
maxIndex=li.index(max)

lifinal=li_copy.copy()
lifinal.sort()
length=len(li)

lifinal.insert(pos-1,max)
lifinal.pop()

weight=0
small=0
nonsmall=0
j=10
print(lifinal)
print(li)
t=1
print("--------------------------------")

if(li[pos-1]!=max and li[pos-1]<max):
    print("Change Max")
    #means it has to interchange
    #check for smaller weight
    small=li[pos-1]
    nonsmall=li[maxIndex]
    if(small>li[maxIndex]):
        small=li[maxIndex]
        nonsmall=li[pos-1]
                  
    if(((small*min)*2+nonsmall*min)<(li[pos-1]*li[maxIndex])):
        #means it has to interchange wile using smallest value
        weight=weight+((small*min)*2+nonsmall*min)
        temp=li[pos-1]
        li[pos-1]=li[maxIndex]
        li[maxIndex]=temp
        print("Test1="+str((small*min)*2+nonsmall*min))
    else:
        weight=weight+li[pos-1]*li[maxIndex]
        temp=li[pos-1]
        li[pos-1]=li[maxIndex]
        li[maxIndex]=temp
        print("Test2="+str((li[pos-1]*li[maxIndex])))
    #i=i+1
    print(li)
    print("changed = "+str(weight) )
                                    
              
while(j>0):
    j=j-1
    t=1
    for i in range(0,length-1):
        if(li[i]>li[i+1]):
            
            if(li[i]!=max and li[i+1]!=max):
                t=1
                
                #means it has to interchange
                #check for smaller weight
                small=li[i]
                nonsmall=li[i+t]
                if(small>li[i+t]):
                    small=li[i+t]
                    nonsmall=li[i]
                  
                if(((small*min)*2+nonsmall*min)<(li[i]*li[i+t])):
                    #means it has to interchange wile using smallest value
                    weight=weight+((small*min)*2+nonsmall*min)
                    temp=li[i]
                    li[i]=li[i+t]
                    li[i+t]=temp
                    print("Test1="+str((small*min)*2+nonsmall*min))
                else:
                    weight=weight+li[i]*li[i+t]
                    temp=li[i]
                    li[i]=li[i+t]
                    li[i+t]=temp
                    print("Test2="+str((li[i]*li[i+t])))
                #i=i+1
                print(li)
                print("Done = "+str(weight))
            
            
print("????????????????????????????")
print(lifinal)
print(li)
print(weight)


"""elif(t+2<length-2):
                t=2
                print(i)
                #means it has to interchange
                #check for smaller weight
                small=li[i]
                nonsmall=li[i+t]
                if(small>li[i+t]):
                    small=li[i+t]
                    nonsmall=li[i]
                  
                if(((small*min)*2+nonsmall*min)<(li[i]*li[i+t])):
                    #means it has to interchange wile using smallest value
                    weight=weight+((small*min)*2+nonsmall*min)
                    temp=li[i]
                    li[i]=li[i+t]
                    li[i+t]=temp
                    print("Test1="+str((small*min)*2+nonsmall*min))
                else:
                    weight=weight+li[i]*li[i+t]
                    temp=li[i]
                    li[i]=li[i+t]
                    li[i+t]=temp
                    print("Test2="+str((li[i]*li[i+t])))
                #i=i+1
                print(li)
                print("Done = "+str(weight))
            """
