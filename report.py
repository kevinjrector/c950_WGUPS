"""
This module contains functions to generate reports for the delivery routing program.

The `miles_traveled` function calculates the total miles traveled by a truck at a specific time.
The `generate_report` function generates a report showing the status of trucks and packages at a specific time.
The `generate_packageStatus` function generates a report showing the status of a single package at a specific time.
"""
from datetime import datetime

def miles_traveled(set_time, truck, delivered_count):
    """
    Calculates the total miles traveled by a truck at a specific time.

    set_time: datetime object indicating the time at which the miles are calculated
    truck: Truck object for which miles are calculated
    delivered_count: Number of packages delivered by the truck up to `set_time`

    Returns the total miles traveled by the truck at `set_time`.
    """
    # If the truck hasn't left yet, return 0 miles
    if truck.departTime.time() > set_time.time():
        return 0

    # If the truck has returned before set_time, return full miles traveled
    if truck.returnTime and truck.returnTime.time() <= set_time.time():
        return truck.milesTotal

    # Find the number of packages delivered up to `set_time`
    delivered_count = delivered_count

    # If no packages were delivered yet, return 0 miles
    if delivered_count == 0:
        return 0

    # Use the delivery count as an index to get the miles traveled from the list
    return truck.milesTotal_list[min(delivered_count - 1, len(truck.milesTotal_list) - 1)]





def generate_report(set_time, trucks, package_table):
    """
    Generates a report showing the status of trucks and packages at a specific time.

    set_time: datetime object indicating the time at which the report is generated
    trucks: List of Truck objects
    package_table: HashTable containing all packages

    Returns the generated report.
    """

    set_time = datetime.strptime(set_time, '%I:%M %p')
    
    print(f"\n📅 Report at {set_time.strftime('%I:%M %p')}")

    for truck in trucks:
        print(f"\n🚛 Truck {truck.truckID} status at {set_time.strftime('%I:%M %p')}:")

        # Check if the truck has completed deliveries or still in transit or returned to the hub
        if truck.departTime.time() > set_time.time():
            print(f"  - Truck {truck.truckID} has not left the hub yet.")
        elif truck.returnTime.time() <= set_time.time():
            print(f"  - Truck {truck.truckID} returned to the hub at {truck.returnTime.strftime('%I:%M %p')}.")
        else:
            print(f"  - Truck {truck.truckID} is currently en route.")

        # Update package statuses based on the current time and truck depart/return times
        for package_id in range(1, 41):
            package = package_table.search(package_id)

            if package.assignedTruck == truck.truckID: 
                if package.deliveryTime and datetime.strptime(package.deliveryTime, '%I:%M %p') <= set_time: # If the package has been delivered
                    package.status = "Delivered"
                elif package.updateTime and package.oldAddress: # If the package has an update time and old address
                    if package.updateTime.time() > set_time.time():
                        package.status = "Erroneous"
                    elif package.updateTime.time() <= set_time.time() and truck.departTime <= set_time < truck.returnTime.time(): # If the update time is less than or equal to the set time and the truck is en route
                        package.status = "En Route"
                    elif package.updateTime.time() <= set_time.time() and truck.departTime > set_time: # If the update time is less than or equal to the set time and the truck is at the hub
                        package.status = "At Hub"
                elif not package.updateTime:
                    if truck.departTime.time() <= set_time.time() < truck.returnTime.time(): # If the truck is en route
                        package.status = "En Route"
                    elif truck.departTime.time() > set_time.time(): # If the truck is at the hub
                        package.status = "At Hub"

        # Print package statuses for the truck
        print(f"\n  - [X] Packages Delivered:")
        for package_id in range(1, 41):
            package = package_table.search(package_id)
            if package.assignedTruck == truck.truckID and package.status == "Delivered":
                print(f"    - Package {package.packageID}: {package.get_address()} | Delivered at {package.deliveryTime}")

        print(f"\n  - (~) Packages Remaining:")
        for package_id in range(1, 41):
            package = package_table.search(package_id)
            if package.assignedTruck == truck.truckID and package.status == "En Route":
                print(f"    - Package {package.packageID}: {package.address} ({package.status})")
            elif package.assignedTruck == truck.truckID and package.status == "At Hub":
                print(f"    - Package {package.packageID}: {package.address} ({package.status})")

        print(f"\n  - (!) Erroneous Packages:")
        for package_id in range(1, 41):
            package = package_table.search(package_id)
            if package.assignedTruck == truck.truckID and package.status == "Erroneous":
                if package.updateTime.time() > set_time.time():
                    print(f"    - Package {package.packageID}: {package.oldAddress} (Will be updated at {package.updateTime.strftime('%I:%M %p')})")
                else:
                    print(f"    - Package {package.packageID}: {package.address} (Updated at {package.updateTime.strftime('%I:%M %p')})")

        # Calculate and print the total delivered, remaining, erroneous packages, and miles traveled
        delivered_count = sum(1 for package_id in range(1, 41) if package_table.search(package_id).assignedTruck == truck.truckID and package_table.search(package_id).status == "Delivered")
        remaining_count = sum(1 for package_id in range(1, 41) if package_table.search(package_id).assignedTruck == truck.truckID and package_table.search(package_id).status in ["En Route", "At Hub"])
        erroneous_count = sum(1 for package_id in range(1, 41) if package_table.search(package_id).assignedTruck == truck.truckID and package_table.search(package_id).status == "Erroneous")
        miles_at_time = miles_traveled(set_time, truck, delivered_count)


        print(f"\n  - Total Packages Delivered: {delivered_count}")
        print(f"  - Total Packages Remaining: {remaining_count}")
        print(f"  - Total Erroneous Packages: {erroneous_count}")
        print(f"  - Total Miles Traveled at {set_time.strftime('%I:%M %p')}: {miles_at_time:.2f} miles")



