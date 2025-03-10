"""
This module contains the user interface.
The user interface allows the user to select options to generate reports or view package status.
"""

import report

def get_report_time():
    """
    Prompts the user to enter the time for the report and ensures it follows 'HH:MM AM/PM' format.
    """
    while True:
        user_input = input("Enter the time for the report (e.g., '10:30 AM'): ").strip()

        if user_input == '':
            return "8:00 AM"  # Default time if empty

        parts = user_input.split()
        if len(parts) == 2 and ":" in parts[0] and parts[1] in ["AM", "PM", "am", "pm"]:
            return user_input  # Valid input and return the time
        
        print("Invalid format. Please enter the time as 'HH:MM AM/PM'. Try again.")

def userInterface(trucks, package_hashTable):
    """
    Main user interface function that allows the user to generate reports or view package status.
    """
    while True:
        print("WGUPS Delivery System")
        print("1. Generate a Complete Delivery Report")
        print("2. View a Package's Status")
        print("3. Exit")
        choice = input("Enter your choice: ")

        # Generate a complete delivery report
        if choice == '1':
            set_time = get_report_time()
            report.generate_report(set_time, trucks, package_hashTable)
            print("Report generated successfully!")

            print("Return to the main menu? (y/n)")
            return_menu = input()
            if return_menu.lower() != 'y':
                break

        # View a package's status
        elif choice == '2':
            set_time = get_report_time()
            package_id = int(input("Enter the package ID: "))
            report.generate_packageStatus(set_time, trucks, package_hashTable, package_id)

            # Ask the user if they want to return to the main menu instead of exiting
            print("Return to the main menu? (y/n)")
            return_menu = input()
            if return_menu.lower() != 'y':
                break 

        # Exit the program
        elif choice == '3':
            print("Exiting the program...")
            break
        # Input validation
        else:
            print("Invalid choice. Please try again.")







