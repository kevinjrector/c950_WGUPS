"""
This module contains the main routing logic for the package delivery system.
It includes functions to sort packages for loading and delivery, load trucks, and deliver packages.

I used a greedy approach to optimize the delivery order based on distance and deadlines.
"""
from datetime import datetime, timedelta, time
from data_handler import load_address_data, load_distance_data, distanceBetween, extract_address
import heapq

# Load address and distance data
ADDRESS_FILE = "./data/address_file.csv"
DISTANCE_FILE = "./data/distance_file.csv"
address_dict = load_address_data(ADDRESS_FILE)
distance_matrix = load_distance_data(DISTANCE_FILE)

def sortPackages_forLoading(package_list):
    """ 
    Sorts packages for loading based on distance from the hub and deadlines.
    This method uses a greedy approach to optimize the loading order.

    package_list: List of Package objects to be sorted

    Returns the sorted list of packages for loading.
    """

    # Sets the hub location
    hub_index = extract_address("4001 South 700 East", address_dict)

    #Calculates the distance from the hub to each package
    package_distances = []
    for package in package_list:
        package_index = extract_address(package.get_address(), address_dict)
        if package_index is not None:
            # Get distance from hub initially
            distance = distanceBetween(hub_index, package_index, distance_matrix)
            package_distances.append((distance, package))

    # Sort the packages by distance from the hub
    package_distances.sort(key=lambda x: x[0])

    # Sorts by deadline if distances are equal
    sorted_packages = sorted(package_distances, key=lambda x: x[1].get_deadline())

    # Returns the sorted packages
    return [package[1] for package in sorted_packages]






def sortPackages_forDelivery(truck, package_list):
    """
    Sorts packages for delivery based on distance and deadlines.
    This method uses a greedy approach to optimize the delivery order.

    truck: Truck object that will deliver the packages
    package_list: List of Package objects to be sorted

    Returns the sorted list of packages for delivery.
    """

    sorted_packages = []
    current_location = truck.currentLocation
    remaining_packages = package_list[:] 

    while remaining_packages:
        nearest_package = None
        nearest_distance = float('inf')

        # Find the nearest package from the current location of the truck
        for package in remaining_packages:
            package_index = extract_address(package.get_address(), address_dict)
            current_index = extract_address(current_location, address_dict)

            if package_index is None or current_index is None:
                continue  

            distance = distanceBetween(current_index, package_index, distance_matrix)

            # If a package is closer, update the nearest package
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package

            # If two packages are equidistant, deliver the one with the earliest deadline
            elif distance == nearest_distance:
                if package.get_deadline() < nearest_package.get_deadline():
                    nearest_package = package

        # Add the nearest package to the sorted list
        if nearest_package:
            same_location_packages = [
                pkg for pkg in remaining_packages if pkg.get_address() == nearest_package.get_address()
            ]

            sorted_packages.extend(same_location_packages)
            current_location = nearest_package.get_address()  # Move truck

            # Remove all packages at the same location (this is for packages with the same destination address)
            for pkg in same_location_packages:
                remaining_packages.remove(pkg)
            
    # Return the sorted packages
    return sorted_packages


def load_truck(truck, packages, package_table, assigned_packages):
    """
    Loads packages onto a truck until it reaches capacity or runs out of packages.

    truck: Truck object to load packages onto
    packages: List of Package objects to load
    package_table: HashTable containing all packages
    assigned_packages: Set of package IDs that have already been assigned to a truck
    """

    # Load packages onto the truck
    for package in packages:

        # Skip packages that have already been assigned
        if package.packageID in assigned_packages:
            continue 

        # Load the package onto the truck and update its status
        if truck.load_package(package, package_table):  
            assigned_packages.add(package.packageID)  # Track package as assigned
            package.assignedTruck = truck.truckID  # Assign truck to package
            package.status = "En Route"

        # Stop loading when truck reaches its capacity
        if len(truck.packageInventory) == truck.capacity:
            break

