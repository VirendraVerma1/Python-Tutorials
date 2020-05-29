#method resolution order
class A:#super class

    def __init__(self):
        print("In a init")
        
    def feature1(self):
        print("Feature 1 working")

    def feature2(self):
        print("Feature 2 working")


class B(A): #class b is inheriting all the feature of class A inheritance

    def __init__(self):#its override the above init of a
        super().__init__()
        print("in B in It")
    
    def feature3(self):#subclass
        print("Feature 3 working")

    def feature4(self):
        print("Feature 4 working")

class C:#super class

    def __init__(self):
        print("In c init")
        
    def feature1(self):
        print("Feature 1 working")

    def feature2(self):
        print("Feature 6 working")

class D:#super class

    def __init__(self):
        print("In d init")
        
    def feature1(self):
        print("Feature 1 working")

    def feature2(self):
        print("Feature 5 working")

class E(D,C):#super class

    def __init__(self):
        super().__init__()
        print("In e init")
        
    def feature1(self):
        super().feature2()
        print("Feature 1 working")

    def feature2(self):
        print("Feature 4 working")

a1=B()
a2=E()
a2.feature1()
