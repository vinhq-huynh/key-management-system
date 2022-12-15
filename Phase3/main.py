from menu_helper import *
from functions import *
from menu_display import menu
from populate import populate

if __name__ == '__main__':
    # Menu display

    # Drop all collections if needed
    # for c in project_database.list_collection_names():
    #     project_database.drop_collection(c)

    while True:
        choice = menu()

        if choice == 0:
            populate()
        elif choice == 1:
            create_key()
        elif choice == 2:
            request_access()
        elif choice == 3:
            unauthorized_issue_key()
        elif choice == 4:
            losing_key()
        elif choice == 5:
            accessible_rooms()
        elif choice == 6:
            delete_key()
        elif choice == 7:
            delete_employee()
        elif choice == 8:
            add_door()
        elif choice == 9:
            update_request()
        elif choice == 10:
            report_employees()