def total_miles_traveled(truck):
    """
    Calculates the total miles traveled at the end of the day

    truck: Truck object to calculate total miles for

    returns the total miles traveled by the truck
    """
    stops_count = len(truck.truck.packageInventory) 

    return truck.milesTotal_list[stops_count - 1] if stops_count > 0 else 0



def deliver_packages(truck, package_table):
    """
    Delivers the packages on the truck's route.
    This method sorts the packages for delivery and updates their statuses.

    truck: Truck object to deliver packages
    package_table: HashTable containing all packages
    """
    print(f"\nAttention: Truck {truck.truckID} STARTING route at {truck.current_time.strftime('%I:%M %p')} from {truck.currentLocation}.")

    packages_delivered = 0

    # Calls the sortPackages_forDelivery method to sort the packages for delivery
    truck.packageInventory = sortPackages_forDelivery(truck, truck.packageInventory)

    # While there are packages on the truck, deliver them
    while truck.packageInventory:
        address = truck.packageInventory[0].get_address()
        package_index = extract_address(address, address_dict)
        start_index = extract_address(truck.currentLocation, address_dict)
        distance = float(distanceBetween(start_index, package_index, distance_matrix))

        # Drive to the new address
        truck.current_time = truck.drive_to(address, distance)

        # Delivers all packages for a given address
        delivered_packages = []
        while truck.packageInventory and truck.packageInventory[0].get_address() == address:
            package = truck.packageInventory.pop(0)

            # Update package status and delivery time
            package.deliveryTime = truck.current_time.strftime('%I:%M %p')
            package.status = "Delivered"
            package_table.insert(package.packageID, package)

            # Verify if the package was delivered on time
            package_deadline = package.get_deadline()
            deadline_datetime = datetime.combine(datetime.today(), package_deadline)
            delivery_datetime = datetime.strptime(package.deliveryTime, '%I:%M %p')
            package.was_late = delivery_datetime > deadline_datetime
            status_tag = "(!) LATE " if package.was_late else "ON TIME"

            delivered_packages.append(f"[{package.packageID}] (Deadline: {package.deadline} - {status_tag})")

        print(f"DELIVERED Packages at {address.ljust(30)} {truck.current_time.strftime('%I:%M %p')} → {' | '.join(delivered_packages)}")

        # Update truck location and packages delivered
        truck.currentLocation = address
        packages_delivered += len(delivered_packages)

    # Return to hub
    hub_index = extract_address("4001 South 700 East", address_dict)
    start_index = extract_address(truck.currentLocation, address_dict)
    distance = float(distanceBetween(start_index, hub_index, distance_matrix))

    truck.current_time = truck.drive_to(hub_index, distance)
    truck.return_to_hub()


    print(f"\nTruck {truck.truckID} RETURNED to hub at {truck.returnTime.strftime('%I:%M %p')}.")
    print(f"{packages_delivered} PACKAGES delivered by Truck {truck.truckID}.")
    print("============================ END OF ROUTE ============================\n")







