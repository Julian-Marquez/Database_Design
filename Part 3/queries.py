# Gym Script, Written by Isabella Moleski and Julian Marquez with updates and review by Hannah Knight. CLI Tool

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
    if not members:
        return []
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
    if not result:
        return []
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
    if not members:
        return []
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
    if not equipment:
        return []
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
    if not expired_members:
        return []
    return expired_members

#Query 6: Find classes taught by an instructor
def get_classes_taught(instructorId):
    conn = connect_db()  # Always start by connecting to the DB
    cursor = conn.cursor()

    # Matches classes to instructor based on instructor ID
    query = '''
    SELECT Instructor.name, Instructor.phone, Class.className, Class.classType, Class.duration, Class.classCapacity
    FROM Instructor
    JOIN Class ON Instructor.instructorId = Class.instructorId
    WHERE Instructor.instructorId = ?;
    '''
    
    cursor.execute(query, (instructorId,))
    classes_taught = cursor.fetchall()
    conn.close()
    if not classes_taught:
        return []
    return classes_taught

# Query 7: Find average age of active and expired memberships
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

    avg_active_age, avg_expired_age = result
    if avg_active_age is None and avg_expired_age is None:
        return "No average member ages found."
    elif avg_active_age is None:
        return f"No active memberships found. Average age of expired memberships: {round(avg_expired_age)}"
    elif avg_expired_age is None:
        return f"No expired memberships found. Average age of active memberships: {round(avg_active_age)}"
    
    return result

# Query 8: Find top instructors
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
    if not instructors:
        return []
    return instructors

#Query 9: Find members who attended all classes of a specified type
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
    if not members:
        return []
    return members

# Query 10: Find members who attended classes last month
def members_attended_last_month():
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT Member.name, COUNT(Attends.classId) AS total_classes, 
           GROUP_CONCAT(DISTINCT Class.className) AS classes_attended,
           GROUP_CONCAT(DISTINCT Class.classType) AS class_types
    FROM Member
    JOIN Attends ON Member.memberId = Attends.memberId
    JOIN Class ON Attends.classId = Class.classId
    WHERE Attends.attendanceDate >= date('now', '-1 month')
    GROUP BY Member.name;
    '''
    cursor.execute(query)
    members = cursor.fetchall()
    conn.close()
    if not members:
        return []
    return members

# Get user input for question number and params
def main():

    if len(sys.argv) < 2:
        print("Welcome to the Gym DBMS Management Program. Commands are run as python queries.py N, where N is the option number (1-10) you selected. Here are your options: \n\t1. Return all gym members.\n\t2. Return the number of classes taught at each gym.\n\t3 X. Return members attending the class with integer ID X. \n\t4 S. Return equipment with a type matching string S. \n\t5. Return all members with expired memberships. \n\t6 X. Return all classes taught by an instructor with integer ID X. \n\t7. Return the average age of members with expired and active memberships, separately. \n\t8. Return the top three instructors teaching the most classes. \n\t9 S. Return members who have attended all classes of a specified type string S \n\t10. Return all members who attended classes in the last month..")
        print("Please provide a valid question number.")
        return
    question_number = int(sys.argv[1]) # requires an integer as an input

    if question_number == 1:
        members = get_all_members()
        print("All members of the gym are:")
        if not members:
            print("No members found.")
        for member in members:
            print(member)
            
    elif question_number == 2:
        result = count_classes_by_gym()
        if not result:
            print("No gyms found.")
        print("Here are the number of classes taught at each gym.")
        for item in result:
            print(f"Gym Location: {item[0]}, Classes Count: {item[1]}")
            
    elif question_number == 3 and len(sys.argv) == 3:
        classId = int(sys.argv[2])
        members = get_members_by_class(classId)
        if not members:
            print("No members found.")
            return
        print(f"Here are the members attending the class with ID {classId}.")
        for member in members:
            print(member)
            
    elif question_number == 4 and len(sys.argv) == 3:
        equipment_type = sys.argv[2]
        equipment = get_equipment_by_type(equipment_type)
        if not equipment:
            print(f"No equipment of type {equipment_type} found.")
            return
        print(f"Here is all equipment of type {equipment_type}.")
        for eq in equipment:
            print(eq)
            
    elif question_number == 5:
        expired_members = get_expired_members()
        if not expired_members:
            print("No expired members found.")
            return
        print("Here are all members with expired memberships.")
        for member in expired_members:
            print(member)
            
    elif question_number == 6 and len(sys.argv) == 3: # paramters are needed for certain questions
        instructorId = int(sys.argv[2])
        classes_taught = get_classes_taught(instructorId)
        if not classes_taught:
            print(f"No classes taught by instructor ID {instructorId} found.")
            return
        instructor_name, phone, _, _, _, _ = classes_taught[0]
        print(f"Instructor: {instructor_name}, Phone: {phone}, Classes Taught:")
        for class_info in classes_taught:
            _, _, class_name, class_type, duration, class_capacity = class_info
            print(f"Class: {class_name}, Class Type: {class_type}, Duration: {duration}, Capacity: {class_capacity}")
        
    elif question_number == 7:
        average_age = get_average_age_memberships()
        if isinstance(average_age, tuple):
            avg_active_age, avg_expired_age = average_age
            avg_active_age = round(avg_active_age)
            avg_expired_age = round(avg_expired_age)
            print(f"Average age for Active Memberships is {avg_active_age} years old.")
            print(f"Average age for Expired Memberships is {avg_expired_age} years old.")
        else:
            print(average_age)
        
    elif question_number == 8:
        instructors = get_top_instructors()
        print("Top 3 instructors: ")
        if not instructors:
            print("No instructors found.")
            return
        for The_best in instructors:
            print(The_best)
        
    elif question_number == 9 and len(sys.argv) == 3:
        class_type = sys.argv[2]
        members = members_attended_all(class_type)
        if not members:
            print(f"No members attending all classes of type {class_type} found.")
            return
        print(f"The members who attended all classes of type {class_type} are:")
        for member in members:
            print(member)

    elif question_number == 10:
        members = members_attended_last_month()
        if not members:
            print("No members who attended classes in the last month found.")
            return
        if len(members) > 0: # run only if there is any members within that category
            print("Recent Class Attendance:")
            print("Member Name    Total Classes Attended    Classes Attended     Class Types") # format a table
            print("=" * 90)
            for member in members:
                name, total_classes, attended_classes, class_types = member
                print(f"{name:<15} {total_classes:<25} {attended_classes:<30} {class_types}")

    else:
        print("Invalid input. You have a missing or invalid argument.")

if __name__ == "__main__": # main 
    main()
