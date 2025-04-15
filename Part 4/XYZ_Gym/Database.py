import sqlite3
import sys
from Member import Member
from Class import Class
from Instructor import Instructor
from GymFacility import GymFacility

class Database: # Made a dedicated database class for simplicity
    def __init__(self):
        self.connect = sqlite3.connect("XYZGym.sqlite")

    def get_all_members(self):
        conn = self.connect
        cursor = conn.cursor()
        query = '''
        SELECT memberId, name, email, phone, address, age, membershipStartDate, membershipEndDate
        FROM Member;
        '''
        cursor.execute(query)
        members = cursor.fetchall()
        allMembers = []
        for m in members:
            member = Member(m[1],m[2],m[3],m[4],m[5],m[6],m[7])
            member.id = m[0]
            allMembers.append(member)

        return allMembers

    def get_all_instructors(self):
        conn = self.connect
        cursor = conn.cursor()
        query = '''
        SELECT instructorId, name, specialty, phone, email FROM Instructor;
        '''
        cursor.execute(query)
        instructors = cursor.fetchall()
        allInstructors = []
        
        for instructor in instructors:

            allInstructors.append(Instructor(instructor[0],instructor[1],instructor[2],instructor[3],instructor[4]))
        
        
        return allInstructors

    def get_all_gym_facilities(self):
        conn = self.connect
        cursor = conn.cursor()
        query = '''
        SELECT gymId, location, phone, manager FROM GymFacility;
        '''
        cursor.execute(query)
        facilities = cursor.fetchall()
        allFacilities = []
        
        for facility in facilities:
            allFacilities.append(GymFacility(facility[0],facility[1],facility[2],facility[3]))
        
        return allFacilities

    def get_all_classes(self):
        conn = self.connect
        cursor = conn.cursor()
        query = '''
        SELECT classId, className, classType, duration, classCapacity, instructorId, gymId
        FROM Class;
        '''
        cursor.execute(query)
        classes = cursor.fetchall()
        allClasses = []
        
        for _class in classes:
            class_ = Class(_class[1], _class[2],_class[3],_class[4],_class[5],_class[6])
            class_.classId = _class[0]
            allClasses.append(class_)
        
        return allClasses

    def get_all_equipment(self):
        conn = self.connect
        cursor = conn.cursor()
        query = '''
        SELECT equipmentId, name, type, quantity, gymId FROM Equipment;
        '''
        cursor.execute(query)
        equipment = cursor.fetchall()
        allEquipment = []
        
        for equip in equipment:
            allEquipment.append(equip[0],equip[1],equip[2],equip[3],equip[4])
        
        return allEquipment

    def get_all_membership_plans(self):
        conn = self.connect
        cursor = conn.cursor()
        query = '''
        SELECT planId, planType, cost FROM MembershipPlan;
        '''
        cursor.execute(query)
        plans = cursor.fetchall()
        allPlans = []
        
        for plan in plans:
            allPlans.append(plan[0],plan[1],plan[2])

        return allPlans

    def get_all_payments(self):
        conn = self.connect
        cursor = conn.cursor()
        query = '''
        SELECT paymentId, memberId, planId, amountPaid, paymentDate FROM Payment;
        '''
        cursor.execute(query)
        payments = cursor.fetchall()
        allPayments = []
        
        for payment in payments:
            print(f"Payment ID: {payment[0]}, Member ID: {payment[1]}, Plan ID: {payment[2]}, Amount Paid: {payment[3]}, Payment Date: {payment[4]}")
        
        return payments

    def get_all_attendance(self):
        conn = self.connect
        cursor = conn.cursor()
        query = '''
        SELECT memberId, classId, attendanceDate FROM Attends;
        '''
        cursor.execute(query)
        attendance = cursor.fetchall()
        
        for attend in attendance:
            print(f"Member ID: {attend[0]}, Class ID: {attend[1]}, Attendance Date: {attend[2]}")

        return attendance


    def insert_member(self, member: Member):
        try:
            conn = self.connect
            cursor = conn.cursor()
            query = '''
            INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            '''
            cursor.execute(query, (
                member.name,
                member.email,
                member.phone,
                member.address,
                int(member.age),
                member.startDate,
                member.endDate
            ))
            conn.commit()
            print("Member inserted successfully.")
            return True
        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return False

    def insert_class(self, _class: Class):
        try:
            conn = self.connect
            cursor = conn.cursor()
            query = '''
            INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId)
            VALUES (?, ?, ?, ?, ?, ?);
            '''
            cursor.execute(query, (
               _class.className,
               _class.classType,
               _class.duration,
               _class.classCapacity,
               _class.instructorId,
               _class.gymId
            ))
            conn.commit()
            print("Member inserted successfully.")
            return True
        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return False

    def update_member(self, member: Member):
        try:
            with sqlite3.connect("XYZGym.sqlite") as conn:
                cursor = conn.cursor()
                query = '''
                UPDATE Member
                SET name = ?, email = ?, phone = ?, address = ?, age = ?, membershipStartDate = ?, membershipEndDate = ?
                WHERE memberId = ?;
                '''
                cursor.execute(query, (
                    member.name,
                    member.email,
                    member.phone,
                    member.address,
                    int(member.age),
                    member.startDate,
                    member.endDate,
                    member.id
                ))
                conn.commit()
                print(f"update succesful")
                return True
        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return False

    def update_class(self,_class : Class):
        try:
            with sqlite3.connect("XYZGym.sqlite") as conn:
                cursor = conn.cursor()
                query = '''
                UPDATE Class
                SET className = ?, classType = ?, duration = ?, classCapacity = ?, instructorId = ?, gymId = ?
                WHERE classId = ?;
                '''
                cursor.execute(query, (
                    _class.className,
                    _class.classType,
                    _class.duration,
                    _class.classCapacity,
                    _class.instructorId,
                    _class.gymId,
                    _class.classId
                ))
                conn.commit()
                print(f"update succesful")
                return True
        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return False


    def deleteMember(self, member: Member):
        try:
            with sqlite3.connect("XYZGym.sqlite") as conn:
                cursor = conn.cursor()
                query = '''
                DELETE FROM Member
                WHERE memberId = ?;
                '''
                cursor.execute(query, (member.id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"SQLite Error during delete: {e}")
            return False

    def deleteClass(self, _class: Class):
        try:
            with sqlite3.connect("XYZGym.sqlite") as conn:
                cursor = conn.cursor()
                query = '''
                DELETE FROM Class
                WHERE classId = ?;
                '''
                cursor.execute(query, (_class.classId,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"SQLite Error during delete: {e}")
            return False

