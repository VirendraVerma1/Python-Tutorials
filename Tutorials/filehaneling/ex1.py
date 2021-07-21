#creating file
with open("filename.txt",'w') as file:
    file.write("")

#writing in file
file=open("test.txt",'w')
file.write("dog")

file.close()

#open file in append mode
file=open("test.txt",'a')
file.write("\ncat")
file.close()

#reading file as it is
file=open("test.txt",'r')
content=file.read()
print(content);

#storing in list
file.seek(0)
content1=file.readline()
#print(content1)

#storring each charecter in list
content2=[i.rstrip("\n") for i in content]
#print(content2)

file.close()
