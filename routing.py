from datetime import datetime, timedelta, time
from data_handler import load_address_data, load_distance_data, distanceBetween, extract_address
import heapq

# Load address and distance data
ADDRESS_FILE = "./data/address_file.csv"
DISTANCE_FILE = "./data/distance_file.csv"
address_dict = load_address_data(ADDRESS_FILE)
distance_matrix = load_distance_data(DISTANCE_FILE)

def sortPackages_forLoading(package_list):
    """ Sorts packages by distance first, then by deadline to optimize delivery order. """

    hub_index = extract_address("4001 South 700 East", address_dict)

    # 1️⃣ Calculate Distance of Each Package from Its Next Closest Stop
    package_distances = []
    for package in package_list:
        package_index = extract_address(package.get_address(), address_dict)
        if package_index is not None:
            # Get distance from hub initially
            distance = distanceBetween(hub_index, package_index, distance_matrix)
            package_distances.append((distance, package))

    # 2️⃣ Sort Packages by Distance First
    package_distances.sort(key=lambda x: x[0])  # Sort by distance value

    # 3️⃣ Sort by Deadline AFTER Sorting by Distance
    sorted_packages = sorted(package_distances, key=lambda x: x[1].get_deadline())

    # ✅ Extract only the package objects from the sorted list
    return [package[1] for package in sorted_packages]






def sortPackages_forDelivery(truck, package_list):
    """
    Implements a nearest-neighbor greedy approach.
    - Truck always goes to the **next closest stop**.
    - Grouped packages are delivered together.
    - Deadline is only considered if distances are equal.
    """

    sorted_packages = []
    current_location = truck.currentLocation
    remaining_packages = package_list[:]  # Copy list so we can modify it

    while remaining_packages:
        nearest_package = None
        nearest_distance = float('inf')

        # Step 1: Find the nearest package
        for package in remaining_packages:
            package_index = extract_address(package.get_address(), address_dict)
            current_index = extract_address(current_location, address_dict)

            if package_index is None or current_index is None:
                continue  # Skip invalid addresses

            distance = distanceBetween(current_index, package_index, distance_matrix)

            # Select package with **shortest distance**
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package

            # If two packages have the same distance, use **earliest deadline**
            elif distance == nearest_distance:
                if package.get_deadline() < nearest_package.get_deadline():
                    nearest_package = package

        # Step 2: Deliver all grouped packages at the same location
        if nearest_package:
            same_location_packages = [
                pkg for pkg in remaining_packages if pkg.get_address() == nearest_package.get_address()
            ]

            sorted_packages.extend(same_location_packages)
            current_location = nearest_package.get_address()  # Move truck

            # Remove delivered packages
            for pkg in same_location_packages:
                remaining_packages.remove(pkg)

    return sorted_packages







def load_truck(truck, packages, package_table, assigned_packages):
    for package in packages:
        # Check if the package is already assigned
        if package.packageID in assigned_packages:
            continue  # Skip already assigned packages

        # Load package and track it
        if truck.load_package(package, package_table):  # Ensure correct method is called
            assigned_packages.add(package.packageID)  # Track package as assigned
            package.assignedTruck = truck.truckID  # Assign truck to package
            package.status = "En Route"

        # Stop loading when truck reaches its capacity
        if len(truck.packageInventory) == truck.capacity:
            break



def deliver_packages(truck, package_table):
    print(f"\n🚛 Truck {truck.truckID} STARTING route at {truck.current_time.strftime('%I:%M %p')} from {truck.currentLocation}.")

    packages_delivered = 0

    # Sort packages dynamically before delivering
    truck.packageInventory = sortPackages_forDelivery(truck, truck.packageInventory)

    while truck.packageInventory:
        # Get the next package's address
        address = truck.packageInventory[0].get_address()
        package_index = extract_address(address, address_dict)
        start_index = extract_address(truck.currentLocation, address_dict)
        distance = float(distanceBetween(start_index, package_index, distance_matrix))

        # Drive to the new address
        truck.current_time = truck.drive_to(address, distance)

        # 🚚 Deliver all packages at this address
        delivered_packages = []
        while truck.packageInventory and truck.packageInventory[0].get_address() == address:
            package = truck.packageInventory.pop(0)

            # ✅ Update package info
            package.deliveryTime = truck.current_time.strftime('%I:%M %p')
            package.status = "Delivered"
            package_table.insert(package.packageID, package)

            # ✅ Check if package was late
            package_deadline = package.get_deadline()
            deadline_datetime = datetime.combine(datetime.today(), package_deadline)
            delivery_datetime = datetime.strptime(package.deliveryTime, '%I:%M %p')
            package.was_late = delivery_datetime > deadline_datetime
            status_tag = "LATE 🚨" if package.was_late else "ON TIME ✅"

            delivered_packages.append(f"[{package.packageID}] (Deadline: {package.deadline} - {status_tag})")

        print(f"🚚 DELIVERED Packages at {address.ljust(30)} {truck.current_time.strftime('%I:%M %p')} → {' | '.join(delivered_packages)}")

        # Update truck location
        truck.currentLocation = address
        packages_delivered += len(delivered_packages)

    # 🏁 Return to hub
    truck.return_to_hub()
    print(f"\n🚛 Truck {truck.truckID} RETURNED to hub at {truck.returnTime.strftime('%I:%M %p')}.")
    print(f"📦 {packages_delivered} PACKAGES delivered by Truck {truck.truckID}.")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")







