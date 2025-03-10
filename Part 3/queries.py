import sqlite3
import sys

# Connect to database
def connect_db():
    # Only connects if XYZGym.sqlite has same path as queries.py
    return sqlite3.connect("XYZGym.sqlite")

# Query 1: Retrieve a list of all members in the gym
def get_all_members():
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT name, email, age, membershipPlan.planType 
    FROM Member
    JOIN Payment ON Member.memberId = Payment.memberId
    JOIN MembershipPlan ON Payment.planId = MembershipPlan.planId;
    '''
    cursor.execute(query)
    members = cursor.fetchall()
    conn.close()
    return members

# Query 2: Count the number of classes available at each gym facility
def count_classes_by_gym():
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT GymFacility.location, COUNT(Class.classId)
    FROM GymFacility
    LEFT JOIN Class ON GymFacility.gymId = Class.gymId
    GROUP BY GymFacility.location;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

# Query 3: Retrieve the names of members attending a specific class by classId
def get_members_by_class(classId):
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT Member.name
    FROM Member
    JOIN Attends ON Member.memberId = Attends.memberId
    WHERE Attends.classId = ?;
    '''
    cursor.execute(query, (classId,))
    members = cursor.fetchall()
    conn.close()
    return members

# Query 4: List all equipment of a specific type
def get_equipment_by_type(equipment_type):
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT name, type, quantity
    FROM Equipment
    WHERE type = ?;
    '''
    cursor.execute(query, (equipment_type,))
    equipment = cursor.fetchall()
    conn.close()
    return equipment

# Query 5: Find all members with expired memberships
def get_expired_members():
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT name, email, membershipEndDate
    FROM Member
    WHERE membershipEndDate < date('now');
    '''
    cursor.execute(query)
    expired_members = cursor.fetchall()
    conn.close()
    return expired_members

# Add Functions for Queries 6-10 here

# Get user input for question number and params
def main():

    if len(sys.argv) < 2:
        print("Please provide a valid question number.")
        return
    question_number = int(sys.argv[1])
    # Add some more error handling? 

    if question_number == 1:
        members = get_all_members()
        for member in members:
            print(member)
    elif question_number == 2:
        result = count_classes_by_gym()
        for item in result:
            print(f"Gym Location: {item[0]}, Classes Count: {item[1]}")
    elif question_number == 3 and len(sys.argv) == 3:
        classId = int(sys.argv[2])
        members = get_members_by_class(classId)
        for member in members:
            print(member)
    elif question_number == 4 and len(sys.argv) == 3:
        equipment_type = sys.argv[2]
        equipment = get_equipment_by_type(equipment_type)
        for eq in equipment:
            print(eq)
    elif question_number == 5:
        expired_members = get_expired_members()
        for member in expired_members:
            print(member)
    # Elif statements for Queries 6-10
    else:
        print("Invalid input. You have a missing or invalid argument.")

if __name__ == "__main__":
    main()
