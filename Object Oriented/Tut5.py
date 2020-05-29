#two type of method
#instance method
#class method
#static method

class student:

    school='Telusko'#class variable
    
    def __init__(self,m1,m2,m3):
        self.m1=m1#instance variable
        self.m2=m2
        self.m3=m3

    def avg(self):
        return((self.m1+self.m2+self.m3)/3)

    def get_m1(self):#accessors
        return self.m1

    def set_m1(self,value):#mutators
        self.m1=value

    @classmethod
    def info(cls):#if you use class variable use cls and when we use instance variable use self
        return cls.school

    @staticmethod
    def info():#use empty refers to static method
        print("This is Student Class")
        

s1=student(34,67,32)
s2=student(89,32,12)

print(s1.avg())
print(s2.avg())

print(student.info())
student.info()
#for fetch the value accessors
#for modify the value mutators
