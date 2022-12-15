from connections.orm_base import metadata
from menu_display import menu
from connections.populate_database import populate
from connections.db_connection import Session
from menu_implementation import *

if __name__ == "__main__":

    # Begin a session
    with Session() as session:
        session.begin()

        # Menu display
        while True:
            choice = menu()

            if choice == 0:
                populate(session)
            elif choice == 1:
                create_key(session)
            elif choice == 2:
                request_access(session)
            elif choice == 3:
                unauthorized_issue_key(session)
            elif choice == 4:
                losing_key(session)
            elif choice == 5:
                accessible_rooms(session)
            elif choice == 6:
                delete_key(session)
            elif choice == 7:
                delete_employee(session)
            elif choice == 8:
                add_door(session)
            elif choice == 9:
                update_request(session)
            elif choice == 10:
                report_employees(session)
