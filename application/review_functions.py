
from db_connection import get_connection


def submit_review(
    assignment_id,
    score,
    comments_to_author,
    comments_to_editor,
    recommendation
):
    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # Step 1: Check whether assignment exists and is pending
        cursor.execute("""
            SELECT status
            FROM REVIEW_ASSIGNMENTS
            WHERE assignment_id = %s
        """, (assignment_id,))

        result = cursor.fetchone()

        if result is None:
            raise ValueError("Review assignment does not exist.")

        if result[0] != "Pending":
            raise ValueError("This assignment is not pending.")

        # Step 2: Insert the review
        cursor.execute("""
            INSERT INTO REVIEWS
            (
                assignment_id,
                score,
                comments_to_author,
                comments_to_editor,
                recommendation
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            assignment_id,
            score,
            comments_to_author,
            comments_to_editor,
            recommendation
        ))

        review_id = cursor.lastrowid

        # Step 3: Mark assignment as completed
        cursor.execute("""
            UPDATE REVIEW_ASSIGNMENTS
            SET status = 'Completed'
            WHERE assignment_id = %s
        """, (assignment_id,))

        connection.commit()

        print("Review submitted successfully!")

        return review_id

    except Exception as error:
        connection.rollback()
        print("Review submission failed:", error)
        return False

    finally:
        cursor.close()
        connection.close()
