# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 15:14:38 2021

@author: Virendra
"""
#n="1,2,4,4,6,10,12"
n=input()
linum=n.split(',')
li=[]
for i in linum:
    li.append(int(i))
    
#m="4,6,10"
m=input()
li1num=m.split(',')
li1=[]
for i in li1num:
    li1.append(int(i))
    
print(li,li1)
counter=len(li1)
b=0
for i in range(0,len(li)):
    flag=0
    for j in range(0,len(li1)):
        if(li[b]==li1[j]):
            print(li[b],li1[j],counter)
            b+=1
            counter-=1
            if(counter<=0):
                break
        else:
            b=i
            counter=len(li1)
    if(counter<=0):
        break
            
          
if(counter==0):
    print("true")
else:
    print("false")