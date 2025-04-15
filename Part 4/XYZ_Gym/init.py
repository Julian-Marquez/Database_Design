from flask import Flask, request, render_template, session
from Member import Member
from Class import Class
from Instructor import Instructor
from GymFacility import GymFacility
from Database import Database
from datetime import datetime
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

@app.route("/members")
def members():
    connect = Database()

    #members = connect.get_all_members()
    return render_template("membersMenu.html",members = connect.get_all_members())

@app.route("/classes")
def classes():
    return render_template("classMenu.html",classes = Database().get_all_classes(),facilities = Database().get_all_gym_facilities())

@app.route("/equipemnet")
def equipemnet():
    return render_template("equipment.html")


@app.route("/handleMembers",methods=['POST'])
def handleMembers():

    # both have the same value (memberId) but depending on the one chosen will redirect the 
    action = request.form.get('action') #remove button
    memberId = request.form.get('memberId') # member's ID

    if action == 'remove': 
        for member in Database().get_all_members():
            if int(memberId) == int(member.id):
                Database().deleteMember(member)
                return render_template("membersMenu.html",members = Database().get_all_members())
    elif action == 'addMember':
        return render_template('addMember.html')
    else:
        for member_to_edit in Database().get_all_members():
            if member_to_edit.id == int(memberId):
                return render_template("editMember.html",member = member_to_edit)

    return render_template("membersMenu.html",members = Database().get_all_members())

        
    
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


if __name__ == '__main__':
    app.run(debug=True)

    connect = Database()

    members = connect.get_all_members()
    classes = connect.get_all_classes()
    instructors = connect.get_all_instructors()
    facilities = connect.get_all_gym_facilities()


    for member in members:
        print(member.name)

    print('\n')

    for _class in classes:
        print(_class.duration)

    for instructor in instructors:
        print(instructor.specialty)

    print('\n')

    for facility in facilities:
        print(facility.location)


