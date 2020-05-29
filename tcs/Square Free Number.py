#https://www.tcscodevita.com/CodevitaV8/samplequestion.jsp

print("Enter number")
num=int(input())

li_fact=[]
li_perfectSquare=[]
#finding factors
for i in range(2,num):
    if(num%i==0):

        #got the factorial in i
        #remove perfect square
        perfectSquare=0
        for j in range(2,i):
            if(j*j==i):
                perfectSquare=1
                li_perfectSquare.append(i)
                

        isDivisible=0
        #check if perfect sqare is divisible
        for j in range(0,len(li_perfectSquare)):
            if(i%li_perfectSquare[j]==0):
                isDivisible=1
                
        if(perfectSquare==0 and isDivisible==0):
            li_fact.append(i)

print(li_fact)
print(len(li_fact))
