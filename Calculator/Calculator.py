# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 15:21:16 2020

@author: Virendra
"""

s=input()
li_symbol=[]
li_num=[]

t=""
for i in s:
    if(i.isdigit() or i=="."):
        t+=i
    else:
        li_num.append(float(t))
        li_symbol.append(i)
        t=""
li_num.append(float(t))
print(s)
print(li_symbol,li_num)
while(len(li_symbol)>0):
    sum=0
    counter=0
    if(counter==0):
        for i in range(0,len(li_symbol)):
            if(li_symbol[i]=="/"):
                sum=li_num[i]/li_num[i+1]
                li_num[i]=sum
                li_num.pop(i+1)
                li_symbol.pop(i)
                counter=1
                break;
    if(counter==0):
        for i in range(0,len(li_symbol)):
            if(li_symbol[i]=="*"):
                sum=li_num[i]*li_num[i+1]
                li_num[i]=sum
                li_num.pop(i+1)
                li_symbol.pop(i)
                counter=1
                break;
    if(counter==0):
        for i in range(0,len(li_symbol)):
            if(li_symbol[i]=="+"):
                sum=li_num[i]+li_num[i+1]
                li_num[i]=sum
                li_num.pop(i+1)
                li_symbol.pop(i)
                counter=1
                break;
    if(counter==0):
        for i in range(0,len(li_symbol)):
            if(li_symbol[i]=="-"):
                sum=li_num[i]-li_num[i+1]
                li_num[i]=sum
                li_num.pop(i+1)
                li_symbol.pop(i)
                counter=1
                break;
    print(li_num,li_symbol)
print("Ans = ",li_num[0])
123