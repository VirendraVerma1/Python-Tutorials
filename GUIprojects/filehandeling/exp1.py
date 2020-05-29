file1=open("test.txt",'w')
file1.write("hello world")
file1.close()

file=open("test.txt",'r')
print(file.read())
