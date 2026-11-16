
from db_connection import get_connection


def submit_research_paper(
    edition_id,
    title,
    abstract,
    file_url,
    authors,
    status="Submitted",
    change_summary="Initial submission"
):
    connection = get_connection()

    if connection is None:
        return False

    if not authors:
        print("At least one author is required.")
        connection.close()
        return False

    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # Step 1: Create the submission
        cursor.execute("""
            INSERT INTO SUBMISSIONS
            (edition_id, title, abstract, status)
            VALUES (%s, %s, %s, %s)
        """, (edition_id, title, abstract, status))

        submission_id = cursor.lastrowid

        # Step 2: Create the first manuscript version
        cursor.execute("""
            INSERT INTO MANUSCRIPT_VERSIONS
            (submission_id, version_no, file_url, change_summary)
            VALUES (%s, %s, %s, %s)
        """, (
            submission_id,
            1,
            file_url,
            change_summary
        ))

        version_id = cursor.lastrowid

        # Step 3: Register all authors
        for user_id, author_order, is_corresponding in authors:
            cursor.execute("""
                INSERT INTO VERSION_AUTHORS
                (version_id, user_id, author_order, is_corresponding)
                VALUES (%s, %s, %s, %s)
            """, (
                version_id,
                user_id,
                author_order,
                is_corresponding
            ))

        connection.commit()

        print("Research paper submitted successfully!")

        return submission_id, version_id

    except Exception as error:
        connection.rollback()
        print("Submission failed:", error)
        return False

    finally:
        cursor.close()
        connection.close()
