li=[4,5,6,1,2,7,8,9]
w=3

addCount=0
sum=0
counter=0
s=0
for i in range(0,len(li)):
    counter+=1
    addCount+=1
    if(addCount<4):
        print(li[i])
        sum+=li[i]
    elif(addCount==4):
        print(li[i])
        print("dasd")
        pass
    else:
        s=0
        print("Lent rest",len(li)-counter)
        h=len(li)-counter
        if(h==3):
            s+=li[counter]
            s+=li[counter+1]
            s+=li[counter+2]
            if(li[i]>=s):
                sum+=s
                print("break")
                break
            else:
                print("reset")
                addCount=0
                continue
        else:
            sum+=li[i]
            
    
        
    
print(sum)

print("Second method")

li=[4,5,6,1,2,3,7,8,9]
w=3

addCount=0
sum=0
counter=0
s=0
i=0
while(len(li)>i):
    print(li[i])
    le=(len(li)-counter)
    if(le>3):
        print("Length",le-1)
        if( (le-1)!=4):
            print("asdf")
            s1=li[i]+li[i+1]+li[i+2]
            s2=li[i+1]+li[i+2]+li[i+3]
            if(s1>=s2):
                sum+=s1
                i+=3
                counter+=3
            else:
                sum+=s2
                i=i+4
                counter+=4
        else:
            print("suma")
            sum+=li[i]
        print("sum",sum)
        print("-----------------------")
    else:
        counter+=1
        print("skipped",le)
    
    i+=1
print(sum)
