
PRAGMA foreign_keys = ON;

--Tables to be made in Database

-- Create Member table
CREATE TABLE Member (
    memberId INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(100),
    age INTEGER CHECK (age >= 15),
    membershipStartDate TEXT NOT NULL,
    membershipEndDate TEXT NOT NULL CHECK (membershipEndDate >= membershipStartDate)
);

--Instructor table
CREATE TABLE Instructor (
    instructorId INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    specialty VARCHAR(50),
    phone VARCHAR(15),
    email VARCHAR(100) NOT NULL
);


-- GymFacility table
CREATE TABLE GymFacility (
    gymId INTEGER PRIMARY KEY AUTOINCREMENT,
    location VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    manager VARCHAR(50)
);

-- Class table
CREATE TABLE Class (
    classId INTEGER PRIMARY KEY AUTOINCREMENT,
    className VARCHAR(50) NOT NULL,
    classType VARCHAR(20) CHECK (classType IN ('Yoga', 'Acrobats', 'Cardio', 'Weight-Lifting')),
    duration INTEGER NOT NULL,
    classCapacity INTEGER NOT NULL,
    instructorId INTEGER,
    gymId INTEGER,
    FOREIGN KEY (instructorId) REFERENCES Instructor(instructorId),
    FOREIGN KEY (gymId) REFERENCES GymFacility(gymId)
);

-- Equipment table
CREATE TABLE Equipment (
    equipmentId INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(30) CHECK (type IN ('Cardio', 'Flexibility', 'Recovery','Strength')),
    quantity INTEGER,
    gymId INTEGER,
    FOREIGN KEY (gymId) REFERENCES GymFacility(gymId)
);

-- MembershipPlan table
CREATE TABLE MembershipPlan (
    planId INTEGER PRIMARY KEY AUTOINCREMENT,
    planType VARCHAR(20) CHECK (planType IN ('Monthly', 'Annual')),
    cost NUMERIC NOT NULL
);

-- Payment table
CREATE TABLE Payment (
    paymentId INTEGER PRIMARY KEY AUTOINCREMENT,
    memberId INTEGER,
    planId INTEGER,
    amountPaid REAL NOT NULL,
    paymentDate TEXT NOT NULL,
    FOREIGN KEY (memberId) REFERENCES Member(memberId),
    FOREIGN KEY (planId) REFERENCES MembershipPlan(planId)
);

--  Attendence table
CREATE TABLE Attends (
    memberId INTEGER,
    classId INTEGER,
    attendanceDate TEXT NOT NULL, 
    PRIMARY KEY (memberId, classId, attendanceDate),
    FOREIGN KEY (memberId) REFERENCES Member(memberId),
    FOREIGN KEY (classId) REFERENCES Class(classId)
);
