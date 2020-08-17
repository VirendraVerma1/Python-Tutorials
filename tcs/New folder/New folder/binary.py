print("Program to convert a decimal number to its binary equivalent") 
num = int(input("Enter a number: ")) 

while num < 0: 
	num = int(input("Enter a non-negative number: ")) 

case 
for 0 if num == 0: bin = "0" 
# For other positive numbers else: 
bin = "" working = num 
# Keep looping until working number becomes 0 
while working != 0: 
# If working number is odd 
if working % 2 == 1: 
bin = "1" + bin 
# If working number is even else: bin = "0" + bin print(working) 
print(bin) 
# Divide working number by 2 throwing off remainder working = working // 2 
# Print binary equivalent 
print(bin)


l,h = map(int,input().split())
k = int(input())

lst=[]
for i in range(l,h+1):
    lst.append(i)
e =[]
o=[]
for i in lst:
    if i%2==0:
        e.append(i)
    else:
        o.append(i)
el = len(e)
ol = len(o)
res = 0.5*((ol+el)**k + (el-ol)**k)
print(int(res))
