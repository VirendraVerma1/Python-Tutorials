#https://www.hackerrank.com/challenges/grading/problem
#!/bin/python3

#
# Complete the 'gradingStudents' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY grades as parameter.
#

def gradingStudents(grades):
    # Write your code here
    li=[]
    for i in range(0,len(grades)):
        n=0
        r=0;
        while(n<grades[i]):
            n=r*5
            r=r+1

        if(grades[i]<38):
            li.append(grades[i])
        elif(n-grades[i]<3):
            li.append(n)
        else:
            li.append(grades[i])

    return li

print(gradingStudents([4,73,67,38,33]))
