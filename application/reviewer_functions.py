
from db_connection import get_connection


def assign_reviewers(version_id, reviewer_ids, assigned_by, due_date):
    connection = get_connection()

    if connection is None:
        return False

    if not reviewer_ids:
        print("At least one reviewer is required.")
        connection.close()
        return False

    if len(reviewer_ids) != len(set(reviewer_ids)):
        print("Duplicate reviewer IDs are not allowed.")
        connection.close()
        return False

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # Step 1: Find the venue associated with this version
        cursor.execute("""
            SELECT ve.venue_id
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

        venue_id = result[0]

        # Step 2: Check whether the assigning user is an editor
        cursor.execute("""
            SELECT COUNT(*)
            FROM VENUE_ROLES
            WHERE user_id = %s
              AND venue_id = %s
              AND LOWER(role) = 'editor'
        """, (assigned_by, venue_id))

        if cursor.fetchone()[0] == 0:
            raise ValueError("Assigning user is not an editor of this venue.")

        # Step 3: Insert assignments for each reviewer
        for reviewer_id in reviewer_ids:

            # Check whether the user is a reviewer for this venue
            cursor.execute("""
                SELECT COUNT(*)
                FROM VENUE_ROLES
                WHERE user_id = %s
                  AND venue_id = %s
                  AND LOWER(role) = 'reviewer'
            """, (reviewer_id, venue_id))

            if cursor.fetchone()[0] == 0:
                raise ValueError(
                    f"User {reviewer_id} is not a reviewer for this venue."
                )

            # Prevent duplicate assignments
            cursor.execute("""
                SELECT COUNT(*)
                FROM REVIEW_ASSIGNMENTS
                WHERE version_id = %s AND reviewer_id = %s
            """, (version_id, reviewer_id))

            if cursor.fetchone()[0] > 0:
                raise ValueError(
                    f"Reviewer {reviewer_id} is already assigned."
                )

            cursor.execute("""
                INSERT INTO REVIEW_ASSIGNMENTS
                (version_id, reviewer_id, assigned_by, due_date, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                version_id,
                reviewer_id,
                assigned_by,
                due_date,
                "Pending"
            ))

        connection.commit()

        print("Reviewer assignments created successfully!")

        return True

    except Exception as error:
        connection.rollback()
        print("Reviewer assignment failed:", error)
        return False

    finally:
        cursor.close()
        connection.close()
