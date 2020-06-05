def add(n):
    if(n==1):
        return 1
    
    return n+add(n-1)
    

print(add(int(input())))
