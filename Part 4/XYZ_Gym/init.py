from flask import Flask, request, render_template, session
from Member import Member
from Class import Class
from Instructor import Instructor
from GymFacility import GymFacility
from Attendance import Attendance
from Database import Database
from datetime import datetime
from Equipment import Equipment
import pickle

# XYZ Gym Started By Julian Marquez

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/menu",methods=['POST'])
def menu():

    action = request.form.get('action')

    if action == 'members':
        return render_template('membersMenu.html',members = Database().get_all_members())
    elif action == 'classes':
        return render_template('classMenu.html',classes = Database().get_all_classes(),facilities = Database().get_all_gym_facilities())
    elif action == 'equipment':
        return render_template("equipment.html",equipment = Database().get_all_equipment())
    else:
        classColors = ['color-green', 'color-blue', 'color-indigo', 'color-purple', 'color-teal', 'color-pink']
        return render_template('attendence.html',attendance = Database().get_all_attendance(),classColors = classColors)
@app.route('/addMember', methods=['POST'])
def addMember():

    fName = request.form.get('firstName')
    lName = request.form.get('lastName')
    email = request.form.get('email')
    phone = request.form.get('phone')
    age = request.form.get('age')
    address  = request.form.get('address')
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')

    member = Member(f"{fName} {lName}",email,phone,address,age,startDate,endDate)

    Database().insert_member(member)

    return render_template('membersMenu.html',members = Database().get_all_members())

@app.route("/addClass",methods = ['POST'])
def addClass():

    name = request.form.get('name')
    classType = request.form.get('classType')
    duration = request.form.get('duration')
    capacity = request.form.get('capacity')
    instructorId = request.form.get('instructorId')
    gymId = request.form.get('gymId')

    _class = Class(name,classType,duration,capacity,instructorId,gymId)

    Database().insert_class(_class)

    return render_template('classMenu.html',classes = Database().get_all_classes())

@app.route("/addEquipment", methods=['GET'])
def show_add_equipment_form():
    return render_template('addEquipment.html')

@app.route("/addEquipment", methods=['POST'])
def addEquipment():
    name = request.form.get('name')
    equipmentType = request.form.get('type')
    quantity = request.form.get('quantity')
    gymId = request.form.get('gymId')

    if Database().insert_equipment(name, equipmentType, quantity, gymId):
        print("Equipment inserted successfully.")
    else:
        print("Failed to insert equipment.")

    return render_template('equipment.html', equipment=Database().get_all_equipment())

@app.route("/handleClasses",methods = ['POST'])
def handleClasses():

    action = request.form.get('action')
    classId = request.form.get('classId')

    allGyms = Database().get_all_gym_facilities()
    allInstructors  = Database().get_all_instructors()

    if action == 'addClass': # this saves time, check before running any loops
        return render_template('addClass.html',instructors = allInstructors,facilities = allGyms) 

    else:
        _class = None
        for class_ in Database().get_all_classes():
            if int(class_.classId) == int(classId):
                _class = class_

        if action == 'remove':
            Database().deleteClass(_class)
            return render_template('classMenu.html',classes = Database().get_all_classes())
        else:
            return render_template('editClass.html',eClass = _class,instructors = allInstructors,facilities = allGyms )


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/attendence")
def attendance():
    classColors = ['color-green', 'color-blue', 'color-indigo', 'color-purple', 'color-teal', 'color-pink']
    return render_template('attendence.html',attendance = Database().get_all_attendance(),classColors = classColors)

@app.route("/members")
def members():
    connect = Database()

    #members = connect.get_all_members()
    return render_template("membersMenu.html",members = connect.get_all_members())

@app.route("/classes")
def classes():
    return render_template("classMenu.html",classes = Database().get_all_classes(),facilities = Database().get_all_gym_facilities())

@app.route("/equipment")
def equipment():
    return render_template("equipment.html",equipment = Database().get_all_equipment())


