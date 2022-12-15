
def menu():
    while True:
        choice = input("\nMENU\n"
                       "0. Populate the database\n"
                       "1. Create a Key\n"
                       "2. Request access to a given room by a given employee\n"
                       "3. Capture the issue of a key to an employee\n"
                       "4. Capture losing a key\n"
                       "5. Report out all the rooms that an employee can enter, given the keys that he/she already "
                       "has\n"
                       "6. Delete a key\n"
                       "7. Delete an employee\n"
                       "8. Add a new door that can be opened by an existing hook\n"
                       "9. Update an access request to move it to a new employee\n"
                       "10. Report out all the employees who can get into a room\n"
                       "Your choice: ")

        # Check if choice is a number
        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a number.")

        # Check if choice is in range
        if choice in range(11):
            return choice
        else:
            print("Invalid input.\n")