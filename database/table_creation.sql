
USE academic_review_system;

-- 1. VENUES
CREATE TABLE VENUES (
    venue_id INT AUTO_INCREMENT,
    venue_name VARCHAR(200) NOT NULL,
    venue_type VARCHAR(30) NOT NULL,
    description TEXT,

    PRIMARY KEY (venue_id)
) ENGINE=InnoDB;


-- 2. USERS
CREATE TABLE USERS (
    user_id INT AUTO_INCREMENT,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    affiliation VARCHAR(200),

    PRIMARY KEY (user_id),
    UNIQUE (email)
) ENGINE=InnoDB;


-- 3. VENUE_EDITIONS
CREATE TABLE VENUE_EDITIONS (
    edition_id INT AUTO_INCREMENT,
    venue_id INT NOT NULL,
    edition_name VARCHAR(150) NOT NULL,
    submission_deadline DATETIME,
    review_deadline DATETIME,

    PRIMARY KEY (edition_id),

    FOREIGN KEY (venue_id)
        REFERENCES VENUES(venue_id)
) ENGINE=InnoDB;


-- 4. SUBMISSIONS
CREATE TABLE SUBMISSIONS (
    submission_id INT AUTO_INCREMENT,
    edition_id INT NOT NULL,
    title VARCHAR(300) NOT NULL,
    abstract TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'Submitted',

    PRIMARY KEY (submission_id),

    FOREIGN KEY (edition_id)
        REFERENCES VENUE_EDITIONS(edition_id)
) ENGINE=InnoDB;


-- 5. MANUSCRIPT_VERSIONS
CREATE TABLE MANUSCRIPT_VERSIONS (
    version_id INT AUTO_INCREMENT,
    submission_id INT NOT NULL,
    version_no INT NOT NULL,
    file_url VARCHAR(500),
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    change_summary TEXT,
    decision_status VARCHAR(30),
    editor_id INT,
    decision_comments TEXT,
    decided_at DATETIME,

    PRIMARY KEY (version_id),

    UNIQUE (submission_id, version_no),

    FOREIGN KEY (submission_id)
        REFERENCES SUBMISSIONS(submission_id),

    FOREIGN KEY (editor_id)
        REFERENCES USERS(user_id)
) ENGINE=InnoDB;


-- 6. VENUE_ROLES
CREATE TABLE VENUE_ROLES (
    user_id INT NOT NULL,
    venue_id INT NOT NULL,
    role VARCHAR(50) NOT NULL,

    PRIMARY KEY (user_id, venue_id, role),

    FOREIGN KEY (user_id)
        REFERENCES USERS(user_id),

    FOREIGN KEY (venue_id)
        REFERENCES VENUES(venue_id)
) ENGINE=InnoDB;


-- 7. VERSION_AUTHORS
CREATE TABLE VERSION_AUTHORS (
    version_id INT NOT NULL,
    user_id INT NOT NULL,
    author_order INT NOT NULL,
    is_corresponding BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (version_id, user_id),

    UNIQUE (version_id, author_order),

    CHECK (author_order > 0),

    FOREIGN KEY (version_id)
        REFERENCES MANUSCRIPT_VERSIONS(version_id),

    FOREIGN KEY (user_id)
        REFERENCES USERS(user_id)
) ENGINE=InnoDB;


-- 8. REVIEW_ASSIGNMENTS
CREATE TABLE REVIEW_ASSIGNMENTS (
    assignment_id INT AUTO_INCREMENT,
    version_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    assigned_by INT NOT NULL,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME,
    status VARCHAR(30) DEFAULT 'Assigned',

    PRIMARY KEY (assignment_id),

    FOREIGN KEY (version_id)
        REFERENCES MANUSCRIPT_VERSIONS(version_id),

    FOREIGN KEY (reviewer_id)
        REFERENCES USERS(user_id),

    FOREIGN KEY (assigned_by)
        REFERENCES USERS(user_id)
) ENGINE=InnoDB;


-- 9. REVIEWS
CREATE TABLE REVIEWS (
    review_id INT AUTO_INCREMENT,
    assignment_id INT NOT NULL,
    score DECIMAL(5,2),
    comments_to_author TEXT,
    comments_to_editor TEXT,
    recommendation VARCHAR(50),
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (review_id),

    UNIQUE (assignment_id),

    FOREIGN KEY (assignment_id)
        REFERENCES REVIEW_ASSIGNMENTS(assignment_id)
) ENGINE=InnoDB;



USE academic_review_system;

SHOW TABLES;

-- Check individual table structures
DESCRIBE VENUES;
DESCRIBE USERS;
DESCRIBE VENUE_EDITIONS;
DESCRIBE SUBMISSIONS;
DESCRIBE MANUSCRIPT_VERSIONS;
DESCRIBE VENUE_ROLES;
DESCRIBE VERSION_AUTHORS;
DESCRIBE REVIEW_ASSIGNMENTS;
DESCRIBE REVIEWS;

