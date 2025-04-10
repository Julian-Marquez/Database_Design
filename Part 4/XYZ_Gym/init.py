from flask import Flask, request, render_template, session
from Member import Member
from Class import Class
from Instructor import Instructor
from GymFacility import GymFacility
from Database import Database
from datetime import datetime
import pickle


if __name__ == '__main__':

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


