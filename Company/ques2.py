# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 14:56:05 2021

@author: Virendra
"""

#sample input 1,7,3,4
#[14, 49, 11, 7]
#n="1,7,3,4"
n=input()
linum=n.split(',')
li=[]
for i in linum:
    li.append(int(i))
    
turn=0
temp=[]
newli=[]
for i in range(0,len(li)):
    #-----------------turn changer
    if(turn==0):
        turn=1
    else:
        turn=0
        
    #--------------------regular initializer
    currentNU=li[i]
    temp.clear()
    mult=1
    summ=0
    
    #-------------------greater number initializer
    for j in li:
        if(j>currentNU):
            temp.append(j)
           
    if(len(temp)==0):
        temp.append(currentNU)
        
    #print(li[i],temp)
    
    #-------------------mulitiplication and addition
    if(turn==0):    #means multiplication
        for j in temp:
            mult=mult*j
        if(mult==currentNU):
            mult=mult*mult
        newli.append(mult)
    else:#means addition
        for j in temp:
            summ=summ+j
            
        newli.append(summ)
        
print(newli)