#https://www.hackerrank.com/challenges/maximize-it/problem
"""
a=input()
li=[]
li=a.split(' ')

m=[]
sum=0
for i in range(0,int(li[0])):
    l=[]
    
    h=[]
    c=input()
    h=c.split(' ')

    for j in range(1,int(h[0])+1):
        l.append(int(h[j]))

    m.append(max(l))

s=0
print(m)
for i in range(0,len(m)):
    s=s+m[i]*m[i]
print(s%int(li[1]))


for _ in range(10):
    print("Hey! Listen!")

x = lambda a: a + 10
print(x(5))


lambda x: sum(i**2 for i in x
              

users=['Hello', 'World']
for user, status in 10,10:
    print(user)
    print(status)

sum(i**2 for i in 10)
print(sum)
"""

from itertools import product
K,M = map(int,input().split())
N = (list(map(int, input().split()))[1:] for _ in range(K))
results = map(lambda x: sum(i**2 for i in x)%M, product(*N))
print(max(results))
