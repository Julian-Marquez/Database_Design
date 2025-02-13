-- Insert Member records
INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate) VALUES
('John Doe', 'johnd@email.com', '1234567890', '123 Main St', 25, '2024-01-01', '2025-01-01'),
('Jane Smith', 'janes@email.com', '9876543210', '456 Oak St', 30, '2024-02-01', '2025-02-01'),
('Alice Johnson', 'alicej@email.com', '5556667777', '789 Pine St', 40, '2024-03-01', '2024-04-01'),
('Bob Brown', 'bobb@email.com', '2223334444', '321 Street St', 35, '2024-04-01', '2025-04-01'),
('Maria Garcia', 'mariag@email.com', '9998887777', '654 Green St', 28, '2024-05-01', '2025-05-01');

-- Insert Instructor records
INSERT INTO Instructor (name, specialty, phone, email) VALUES
('James Johnson', 'Yoga', '1231231234', 'jamesj@email.com'),
('Sarah Smith', 'Cardio', '4564564567', 'sarah@email.com'),
('Tom Harris', 'Weight-Lifting', '7897897890', 'tomh@email.com'),
('Laura Wilson', 'Acrobatics', '3213213210', 'lauraw@email.com'),
('Emma Davis', 'Cardio', '6546546543', 'emmad@email.com');

-- Insert GymFacility records
INSERT INTO GymFacility (location, phone, manager) VALUES
('Downtown', '1112223333', 'Mark Spencer'),
('Uptown', '4445556666', 'Anna Bell'),
('Suburb', '7778889999', 'Chris Jordan'),
('City Center', '1213141516', 'Katie Green'),
('Westside', '1718192021', 'James Carter');

-- Insert Class records
INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId) VALUES
('Morning Yoga', 'Yoga', 60, 20, 1, 1),
('Evening Cardio', 'Cardio', 45, 25, 2, 2),
('Strength Training', 'Weight-Lifting', 90, 15, 3, 3),
('Acrobatics Basics', 'Acrobatics', 75, 10, 4, 4),
('Advanced Cardio', 'Cardio', 50, 30, 5, 5);

-- Insert Equipment records
INSERT INTO Equipment (name, type, quantity, gymId) VALUES
('Treadmill', 'Cardio', 5, 2),
('Barbell', 'Strength', 2, 3),
('Resistance Band', 'Flexibility', 20, 4),
('Foam Roller', 'Recovery', 2, 1),
('Stair Climber', 'Cardio', 10, 5);

-- Insert MembershipPlan records
INSERT INTO MembershipPlan (planType, cost) VALUES
('Monthly', 20),
('Annual', 200);

-- Insert Payment records
INSERT INTO Payment (memberId, planId, amountPaid, paymentDate) VALUES
(1, 1, 200, '2024-01-01'),
(2, 1, 200, '2024-02-01'),
(3, 2, 20, '2024-03-01'),
(4, 1, 200, '2024-04-01'),
(5, 2, 200, '2024-05-01');

-- Insert Attendence measures
INSERT INTO Attendance (memberId, classId, attendanceDate) VALUES
(1, 2, '2024-01-03'),
(2, 4, '2024-04-21'),
(3, 5, '2024-03-14'),
(4, 3, '2024-11-19'),
(5, 1, '2024-07-14');
