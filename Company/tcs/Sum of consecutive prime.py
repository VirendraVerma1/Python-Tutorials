n=9999

primenu=[]
print("First method")
for i in range(2,n):
    flag=0
    for j in range(2,(i//2)+1):
        if(i%j==0):
            flag+=1

    if(flag==0):
        primenu.append(i) 

print(primenu)
g=0
for i in range(0,len(primenu)):
    m=i
    g=0
    for j in range(0,m):
        g+=primenu[j]
        
        #print(primenu[m])
        if(g==primenu[m]):
            print(g)
        
    
"""
print("\n\n\n\n\n\nSecond method")
for k in range(3,n+1):
    m=k
    g=0
    for i in range(2,m):
        flag=0
        for j in range(2,(i//2)+1):
            if(i%j==0):
                flag+=1

        if(flag==0):
            g+=i
            #print(i)
        
        if(g==k and flag==0):
            print(g)
            
            print("-----------")
            g=0
        
            
""" 
    
