n=int(input())
s=input()


li1=[]


lise1=[]
for i in range(0,n):
    if(s[i]=='A'):
        t=0
        j=i-1
        if(j>=0):
            for j in range(i-1,0,-1):
                if(s[j]=='-'):
                    li1.append(t)
                elif(s[j]=='A' or s[j]=='B'):
                    li1.append(99)
                    break
                else:
                    li1.append(99)
                t=t+1
    elif(s[i]=='B'):
        t=0
        j=i+1
        if(j<n):
            for j in range(i+1,n):
                if(s[j]=='-'):
                    lise1.append(t)
                elif(s[j]=='B' or s[j]=='A'):
                    lise1.append(99)
                    break
                else:
                    lise1.append(99)
                t+=1
    else:
        li1.append(99)
        lise1.append(99)
a=0
b=0
#print(n,len(li1))
counter=0
for i in range(0,n):
    

    if(s[i]=='A'):
        a+=1
    elif(s[i]=='B'):
        b+=1

    if(s[i]=='-'):
        print(counter)
        x=li1[i]
        y=lise1[i]
        if(x>y):
            b+=1
        elif(x<y):
            a+=1
        counter+=1

if(a>b):
    print("A")
elif(b>a):
    print("B")
else:
    print("Coalition government")
