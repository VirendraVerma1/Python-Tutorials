#https://www.hackerrank.com/challenges/sock-merchant/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=warmup

def sockMerchant(n, ar):
    pair=0
    li=ar
    
    l=len(li)
    a=0
    while(a==0):
        x=0
        y=0
        t=0
        for i in range(0,l):
            for j in range(0,l):
                if(t==0):
                    if(li[i]==li[j] and not i==j):
                        
                        x=i
                        y=j
                        t=1
                    

        if(t==1):
            
            li.pop(x)
            li.pop(y-1)
            l=len(li)
            pair=pair+1
            
        if(t==0):
            a=1


    print(pair)
sockMerchant(9,[10,20,20,10,10,30,50,10,20])
