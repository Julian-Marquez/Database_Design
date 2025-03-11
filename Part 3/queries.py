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

def get_classes_taught(instructorId):
    conn = connect_db()  # Always start by connecting to the DB
    cursor = conn.cursor()
    
    query = '''
    SELECT Instructor.name, Instructor.phone, Class.className, Class.classType, Class.duration, Class.classCapacity
    FROM Instructor
    JOIN Class ON Instructor.instructorId = Class.instructorId
    WHERE Instructor.instructorId = ?;
    '''
    
    cursor.execute(query, (instructorId,))
    classes_taught = cursor.fetchall()
    conn.close()
    
    return classes_taught

def get_average_age_memberships():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Query to calculate average age for active and expired memberships
    query = '''
    SELECT
        AVG(CASE WHEN membershipEndDate >= date('now') THEN age ELSE NULL END) AS avg_active_age,
        AVG(CASE WHEN membershipEndDate < date('now') THEN age ELSE NULL END) AS avg_expired_age
    FROM Member;
    '''
    
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

def get_top_instructors():
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT Instructor.name, COUNT(Class.classId) AS class_count
    FROM Instructor
    JOIN Class ON Instructor.instructorId = Class.instructorId
    GROUP BY Instructor.instructorId
    ORDER BY class_count DESC
    LIMIT 3;
    '''
    cursor.execute(query)
    instructors = cursor.fetchall()
    conn.close()
    return instructors

def members_attended_all(class_type):
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT Member.name
    FROM Member
    JOIN Attends ON Member.memberId = Attends.memberId
    JOIN Class ON Attends.classId = Class.classId
    WHERE Class.classType = ?
    GROUP BY Member.name
    HAVING COUNT(DISTINCT Class.classId) = (SELECT COUNT(*) FROM Class WHERE classType = ?);
    '''
    cursor.execute(query, (class_type, class_type))
    members = cursor.fetchall()
    conn.close()
    return members

def members_attended_last_month():
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT Member.name, Class.className, Class.classType
    FROM Member
    JOIN Attends ON Member.memberId = Attends.memberId
    JOIN Class ON Attends.classId = Class.classId
    WHERE Attends.attendanceDate >= date('now', '-1 month');
    '''
    cursor.execute(query)
    members = cursor.fetchall()
    conn.close()
    return members
# Get user input for question number and params
def main():

    if len(sys.argv) < 2:
        print("Please provide a valid question number.")
        return
    question_number = int(sys.argv[1]) # requiers an integer as an input

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
    elif question_number == 6 and len(sys.argv) == 3: # paramters are needed for cetain question
        instructorId = sys.argv[2]
        classes_taught = get_classes_taught(instructorId)
        for classes in classes_taught:
            print(f"Classes Taght: {classes_taught}")
        
    elif question_number == 7:
        average_age = get_average_age_memberships()
        for age in average_age:
            average_age = round(age) # round it off
        print(f"Average age for Active Memberships is {average_age} years old.")

        
    elif question_number == 8:
        instructors = get_top_instructors()
        print("Top 3 instructors: ")
        for The_best in instructors:
            print(The_best)
        
    elif question_number == 9 and len(sys.argv) == 3:
        class_type = sys.argv[2]
        members = members_attended_all(class_type)
        for member in members:
            print(member)

    elif question_number == 10:
        members = members_attended_last_month()
        for member in members:
            print(member)
    else:
        print("Invalid input. You have a missing or invalid argument.")

if __name__ == "__main__": # main 
    main()