def plan_deliveries(trucks, package_table):
    """
    Main function to assign packages to trucks and schedule deliveries.
    """
    dailyTotal_packages = 0

    # ✅ Global Set to Track Assigned Packages
    assigned_packages = set()

    # ✅ Track Delayed Packages (like Package #9)
    delayed_packages = []

    # STEP 1: Get all packages and sort them
    all_packages = [package_table.search(i) for i in range(1, 41) if package_table.search(i)]
    all_packages = sortPackages_forLoading(all_packages)

    # STEP 2: Remove Package #9 & Store in `delayed_packages`
    for package in all_packages[:]:  # Iterate over a copy to avoid modifying the list while iterating
        if package.packageID == 9:
            delayed_packages.append(package)
            all_packages.remove(package)

    # STEP 3: Grouped Packages (Must Be Together)
    group_A_packages = [package_table.search(i) for i in [20, 13, 15, 19, 14, 16]]
    delayed_packages_truck2 = [package_table.search(i) for i in [6, 25, 28, 32]]

    #Sort the packages in group A
    group_A_packages = sortPackages_forLoading(group_A_packages)

    truck_1 = trucks[0]  # Truck 1 leaves at 8:00 AM

    # Load Group A packages first
    load_truck(truck_1, group_A_packages, package_table, assigned_packages)


    assigned_packages.update(pkg.packageID for pkg in group_A_packages)  # ✅ Track assigned packages

    # Remove assigned packages before filling Truck 1
    remaining_packages = [pkg for pkg in all_packages if pkg.packageID not in assigned_packages and pkg.packageID not in {p.packageID for p in delayed_packages_truck2}]
    
    load_truck(truck_1, remaining_packages, package_table, assigned_packages)

        #Show truck 1 final inventory before starting the route
    print('Truck 1 Inventory (FINAL)')
    for pkg in truck_1.packageInventory:
        print(f'Package {pkg.packageID} - Address: {pkg.address} - Deadline: {pkg.get_deadline()} - Distance: {distanceBetween(extract_address("4001 South 700 East", address_dict), extract_address(pkg.get_address(), address_dict), distance_matrix)}')

    # STEP 4: Truck 2 (Delayed Departure at 9:05 AM)
    truck_2 = trucks[1]
    truck_2.current_time = datetime.combine(datetime.today(), time(9, 5))  # Delay truck 2's departure
    
    
    delayed_packages_truck2 = sortPackages_forLoading(delayed_packages_truck2)

    load_truck(truck_2, delayed_packages_truck2, package_table, assigned_packages)

    remaining_packages = [pkg for pkg in remaining_packages if pkg.packageID not in assigned_packages]
    load_truck(truck_2, remaining_packages, package_table, assigned_packages)

            #Show truck 1 final inventory before starting the route
    print('Truck 2 Inventory (FINAL)')
    for pkg in truck_2.packageInventory:
        print(f'Package {pkg.packageID} - Address: {pkg.address} - Deadline: {pkg.get_deadline()} - Distance: {distanceBetween(extract_address("4001 South 700 East", address_dict), extract_address(pkg.get_address(), address_dict), distance_matrix)}')

    # STEP 5: Truck 3 (Waits for Driver After First Truck Returns)
    truck_3 = trucks[2]

    #print("\n🚛 Truck 3 is waiting at the hub until a driver is available...")

    # STEP 6: Deliver Packages in Order
    deliver_packages(truck_1, package_table)
    deliver_packages(truck_2, package_table)

    # Find the earliest available driver return time
    earliest_driver_available = min(truck_1.returnTime, truck_2.returnTime)

    # Convert 12:00 PM into a datetime object with the same date as earliest_driver_available
    noon_time = datetime.combine(earliest_driver_available.date(), datetime.strptime("12:00 PM", "%I:%M %p").time())

    # Ensure Truck 3 departs at 12:00 PM **at the earliest**
    truck_3.departTime = max(earliest_driver_available, noon_time)

    truck_3.current_time = truck_3.departTime

    for package in delayed_packages:
        if package.packageID == 9:
            package.oldAddress = package.address # Store original address

            #print("\n🚨 AT 10:20 AM: Corrected address for Package 9 received!")
            package.address = "410 S State St"  # ✅ Update address
            package.updateTime = datetime.strptime("10:20 AM", "%I:%M %p") 


    # ✅ Reintegrate Delayed Packages Into The System
    load_truck(truck_3, delayed_packages, package_table, assigned_packages)

    remaining_packages = [pkg for pkg in all_packages if pkg.packageID not in assigned_packages]

    load_truck(truck_3, remaining_packages, package_table, assigned_packages)

    deliver_packages(truck_3, package_table)


    print("\n🎉 ALL PACKAGES DELIVERED! DAY COMPLETE.")





