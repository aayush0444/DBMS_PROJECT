
# =====================================================
# CONFERENCE AND JOURNAL ACADEMIC REVIEW SYSTEM
# MAIN APPLICATION
# =====================================================

# Import five prototype functions
from venue_functions import register_venue_and_edition
from submission_functions import submit_research_paper
from reviewer_functions import assign_reviewers
from review_functions import submit_review
from decision_functions import record_editorial_decision

# Import five transaction rollback demonstrations
from transaction_tests import (
    rollback_venue_edition,
    rollback_submission,
    rollback_reviewer_assignment,
    rollback_review,
    rollback_editorial_decision
)


# =====================================================
# MAIN MENU
# =====================================================

while True:

    print("\n==============================================")
    print("       ACADEMIC REVIEW MANAGEMENT SYSTEM")
    print("==============================================")

    print("\n---------- PROTOTYPE FUNCTIONS ----------")

    print("1. Register Venue and Edition")
    print("2. Submit Research Paper")
    print("3. Assign Reviewers")
    print("4. Submit Review")
    print("5. Record Editorial Decision")

    print("\n---------- TRANSACTION ROLLBACK TESTS ----------")

    print("6. Rollback - Register Venue and Edition")
    print("7. Rollback - Submit Research Paper")
    print("8. Rollback - Assign Reviewers")
    print("9. Rollback - Submit Review")
    print("10. Rollback - Editorial Decision")

    print("\n0. Exit")

    choice = input("\nEnter your choice: ")


    # =================================================
    # PROTOTYPE 1: REGISTER VENUE AND EDITION
    # =================================================

    if choice == "1":

        print("\n--- Register Venue and Edition ---")

        result = register_venue_and_edition(
            venue_name="Test Conference",
            venue_type="Conference",
            description="Testing venue registration",
            edition_name="Test Edition 2027",
            submission_deadline="2027-01-15 23:59:59",
            review_deadline="2027-02-15 23:59:59"
        )

        print("Result:", result)


    # =================================================
    # PROTOTYPE 2: SUBMIT RESEARCH PAPER
    # =================================================

    elif choice == "2":

        print("\n--- Submit Research Paper ---")

        result = submit_research_paper(
            edition_id=101,
            title="Testing New Research Paper",
            abstract="Sample abstract for testing.",
            file_url="paper.pdf",
            authors=[
                (4, 1, True),
                (5, 2, False)
            ]
        )

        print("Result:", result)


    # =================================================
    # PROTOTYPE 3: ASSIGN REVIEWERS
    # =================================================

    elif choice == "3":

        print("\n--- Assign Reviewers ---")

        result = assign_reviewers(
            version_id=1002,
            reviewer_ids=[3],
            assigned_by=1,
            due_date="2026-11-25"
        )

        print("Result:", result)


    # =================================================
    # PROTOTYPE 4: SUBMIT REVIEW
    # =================================================

    elif choice == "4":

        print("\n--- Submit Review ---")

        result = submit_review(
            assignment_id=9003,
            score=8,
            comments_to_author="Good research work.",
            comments_to_editor="Minor improvements required.",
            recommendation="Minor Revision"
        )

        print("Result:", result)


    # =================================================
    # PROTOTYPE 5: RECORD EDITORIAL DECISION
    # =================================================

    elif choice == "5":

        print("\n--- Record Editorial Decision ---")

        result = record_editorial_decision(
            version_id=1002,
            editor_id=1,
            decision_status="Accepted",
            decision_comments="The manuscript is accepted."
        )

        print("Result:", result)


    # =================================================
    # TRANSACTION ROLLBACK DEMONSTRATIONS
    # =================================================

    elif choice == "6":

        print("\n--- Rollback Test: Venue and Edition ---")

        rollback_venue_edition()


    elif choice == "7":

        print("\n--- Rollback Test: Research Paper Submission ---")

        rollback_submission()


    elif choice == "8":

        print("\n--- Rollback Test: Reviewer Assignment ---")

        rollback_reviewer_assignment()


    elif choice == "9":

        print("\n--- Rollback Test: Review Submission ---")

        rollback_review()


    elif choice == "10":

        print("\n--- Rollback Test: Editorial Decision ---")

        rollback_editorial_decision()


    # =================================================
    # EXIT
    # =================================================

    elif choice == "0":

        print("\nExiting Academic Review Management System.")
        break


    # =================================================
    # INVALID INPUT
    # =================================================

    else:

        print("\nInvalid choice. Please enter a valid option.")
