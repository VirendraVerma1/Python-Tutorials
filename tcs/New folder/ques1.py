input1=3
input2=[80,48,82]

midvalue=int(len(input2)/2)

sum=0
midarray=input2[midvalue]
print(midarray)
for i in input2:
    print(i)
    if(i>=midarray):
        sum+=midarray

print(sum)
