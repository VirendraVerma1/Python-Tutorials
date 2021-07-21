def Palindrome(a,i):
    
    t=False
    if(a[i]==a[len(a)-i-1]):
        t=True
    else:
        t=False
    
    if(i>=len(a)-i-1 or t==False):
        return t
        
    return Palindrome(a,i+1)

a=input()
t=Palindrome(a,0)
if(t==True):
    print("Palindrome")
else:
    print("Not a Palindrome")
