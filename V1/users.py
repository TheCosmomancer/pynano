class User:
    def __init__(self,name,password,*privlages):
        self.name = name
        self.password = password
        self.privlages = [privlage for privlage in privlages]