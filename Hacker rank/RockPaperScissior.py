#https://www.hackerrank.com/contests/all-india-contest-by-coding-club-india-30-may-2020/challenges/rock-paper-scissor-3-2/problem
n=int(input())
li=[]
copy=[]
for i in range(n*3):
    h=[]
    t=[]
    a,b=map(str,input().split())
    h.append(a)
    h.append(b)
    t.append(0)
    t.append(0)
    copy.append(t)
    li.append(h)

for i in range(len(li)):
    a=li[i][0]
    b=li[i][1]
    for j in range(len(li)):
        for k in range(2):
            if(a==li[j][k]):
                copy[j][k]=copy[j][k]+1
            if(b==li[j][k]):
                copy[j][k]=copy[j][k]-1
 
for i in range(len(copy)):
    flag=0
    if(not copy[i][0]==0 and not copy[i][0]==0):
        flag=flag+1
        
if(flag==0):
    print("Valid")
else:
    print("Invalid")
