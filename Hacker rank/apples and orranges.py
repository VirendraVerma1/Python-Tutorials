#https://www.hackerrank.com/challenges/apple-and-orange/problem?h_r=next-challenge&h_v=zen

def countApplesAndOranges(s, t, a, b, apples, oranges):
    checkera=0
    checkerb=0
    
    lia=[]
    checkera=0
    for i in range(0,len(apples)):
        lia.append(a+apples[i])
        if(lia[i]>=s and lia[i]<=t):
            checkera=checkera+1
    lib=[]
    checkerb=0
    for i in range(0,len(oranges)):
        lib.append(b+oranges[i])
        if(lib[i]<=t):
            checkerb=checkerb+1

    print(lia)
    print(lib)
    print(checkera)
    print(checkerb)


countApplesAndOranges(7,10,4,12,[2,3,-4],[3,-2,-4])
