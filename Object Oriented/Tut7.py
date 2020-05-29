class A:#super class
    def feature1(self):
        print("Feature 1 working")

    def feature2(self):
        print("Feature 2 working")


class B(A): #class b is inheriting all the feature of class A inheritance
    def feature3(self):#subclass
        print("Feature 3 working")

    def feature4(self):
        print("Feature 4 working")

class C(B):
    def feature5(self):
        print("Feature 5 working")
        
class E:
    def feature7(self):
        print("Feature 7 working")

class D(A,E):
    def feature6(self):
        print("Feature 6 working")
a1=A()
a1.feature1()
a1.feature2()

b1=B()
c1=C()
d1=D()
d1.feature7()
c1.feature1()
