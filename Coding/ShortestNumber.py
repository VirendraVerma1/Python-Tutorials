li1=[3,1,1]
li2=[6,5,4]

li1.sort(reverse=True)
li2.sort()

print(li1)
print(li2)
sum=0
for i in range(0,len(li1)):
    sum=sum+li1[i]*li2[i]

print(sum)
