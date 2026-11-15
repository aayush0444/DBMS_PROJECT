-- =====================================================
-- TEST 1: DUPLICATE EMAIL VALIDATION
-- =====================================================
-- PURPOSE:
-- Verify that two users cannot register with the same email.
--
-- CONSTRAINT TESTED:
-- USERS.email -> UNIQUE
--
-- EXPECTED RESULT:
-- MySQL rejects the INSERT because the email already exists.
-- Expected error: Duplicate entry.
-- =====================================================

INSERT INTO USERS
(full_name, email, password_hash, affiliation)
VALUES
('Test User', 'meera@university.edu',
 SHA2('Test123', 256), 'Test University');
 
 -- =====================================================
-- TEST 2: INVALID FOREIGN KEY VALIDATION
-- =====================================================
-- PURPOSE:
-- Verify that a submission cannot reference a
-- non-existent venue edition.
--
-- CONSTRAINT TESTED:
-- SUBMISSIONS.edition_id -> VENUE_EDITIONS.edition_id
--
-- EXPECTED RESULT:
-- MySQL rejects the INSERT because edition_id 999
-- does not exist.
-- =====================================================

INSERT INTO SUBMISSIONS
(edition_id, title, abstract)
VALUES
(999, 'Invalid Test Paper',
 'This paper references a non-existent edition.');
 
 
 -- =====================================================
-- TEST 3: DUPLICATE REVIEW VALIDATION
-- =====================================================
-- PURPOSE:
-- Verify that one review assignment cannot have
-- multiple review records.
--
-- CONSTRAINT TESTED:
-- REVIEWS.assignment_id -> UNIQUE
--
-- EXPECTED RESULT:
-- MySQL rejects the INSERT because assignment_id 9001
-- already has a review.
-- =====================================================

INSERT INTO REVIEWS
(assignment_id, score, comments_to_author,
 comments_to_editor, recommendation)
VALUES
(9001, 9, 'Duplicate review test',
 'Testing unique constraint.',
 'Accept');
 
-- =====================================================
-- TEST 4: INVALID AUTHOR ORDER VALIDATION
-- =====================================================
-- PURPOSE:
-- Verify that author_order must be greater than zero.
--
-- CONSTRAINT TESTED:
-- VERSION_AUTHORS.author_order CHECK (author_order > 0)
--
-- EXPECTED RESULT:
-- MySQL rejects the INSERT because author_order = 0.
-- Requires MySQL 8.0.16 or later for CHECK enforcement.
-- =====================================================

INSERT INTO VERSION_AUTHORS
(version_id, user_id, author_order, is_corresponding)
VALUES
(1001, 12, 0, 0);