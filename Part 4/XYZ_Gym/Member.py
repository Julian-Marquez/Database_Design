import datetime

class Member:
    def __init__(self,name,email,phone,address,age,startDate,endDate):
        self.id = 0
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.age = age
        self.startDate = startDate
        self.endDate = endDate
        self.classes = []
        self.attendance = []