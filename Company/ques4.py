# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 15:24:23 2021

@author: Virendra
"""
#, end =" "
n=int(input())
#n=5
li=[]
sum=0
counter=0
prev=1
for i in range(1,n*n):
    sum=counter+prev
    li.append(sum)
    counter=prev
    prev=sum
  

counter=0
rev=n
for i in range(0,n):
    
    rev=n-i
    for j in range(0,n):
        rev-=1
        if(rev>0):
            print(" ", end =" ")
        else:
            print(li[counter], end =" ")
            counter+=1
    
    print("")