#https://www.tcscodevita.com/CodevitaV8/samplequestion.jsp

print("Enter a number")
num=int(input())

li=[]
sum=0
for i in range(0,num):
    n=int(input())

    num_Pow=pow(2,n)
    a=0
    if(len(str(num_Pow))>2):
        s=str(num_Pow)
        ss=s[len(str(num_Pow))-2:]
        a=int(ss)
    else:
        a=num_Pow
    
    sum=sum+a

print(sum)
print(sum%100)
