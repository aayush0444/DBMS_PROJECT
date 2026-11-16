
from db_connection import get_connection


def record_editorial_decision(
    version_id,
    editor_id,
    decision_status,
    decision_comments
):
    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # Step 1: Find the venue associated with this version
        cursor.execute("""
            SELECT ve.venue_id, s.submission_id
            FROM MANUSCRIPT_VERSIONS mv
            JOIN SUBMISSIONS s
                ON mv.submission_id = s.submission_id
            JOIN VENUE_EDITIONS ve
                ON s.edition_id = ve.edition_id
            WHERE mv.version_id = %s
        """, (version_id,))

        result = cursor.fetchone()

        if result is None:
            raise ValueError("Manuscript version does not exist.")

        venue_id, submission_id = result

        # Step 2: Verify that the user is an editor of this venue
        cursor.execute("""
            SELECT COUNT(*)
            FROM VENUE_ROLES
            WHERE user_id = %s
              AND venue_id = %s
              AND LOWER(role) = 'editor'
        """, (editor_id, venue_id))

        if cursor.fetchone()[0] == 0:
            raise ValueError("User is not an editor of this venue.")

        # Step 3: Record the editorial decision
        cursor.execute("""
            UPDATE MANUSCRIPT_VERSIONS
            SET decision_status = %s,
                editor_id = %s,
                decision_comments = %s,
                decided_at = NOW()
            WHERE version_id = %s
        """, (
            decision_status,
            editor_id,
            decision_comments,
            version_id
        ))

        # Step 4: Update the overall submission status
        cursor.execute("""
            UPDATE SUBMISSIONS
            SET status = %s
            WHERE submission_id = %s
        """, (decision_status, submission_id))

        connection.commit()

        print("Editorial decision recorded successfully!")

        return True

    except Exception as error:
        connection.rollback()
        print("Editorial decision failed:", error)
        return False

    finally:
        cursor.close()
        connection.close()
