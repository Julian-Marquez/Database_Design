-- Add class assignments for instructors (Questions 6 + 8)
INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId) VALUES
('Lunchtime Yoga', 'Yoga', 60, 20, 1, 2),
('HIIT Cardio', 'Cardio', 45, 30, 2, 3),
('Bodybuilding Basics', 'Weight-Lifting', 90, 15, 3, 1);

-- Make sure there are active and expired memberships (Question 7)
UPDATE Member SET membershipStartDate = '2023-1-31' WHERE name = 'Alice Johnson';
UPDATE Member SET membershipEndDate = '2023-12-31' WHERE name = 'Alice Johnson';
UPDATE Member SET membershipEndDate = '2026-01-01' WHERE name = 'Bob Brown';

-- More Attendance Records for Questions 9 & 10
INSERT INTO Attends (memberId, classId, attendanceDate) VALUES
(1, 1, '2024-03-15'),
(1, 6, '2024-03-20'),
(2, 2, '2025-04-10'), 
(2, 7, '2025-04-15'), 
(3, 3, '2025-04-25'); 
