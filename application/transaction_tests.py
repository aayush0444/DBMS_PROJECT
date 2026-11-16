
from db_connection import get_connection


# =====================================================
# TEST 1: ROLLBACK - REGISTER VENUE AND EDITION
# =====================================================

def rollback_venue_edition():

    connection = get_connection()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # First operation: successful venue insertion
        cursor.execute("""
            INSERT INTO VENUES
            (venue_name, venue_type, description)
            VALUES (%s, %s, %s)
        """, (
            "Rollback Test Venue",
            "Conference",
            "Testing transaction rollback"
        ))

        venue_id = cursor.lastrowid
        print("Venue inserted successfully.")

        # Second operation: deliberately invalid edition
        cursor.execute("""
            INSERT INTO VENUE_EDITIONS
            (venue_id, edition_name, submission_deadline, review_deadline)
            VALUES (%s, %s, %s, %s)
        """, (
            venue_id,
            None,
            "2027-01-15 23:59:59",
            "2027-02-15 23:59:59"
        ))

        connection.commit()
        print("Transaction committed.")

    except Exception as error:
        print("Expected failure:", error)

        # KEEP ACTIVE FOR ROLLBACK DEMONSTRATION
        connection.rollback()

        print("Venue and edition changes rolled back.")

    finally:
        cursor.close()
        connection.close()


# =====================================================
# TEST 2: ROLLBACK - SUBMIT RESEARCH PAPER
# =====================================================

def rollback_submission():

    connection = get_connection()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # First operation: insert submission
        cursor.execute("""
            INSERT INTO SUBMISSIONS
            (edition_id, title, abstract, status)
            VALUES (%s, %s, %s, %s)
        """, (
            101,
            "Rollback Test Paper",
            "Testing rollback during paper submission.",
            "Submitted"
        ))

        submission_id = cursor.lastrowid
        print("Submission inserted successfully.")

        # Second operation: insert manuscript version
        cursor.execute("""
            INSERT INTO MANUSCRIPT_VERSIONS
            (submission_id, version_no, file_url, change_summary)
            VALUES (%s, %s, %s, %s)
        """, (
            submission_id,
            1,
            "rollback_test.pdf",
            "Initial submission"
        ))

        version_id = cursor.lastrowid
        print("Manuscript version inserted successfully.")

        # Third operation: deliberately invalid author ID
        cursor.execute("""
            INSERT INTO VERSION_AUTHORS
            (version_id, user_id, author_order, is_corresponding)
            VALUES (%s, %s, %s, %s)
        """, (
            version_id,
            99999,
            1,
            True
        ))

        connection.commit()
        print("Transaction committed.")

    except Exception as error:
        print("Expected failure:", error)

        # KEEP ACTIVE FOR ROLLBACK DEMONSTRATION
        connection.rollback()

        print("Submission, version and author changes rolled back.")

    finally:
        cursor.close()
        connection.close()


# =====================================================
# TEST 3: ROLLBACK - ASSIGN REVIEWERS
# =====================================================

def rollback_reviewer_assignment():

    connection = get_connection()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # First operation: valid reviewer assignment
        cursor.execute("""
            INSERT INTO REVIEW_ASSIGNMENTS
            (version_id, reviewer_id, assigned_by, due_date, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            1002,
            3,
            1,
            "2026-11-25",
            "Pending"
        ))

        print("First reviewer assigned successfully.")

        # Second operation: deliberately invalid reviewer ID
        cursor.execute("""
            INSERT INTO REVIEW_ASSIGNMENTS
            (version_id, reviewer_id, assigned_by, due_date, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            1002,
            99999,
            1,
            "2026-11-25",
            "Pending"
        ))

        connection.commit()
        print("Transaction committed.")

    except Exception as error:
        print("Expected failure:", error)

        # KEEP ACTIVE FOR ROLLBACK DEMONSTRATION
        connection.rollback()

        print("All reviewer assignments rolled back.")

    finally:
        cursor.close()
        connection.close()


# =====================================================
# TEST 4: ROLLBACK - SUBMIT REVIEW
# =====================================================

def rollback_review():

    connection = get_connection()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # First operation: insert review for a pending assignment
        cursor.execute("""
            INSERT INTO REVIEWS
            (assignment_id, score, comments_to_author,
             comments_to_editor, recommendation)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            9003,
            8,
            "Rollback demonstration review.",
            "Testing transaction atomicity.",
            "Minor Revision"
        ))

        print("Review inserted successfully.")

        # Second operation: update assignment status
        cursor.execute("""
            UPDATE REVIEW_ASSIGNMENTS
            SET status = 'Completed'
            WHERE assignment_id = %s
        """, (9003,))

        print("Assignment status updated successfully.")

        # Deliberately invalid operation
        cursor.execute("""
            INSERT INTO REVIEWS
            (assignment_id, score, comments_to_author,
             comments_to_editor, recommendation)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            99999,
            8,
            "Invalid assignment test.",
            "This should fail.",
            "Accept"
        ))

        connection.commit()
        print("Transaction committed.")

    except Exception as error:
        print("Expected failure:", error)

        # KEEP ACTIVE FOR ROLLBACK DEMONSTRATION
        connection.rollback()

        print("Review insertion and assignment update rolled back.")

    finally:
        cursor.close()
        connection.close()


# =====================================================
# TEST 5: ROLLBACK - EDITORIAL DECISION
# =====================================================

def rollback_editorial_decision():

    connection = get_connection()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # First operation: update manuscript decision
        cursor.execute("""
            UPDATE MANUSCRIPT_VERSIONS
            SET decision_status = %s,
                editor_id = %s,
                decision_comments = %s,
                decided_at = NOW()
            WHERE version_id = %s
        """, (
            "Accepted",
            1,
            "Temporary rollback test decision.",
            1002
        ))

        print("Manuscript decision updated successfully.")

        # Second operation: update submission status
        cursor.execute("""
            UPDATE SUBMISSIONS
            SET status = %s
            WHERE submission_id = (
                SELECT submission_id
                FROM MANUSCRIPT_VERSIONS
                WHERE version_id = %s
            )
        """, (
            "Accepted",
            1002
        ))

        print("Submission status updated successfully.")

        # Deliberately invalid operation: invalid editor foreign key
        cursor.execute("""
            UPDATE MANUSCRIPT_VERSIONS
            SET editor_id = %s
            WHERE version_id = %s
        """, (
            99999,
            1002
        ))

        connection.commit()
        print("Transaction committed.")

    except Exception as error:
        print("Expected failure:", error)

        # KEEP ACTIVE FOR ROLLBACK DEMONSTRATION
        connection.rollback()

        print("Editorial decision and submission status rolled back.")

    finally:
        cursor.close()
        connection.close()