def plan_deliveries(trucks, package_table):
    """
    Plans the delivery routes for the trucks based on the package data.
    This method loads the trucks with packages and calls the deliver_packages method to deliver them.
    Handles special cases like delayed packages and grouped packages.

    trucks: List of Truck objects to plan deliveries for
    package_table: HashTable containing
    """

    # Global Set to Track Assigned Packages
    assigned_packages = set()

    # List to track Delayed Packages (like Package #9)
    delayed_packages = []

    # Initialize the package list and sort for loading
    all_packages = [package_table.search(i) for i in range(1, 41) if package_table.search(i)]
    all_packages = sortPackages_forLoading(all_packages)

    # Remove packages that are delayed or have errors
    for package in all_packages[:]:
        if package.packageID == 9:
            delayed_packages.append(package)
            all_packages.remove(package)

    # Initalize grouped packages and delayed packages for Truck 1 and Truck 2
    group_A_packages = [package_table.search(i) for i in [20, 13, 15, 19, 14, 16]]
    delayed_packages_truck2 = [package_table.search(i) for i in [6, 25, 28, 32]]

    # Update Arrival Time for Delayed Packages
    for package in range(1, 41):
        package = package_table.search(package)
        if package in delayed_packages_truck2:
            package.hubArrivalTime = datetime.combine(datetime.today(), time(9, 5))

    # Sort the grouped packages for loading
    group_A_packages = sortPackages_forLoading(group_A_packages)

    # Assign the first truck object
    truck_1 = trucks[0]

    # Load Group A packages first
    load_truck(truck_1, group_A_packages, package_table, assigned_packages)

    assigned_packages.update(pkg.packageID for pkg in group_A_packages)  

    # Remove assigned packages before filling Truck 1
    remaining_packages = [pkg for pkg in all_packages if pkg.packageID not in assigned_packages and pkg.packageID not in {p.packageID for p in delayed_packages_truck2}]

    # Load remaining packages onto Truck 1
    load_truck(truck_1, remaining_packages, package_table, assigned_packages)

    # Assign the second truck object and set the current time to 9:05 AM (this will be used as truck 2's departure time)
    truck_2 = trucks[1]
    truck_2.current_time = datetime.combine(datetime.today(), time(9, 5))  

    # Sort the packages that were delayed for Truck 2 and load them first
    delayed_packages_truck2 = sortPackages_forLoading(delayed_packages_truck2)
    load_truck(truck_2, delayed_packages_truck2, package_table, assigned_packages)

    # Remove assigned packages before filling Truck 2 with remaining packages
    remaining_packages = [pkg for pkg in remaining_packages if pkg.packageID not in assigned_packages]
    load_truck(truck_2, remaining_packages, package_table, assigned_packages)

    # Assign the third truck object
    truck_3 = trucks[2]

    # Deliver packages for Truck 1 and Truck 2
    deliver_packages(truck_1, package_table)
    deliver_packages(truck_2, package_table)

    # Find the earliest available driver return time by comparing Truck 1 and Truck 2's return times
    earliest_driver_available = min(truck_1.returnTime, truck_2.returnTime)

    # Convert 12:00 PM into a datetime object with the same date as earliest_driver_available
    noon_time = datetime.combine(earliest_driver_available.date(), datetime.strptime("12:00 PM", "%I:%M %p").time())

    # Ensure Truck 3 departs no earlier than the earliest driver return time or 12:00 PM (Truck 3 will never depart before noon)
    truck_3.departTime = max(earliest_driver_available, noon_time)
    truck_3.current_time = truck_3.departTime

    # Package 9 was initially assigned an incorrect address and must be corrected at 10:20 AM.
    # This update ensures the correct address is used when it's scheduled for delivery.
    for package in delayed_packages:
        if package.packageID == 9:
            package.oldAddress = package.address # Store original address

            package.address = "410 S State St" 
            package.updateTime = datetime.strptime("10:20 AM", "%I:%M %p") 


    # Load Truck 3 with delayed packages first
    load_truck(truck_3, delayed_packages, package_table, assigned_packages)

    # Load remaining packages onto Truck 3
    remaining_packages = [pkg for pkg in all_packages if pkg.packageID not in assigned_packages]
    load_truck(truck_3, remaining_packages, package_table, assigned_packages)

    # Deliver packages for Truck 3
    deliver_packages(truck_3, package_table)

    sum_miles = 0
    # Total miles traveled for all trucks
    for truck in trucks:
        sum_miles += truck.milesTotal if truck.milesTotal > 0 else 0
    print(f"TOTAL MILES TRAVELED FOR ALL TRUCKS = {sum_miles:.2f} miles")

    print("\nALL PACKAGES DELIVERED.\n\n\n\n\n\n\n")





