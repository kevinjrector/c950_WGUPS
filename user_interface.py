
import report

# user_interface.py

def get_report_time():
    """Function to ask the user for the time to generate the report."""
    user_input = input("Enter the time for the report (e.g., '10:30 AM'): ")
    return user_input

def userInterface(trucks, package_hashTable):
    while True:
        print("WGUPS Delivery System")
        print("1. Generate a Complete Delivery Report")
        print("2. View a Package's Status")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            set_time = get_report_time()
            report.generate_report(set_time, trucks, package_hashTable)
            print("Report generated successfully!")

            print("Return to the main menu? (y/n)")
            return_menu = input()
            if return_menu.lower() != 'y':
                break

        elif choice == '2':
            set_time = get_report_time()
            package_id = int(input("Enter the package ID: "))
            report.generate_packageStatus(set_time, trucks, package_hashTable, package_id)
            
            print("Return to the main menu? (y/n)")
            return_menu = input()
            if return_menu.lower() != 'y':
                break 
        elif choice == '3':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")







