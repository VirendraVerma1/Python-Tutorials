def Palindrome(a,s,i):
    
    if(i>len(a)-1):
        return s
    else:
        s=s+a[len(a)-i-1]
        return Palindrome(a,s,i+1)

a=input()
t=Palindrome(a,"",0)
print(t)
