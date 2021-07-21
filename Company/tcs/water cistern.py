#https://www.tcscodevita.com/CodevitaV8/samplequestion.jsp

print("Radius, Height, TopSurface")
li1=[]
a=input()
li1=a.split(',')

print("First Coordinate, Second Coordinate")
li2=[]
b=input()
li2=b.split(',')

sum=0
if(int(li2[0])<0):
    sum=int(li1[2])+int(li1[0])-int(li2[0])
else:
    sum=(2*3.14*int(li1[0])*int(li2[1]))/359

print(int(sum))
