import math



def po(a,b):
    if(b==1):
        return 1
    return a*po(a,b-1)


t=po(int(input()),int(input())+1)
print(t)
print(math.log(t))
