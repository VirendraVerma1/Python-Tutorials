a=1
b=10

d=2

counter=0
listt=[[]]
for i in range(a,b+1):
    combo=[]
    for j in range(a,b+1):
        counter+=1
        combo.append(i)
        combo.append(j)
        listt.append(combo.copy())
        combo.clear()
print(counter)
print(listt)

print("Sceond method")
from itertools import permutations  
  
# Get all permutations of [1, 2, 3] 
perm = permutations([1, 2,3,4],4) 
  
# Print the obtained permutations
counter=0
for i in list(perm): 
    sum=i[0]+i[1]
    
    counter+=1

print(counter)