def generate_packageStatus(set_time, trucks, package_table, package_id):
    """
    Generates a report showing the status of a single package at a specific time.

    set_time: datetime object indicating the time at which the report is generated
    trucks: List of Truck objects
    package_table: HashTable containing all packages
    package_id: ID of the package to generate the report

    Returns the status of the package.
    """

    set_time = datetime.strptime(set_time, '%I:%M %p') 

    print(f"\n==Package Status Report== at {set_time.strftime('%I:%M %p')}")

    # Find the package in the package hash table
    if package_table.search(package_id) is None:
        print(f"Package {package_id} not found.")
        return None
    else:
        package = package_table.search(package_id)

    # Find the truck assigned to the package
    for t in trucks:
        if package.assignedTruck == t.truckID:
            truck = t
            break
        else:
            truck = None


    # Update package status based on the current time and truck depart/return times
    if package.deliveryTime and datetime.strptime(package.deliveryTime, '%I:%M %p') <= set_time:
        package.status = "Delivered"
    elif package.updateTime and package.oldAddress:
        if package.updateTime.time() > set_time.time():
            package.status = "Erroneous"
        elif package.updateTime.time() <= set_time.time() and truck.departTime <= set_time < truck.returnTime.time():
            package.status = "En Route"
        elif package.updateTime.time() <= set_time.time() and truck.departTime > set_time:
            package.status = "At Hub"
    elif not package.updateTime:
        if truck.departTime.time() <= set_time.time() < truck.returnTime.time():
            package.status = "En Route"
        elif truck.departTime.time() > set_time.time():
            package.status = "At Hub"


    # Print the package status
    if package.status == "Erroneous":
        print(f"Package {package_id} Status: {package.status} ([ALERT]: Will be updated at {package.updateTime.strftime('%I:%M %p')})\n")
    else:
        print(f"Package {package_id} Status: {package.status}\n")




