USE academic_review_system;

START TRANSACTION;

-- 1. VENUES
INSERT INTO VENUES
(venue_id, venue_name, venue_type, description)
VALUES
(1, 'International Conference on AI Research', 'Conference',
 'Conference focusing on artificial intelligence and machine learning.'),
(2, 'Journal of Computer Science Research', 'Journal',
 'Academic journal covering computer science research.'),
(3, 'International Conference on Data Science', 'Conference',
 'Conference focusing on data analytics and data science.');


-- 2. USERS
INSERT INTO USERS
(user_id, full_name, email, password_hash, affiliation)
VALUES
(1, 'Dr. Meera Sharma', 'meera@university.edu', SHA2('Meera123',256), 'IIT Delhi'),
(2, 'Dr. Arjun Verma', 'arjun@university.edu', SHA2('Arjun123',256), 'IIT Bombay'),
(3, 'Dr. Neha Kapoor', 'neha@university.edu', SHA2('Neha123',256), 'IIT Kanpur'),
(4, 'Aditi Singh', 'aditi@student.edu', SHA2('Aditi123',256), 'IIT Jammu'),
(5, 'Rohan Gupta', 'rohan@student.edu', SHA2('Rohan123',256), 'IIT Jammu'),
(6, 'Sana Khan', 'sana@student.edu', SHA2('Sana123',256), 'IIT Delhi'),
(7, 'Prof. Rajesh Iyer', 'rajesh@university.edu', SHA2('Rajesh123',256), 'IIT Madras'),
(8, 'Dr. Kabir Malhotra', 'kabir@university.edu', SHA2('Kabir123',256), 'IIT Roorkee'),
(9, 'Dr. Nisha Rao', 'nisha@university.edu', SHA2('Nisha123',256), 'IIT Hyderabad'),
(10, 'Vikram Patel', 'vikram@student.edu', SHA2('Vikram123',256), 'IIT Bombay'),
(11, 'Priya Nair', 'priya@student.edu', SHA2('Priya123',256), 'IIT Jammu'),
(12, 'Dr. Amit Bose', 'amit@university.edu', SHA2('Amit123',256), 'IIT Kharagpur');


-- 3. VENUE_EDITIONS
INSERT INTO VENUE_EDITIONS
(edition_id, venue_id, edition_name, submission_deadline, review_deadline)
VALUES
(101, 1, 'AI Research Conference 2026',
 '2026-03-15 23:59:00', '2026-05-15 23:59:00'),
(102, 2, 'Volume 12 Issue 1',
 '2026-04-15 23:59:00', '2026-06-15 23:59:00'),
(103, 3, 'Data Science Summit 2026',
 '2026-05-15 23:59:00', '2026-07-15 23:59:00');


-- 4. VENUE_ROLES
INSERT INTO VENUE_ROLES
(user_id, venue_id, role)
VALUES
(1, 1, 'Editor'),
(2, 1, 'Reviewer'),
(3, 1, 'Reviewer'),
(4, 1, 'Author'),
(5, 1, 'Author'),
(6, 1, 'Author'),

(7, 2, 'Editor'),
(8, 2, 'Reviewer'),
(9, 2, 'Reviewer'),
(10, 2, 'Author'),
(11, 2, 'Author'),

(12, 3, 'Editor'),
(2, 3, 'Reviewer'),
(8, 3, 'Reviewer'),
(4, 3, 'Author'),
(10, 3, 'Author');


-- 5. SUBMISSIONS
INSERT INTO SUBMISSIONS
(submission_id, edition_id, title, abstract, submitted_at, status)
VALUES
(501, 101,
 'Deep Learning Based Image Classification',
 'A study of deep learning methods for accurate image classification.',
 '2026-02-10 10:30:00', 'Under Review'),

(502, 101,
 'Machine Learning for Healthcare Prediction',
 'A machine learning approach for predicting healthcare outcomes.',
 '2026-02-20 11:00:00', 'Under Review'),

(503, 102,
 'Efficient Algorithms for Big Data Processing',
 'An analysis of efficient algorithms for processing large datasets.',
 '2026-03-12 14:00:00', 'Under Review'),

(504, 103,
 'Data Mining Techniques for Smart Cities',
 'A study of data mining techniques for smart city applications.',
 '2026-04-05 09:30:00', 'Under Review');


