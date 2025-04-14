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
    lName = request.form.grt('lastName')
    email = request.form.get('email')
    phone = request.form.get('phone')

    print('data received for now: ' + fName + ' ' + lName + ' ' + email + ' ' + phone)


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
    return render_template("classMenu.html")

@app.route("/equipemnet")
def equipemnet():
    return render_template("equipment.html")


@app.route("/handleMembers",methods=['POST'])
def handleMembers():

    # both have the same value (memberId) but depending on the one chosen will redirect the 
    action = request.form.get('action') #remove button
    memberId = request.form.get('memberId') # member's ID

    if action == 'remove': # tester for now 
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


