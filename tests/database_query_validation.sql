SELECT
    s.submission_id,
    s.title,
    mv.version_no,
    reviewer.full_name AS reviewer_name,
    ra.status AS assignment_status,
    r.score,
    r.recommendation,
    r.comments_to_author

FROM SUBMISSIONS s

JOIN MANUSCRIPT_VERSIONS mv
    ON s.submission_id = mv.submission_id

JOIN REVIEW_ASSIGNMENTS ra
    ON mv.version_id = ra.version_id

JOIN USERS reviewer
    ON ra.reviewer_id = reviewer.user_id

LEFT JOIN REVIEWS r
    ON ra.assignment_id = r.assignment_id

WHERE s.submission_id = 501

ORDER BY mv.version_no, ra.assignment_id;


-- =====================================================
-- TEST 2: RETRIEVE AUTHORS OF EACH MANUSCRIPT VERSION
-- =====================================================
-- PURPOSE:
-- 1. Display each manuscript and its version.
-- 2. Retrieve all authors associated with that version.
-- 3. Display their author order.
-- 4. Identify the corresponding author.
--
-- RELATIONSHIPS TESTED:
-- SUBMISSIONS -> MANUSCRIPT_VERSIONS
-- MANUSCRIPT_VERSIONS -> VERSION_AUTHORS
-- VERSION_AUTHORS -> USERS
-- =====================================================

SELECT
    s.submission_id,
    s.title,
    mv.version_no,
    u.full_name AS author_name,
    va.author_order,
    va.is_corresponding

FROM SUBMISSIONS s

JOIN MANUSCRIPT_VERSIONS mv
    ON s.submission_id = mv.submission_id

JOIN VERSION_AUTHORS va
    ON mv.version_id = va.version_id

JOIN USERS u
    ON va.user_id = u.user_id

ORDER BY
    s.submission_id,
    mv.version_no,
    va.author_order;
    
    
-- =====================================================
-- TEST 3: RETRIEVE REVIEWER ASSIGNMENTS
-- =====================================================
-- PURPOSE:
-- 1. Display each manuscript and its version.
-- 2. Identify the reviewer assigned to that version.
-- 3. Identify the editor who assigned the reviewer.
-- 4. Display assignment date, deadline and status.
--
-- RELATIONSHIPS TESTED:
-- SUBMISSIONS -> MANUSCRIPT_VERSIONS
-- MANUSCRIPT_VERSIONS -> REVIEW_ASSIGNMENTS
-- REVIEW_ASSIGNMENTS -> USERS (reviewer)
-- REVIEW_ASSIGNMENTS -> USERS (assigned_by/editor)
-- =====================================================

SELECT
    s.submission_id,
    s.title,
    mv.version_no,
    reviewer.full_name AS reviewer_name,
    editor.full_name AS assigned_by,
    ra.assigned_at,
    ra.due_date,
    ra.status AS assignment_status

FROM SUBMISSIONS s

JOIN MANUSCRIPT_VERSIONS mv
    ON s.submission_id = mv.submission_id

JOIN REVIEW_ASSIGNMENTS ra
    ON mv.version_id = ra.version_id

JOIN USERS reviewer
    ON ra.reviewer_id = reviewer.user_id

JOIN USERS editor
    ON ra.assigned_by = editor.user_id

ORDER BY
    s.submission_id,
    mv.version_no,
    ra.assignment_id;