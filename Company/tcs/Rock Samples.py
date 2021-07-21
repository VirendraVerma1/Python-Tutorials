#https://www.faceprep.in/tcs/tcs-codevita-questions/

#get input
li=[]
a=input("Enter Input ")
li=a.split(' ')
print(int(li[0]))
print(int(li[1]))

#get rock list
rocksList=[]
b=input("Enter Rocks ")
rocksList=b.split(' ')

ranges=[]
rangesCounter=[]
for i in range(0,int(li[1])):
    c=input("Enter range ")
    new_range=[]
    new_range=c.split(' ')
    ranges.append(new_range)

    counter=0
    for j in range(0,len(rocksList)):
        
        if(int(ranges[i][0]) <= int(rocksList[j]) and int(ranges[i][1]) >= int(rocksList[j])):
            print(rocksList[j])
            counter=counter+1
    print("-------------")
    rangesCounter.append(counter)
print(rangesCounter)