@app.route("/handleMembers",methods=['POST'])
def handleMembers():

    # both have the same value (memberId) but depending on the one chosen will redirect the 
    action = request.form.get('action') #remove button
    memberId = request.form.get('memberId') # member's ID

    member = None

    for member_ in Database().get_all_members():
        if int(memberId) == int(member_.id):
            member = member_

    if action == 'remove': 
        Database().deleteMember(member)
        return render_template("membersMenu.html",members = Database().get_all_members())
    elif action == 'addMember':
        return render_template('addMember.html')
    elif action == 'attends':
        classColors = ['color-green', 'color-blue', 'color-indigo', 'color-purple', 'color-teal', 'color-pink']
        return render_template('attendence.html',attendance = member.attendance,classColors = classColors)
    else:
        for member_to_edit in Database().get_all_members():
            if member_to_edit.id == int(memberId):
                return render_template("editMember.html",member = member_to_edit)

    return render_template("membersMenu.html",members = Database().get_all_members())


@app.route("/handleEquipment", methods=['POST'])
def handleEquipment():
    equipmentId = request.form.get('id')
    action = request.form.get('action')

    # Debugging output
    print(f"Handling equipment: action={action}, id={equipmentId}")

    if action == 'add':
        return render_template('addEquipment.html')
    elif action == "remove":
        print(f"Attempting to delete equipment with ID: {equipmentId}")
        if Database().deleteEquipment(equipmentId):
            print("Delete successful!")
        else:
            print("Delete failed.")
        return render_template('equipment.html', equipment=Database().get_all_equipment())
    elif action == "update":  # Check if it's an update action
        name = request.form.get('name')
        type_ = request.form.get('type')
        quantity = request.form.get('quantity')
        gymId = request.form.get('gymId')

        print(f"Updating equipment: {name}, {type_}, {quantity}, {gymId}")

        success = Database().updateEquipment(equipmentId, name, type_, quantity, gymId)
        
        if success:
            print("Update successful!")
        else:
            print("Update failed.")
        
        # Reload the equipment page after updating
        return render_template('equipment.html', equipment=Database().get_all_equipment())

    else:
        equip = None
        for _equip in Database().get_all_equipment():
            if int(_equip.id) == int(equipmentId):
                equip = _equip

        return render_template('editEquipment.html', equipment=equip)
    
@app.route("/editMember",methods=['POST'])
def editMember():

    memberId = request.form.get('memberId')
    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age')
    phone = request.form.get('phone')
    address = request.form.get('address')
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')

    editMember = None

    for member in Database().get_all_members():
        if member.id == int(memberId):
            editMember = member

    if name:
        editMember.name = name
    if email:
        editMember.email = email
    if age:
        editMember.age = int(age)
    if phone:
        editMember.phone = phone
    if address:
        editMember.address = address
    if startDate:
        editMember.startDate = startDate
    if endDate:
        editMember.endDate = endDate
        
    if editMember:
        Database().update_member(editMember)

    return render_template("membersMenu.html",members = Database().get_all_members())


@app.route("/editClass",methods = ['POST'])
def editClass():

    classId = request.form.get('classId')
    name = request.form.get('name')
    classType = request.form.get('classType')
    duration = request.form.get('duration')
    capacity = request.form.get('capacity')
    instructorId = request.form.get('instructorId')
    gymId = request.form.get('gymId')

    eClass = None

    for _class in Database().get_all_classes():
        if _class.classId == int(classId):
            eClass = _class

    if name:
        eClass.className = name
    if classType:
        eClass.classType = classType
    if duration:
        eClass.duration = duration
    if capacity:
        eClass.classCapacity = capacity
    if instructorId:
        eClass.instructorId = instructorId
    if gymId:
        eClass.gymId = gymId

    Database().update_class(eClass)

    return render_template('classMenu.html',classes = Database().get_all_classes())


if __name__ == '__main__':# main 
    app.run(debug=True) 


  
