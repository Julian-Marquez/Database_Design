import datetime

class Member:
    def __init__(self,id,name,email,phone,address,age):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.age = age
        date = datetime.datetime.now()
        self.startDate = date.strftime("%Y-%m-%d") # every new instance is the starting date unless reloading from the database 