-- 6. MANUSCRIPT_VERSIONS
INSERT INTO MANUSCRIPT_VERSIONS
(version_id, submission_id, version_no, file_url, uploaded_at,
 change_summary, decision_status, editor_id, decision_comments, decided_at)
VALUES
(1001, 501, 1, 'https://example.com/papers/501_v1.pdf',
 '2026-02-10 10:30:00', 'Initial manuscript submission',
 'Revision Required', 1, 'Please improve the experimental analysis.',
 '2026-03-20 12:00:00'),

(1002, 501, 2, 'https://example.com/papers/501_v2.pdf',
 '2026-04-01 10:00:00', 'Revised experiments and improved methodology',
 'Pending', NULL, NULL, NULL),

(1003, 502, 1, 'https://example.com/papers/502_v1.pdf',
 '2026-02-20 11:00:00', 'Initial manuscript submission',
 'Under Review', NULL, NULL, NULL),

(2001, 503, 1, 'https://example.com/papers/503_v1.pdf',
 '2026-03-12 14:00:00', 'Initial manuscript submission',
 'Under Review', NULL, NULL, NULL),

(3001, 504, 1, 'https://example.com/papers/504_v1.pdf',
 '2026-04-05 09:30:00', 'Initial manuscript submission',
 'Under Review', NULL, NULL, NULL);


-- 7. VERSION_AUTHORS
INSERT INTO VERSION_AUTHORS
(version_id, user_id, author_order, is_corresponding)
VALUES
(1001, 4, 1, 1),
(1001, 5, 2, 0),

(1002, 4, 1, 1),
(1002, 5, 2, 0),

(1003, 6, 1, 1),
(1003, 4, 2, 0),

(2001, 10, 1, 1),
(2001, 11, 2, 0),

(3001, 4, 1, 1),
(3001, 10, 2, 0);


-- 8. REVIEW_ASSIGNMENTS
INSERT INTO REVIEW_ASSIGNMENTS
(assignment_id, version_id, reviewer_id, assigned_by,
 assigned_at, due_date, status)
VALUES
(9001, 1001, 2, 1, '2026-02-15 10:00:00',
 '2026-03-10 23:59:00', 'Completed'),

(9002, 1001, 3, 1, '2026-02-15 11:00:00',
 '2026-03-10 23:59:00', 'Completed'),

(9003, 1002, 2, 1, '2026-04-02 10:00:00',
 '2026-04-20 23:59:00', 'Pending'),

(9004, 1003, 3, 1, '2026-02-25 10:00:00',
 '2026-03-25 23:59:00', 'Completed'),

(9005, 2001, 8, 7, '2026-03-15 10:00:00',
 '2026-04-15 23:59:00', 'Completed'),

(9006, 2001, 9, 7, '2026-03-15 11:00:00',
 '2026-04-15 23:59:00', 'Pending'),

(9007, 3001, 2, 12, '2026-04-10 10:00:00',
 '2026-05-10 23:59:00', 'Completed'),

(9008, 3001, 8, 12, '2026-04-10 11:00:00',
 '2026-05-10 23:59:00', 'Pending');


-- 9. REVIEWS
INSERT INTO REVIEWS
(review_id, assignment_id, score, comments_to_author,
 comments_to_editor, recommendation, submitted_at)
VALUES
(8001, 9001, 8,
 'Good research work. Minor improvements are required.',
 'The methodology is sound but the experiments need improvement.',
 'Minor Revision', '2026-03-01 12:00:00'),

(8002, 9002, 7,
 'The paper is interesting but needs stronger experimental results.',
 'Recommend revision before acceptance.',
 'Major Revision', '2026-03-05 14:00:00'),

(8003, 9004, 9,
 'Well-written paper with a clear methodology.',
 'The paper is suitable for publication.',
 'Accept', '2026-03-15 10:00:00'),

(8004, 9005, 6,
 'The proposed algorithm requires further optimization.',
 'Significant improvements are needed.',
 'Major Revision', '2026-04-05 16:00:00'),

(8005, 9007, 8,
 'Good contribution to smart city research.',
 'Minor changes are recommended.',
 'Minor Revision', '2026-04-25 11:00:00');

COMMIT;