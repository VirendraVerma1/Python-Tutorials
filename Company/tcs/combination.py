"""
input1=int(input())
input2=[]
for i in range(input1):
    input2.append(int(input()))
input3=int(input())
"""
input1=4
input2=[1,2,3]
input3=2

final=[]
final=input2.copy()
total=0
while(len(final)>1):
    input2=final.copy()
    final.clear()
    print(input2)
    for i in range(0,len(input2)-1,2):
        
        sum=0
        print(i,"-",i+1)
        print(input2[i],"-",input2[i+1])
        sum=input2[i]+input2[i+1]
        t=sum*input3
        total+=t
        final.append(sum)
        print("---------------")
    if(len(input2)%2==0):
        print("even")
    else:
        l=len(input2)-1
        final.append(input2[l])
    
print(final)
print(total)


