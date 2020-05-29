class computer:

    def __init__(self,cpu,ram):
        self.cpu=cpu
        self.ram=ram
                
    def config(self):
        print("test ",self.cpu,self.ram)

com1=computer('i4',19)
com2=computer('43',2)
com1.config()
computer.config(com2)

