a=int(input("Enter Range "))

li=[]

primeCounter=0;

for i in range(0,a):
    
    #prime number
    counter=0
    for j in range(1,i):
        if(i%j==0):
            counter=counter+1


            
    if(counter==1):
        #add all previous prime number and check
        li.append(i)
        sum=0
        composite=0
        for j in range(0,len(li)):
            if(sum<i):
                sum=sum+li[j]
                composite=composite+1
           
        if(sum==i and composite>1):
            primeCounter=primeCounter+1
            print(i)
    
print("-------------")
print(primeCounter)

    
    
    
