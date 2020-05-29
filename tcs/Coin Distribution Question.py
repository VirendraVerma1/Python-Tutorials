#https://www.faceprep.in/tcs/tcs-codevita-questions/

#get the input
number = int(input())


#find the number of five rupee coins
#maximize possible number of coins, after leavinf out 4 rupees to make all possible values till 4
five = int((number-4)/5)
print(five)

#find the number of one rupee coins
#of the remaining value, number of one rupee coins is 1, if the value is odd & it is 2 if the value is even
if((number-5*five) % 2) == 0:
    one=2
else:
    one=1
print(one)

#find the number of two rupee coins
#the rest of the amount will be from two rupee coins
two=(number-5*five-one)//2
print(two)

#print total coins, five ruppe coins, two rupee coins, one rupee coins    
print(one+two+five,five,two,one)

