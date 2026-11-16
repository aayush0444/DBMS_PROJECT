
from db_connection import get_connection


def register_venue_and_edition(
    venue_name,
    venue_type,
    description,
    edition_name,
    submission_deadline,
    review_deadline
):
    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # Step 1: Register the venue
        cursor.execute("""
            INSERT INTO VENUES
            (venue_name, venue_type, description)
            VALUES (%s, %s, %s)
        """, (venue_name, venue_type, description))

        venue_id = cursor.lastrowid

        # Step 2: Register an edition for that venue
        cursor.execute("""
            INSERT INTO VENUE_EDITIONS
            (venue_id, edition_name, submission_deadline, review_deadline)
            VALUES (%s, %s, %s, %s)
        """, (
            venue_id,
            edition_name,
            submission_deadline,
            review_deadline
        ))

        edition_id = cursor.lastrowid

        connection.commit()

        print("Venue and edition registered successfully!")

        return venue_id, edition_id

    except Exception as error:
        connection.rollback()
        print("Registration failed:", error)
        return False

    finally:
        cursor.close()
        connection.close()
