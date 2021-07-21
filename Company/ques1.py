# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 14:55:35 2021

@author: Virendra
"""

#sample input 4,2,4,5,6,4,5,1,2,4,6,0,1,6
n=input()
linum=n.split(',')
li=[]
for i in linum:
    li.append(int(i))
#li=[4,2,4,5,6,4,5,1,2,4,6,0,1,6]
newli=[]
newcounter=[]
for i in range(0,len(li)):
    
    flag=0
    for j in range(0,len(newli)):
        if(li[i]==newli[j]):
            flag=1
            newcounter[j]+=1
    if(flag==0):
        newli.append(li[i])
        newcounter.append(flag)
 
s=""
print(newli,newcounter)
for i in range(0,len(newcounter)):
    if(newcounter[i]>1):
        s=s+" "+str(newli[i])
        
print(s)