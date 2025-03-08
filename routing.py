from datetime import datetime, timedelta, time
from data_handler import distanceBetween, extract_address

def sort_packages_by_deadline_and_distance(package_list):
    """ Sorts packages by deadline first, then by distance from the hub. """
    hub_index = extract_address("4001 South 700 East")
    
    return sorted(package_list, key=lambda package: (
        package.get_deadline(),  # Sort by deadline
        float(distanceBetween(hub_index, extract_address(package.get_address())))  # Then by distance
    ))

def load_truck(truck, packages, package_table, assigned_packages):
    for package in packages:
        # Check if the package is already assigned
        if package.packageID in assigned_packages:
            continue  # Skip already assigned packages

        # Load package and track it
        if truck.load_package(package, package_table):
            assigned_packages.add(package.packageID)  # Track package as assigned
            package.assignedTruck = truck.truckID  # Assign truck to package
            package.status = "En Route"

        # Stop loading when truck reaches its capacity
        if len(truck.packageInventory) == truck.capacity:
            #print(f"Truck {truck.truckID} is full. Stopping load.")  # Debug line
            break





def deliver_packages(truck, package_table):
    """
    Delivers all packages on the truck in order, updating the truck's time.
    """
    print(f"\n🚛 Truck {truck.truckID} STARTING route at {truck.current_time.strftime('%I:%M %p')} from {truck.currentLocation}.")
    packages_delivered = 0

    while truck.packageInventory:
        package = truck.packageInventory.pop(0)
        address_index = extract_address(package.get_address())
        distance = float(distanceBetween(extract_address(truck.currentLocation), address_index))
        
        # Move truck and update time
        truck.current_time = truck.drive_to(package.get_address(), distance)
        package.deliveryTime = truck.current_time.strftime('%I:%M %p')  # Set delivery time for report
        package.status = "Delivered"
        package_table.insert(package.packageID, package)  # Update package status
        
        packages_delivered += 1
        
        print(f"   - DELIVERED Package {package.packageID} at {package.get_address()} at {package.deliveryTime}.")
    
    truck.return_to_hub()  # Mark truck as back at hub
    print(f"🚛 Truck {truck.truckID} RETURNED to hub at {truck.returnTime.strftime('%I:%M %p')}.")
    print(f"📦 {packages_delivered} PACKAGES delivered by Truck {truck.truckID}.")



def plan_deliveries(trucks, package_table):
    """
    Main function to assign packages to trucks and schedule deliveries.
    """
    # ✅ Global Set to Track Assigned Packages
    assigned_packages = set()

    # ✅ Track Delayed Packages (like Package #9)
    delayed_packages = []

    # STEP 1: Get all packages and sort them
    all_packages = [package_table.search(i) for i in range(1, 41) if package_table.search(i)]
    all_packages = sort_packages_by_deadline_and_distance(all_packages)

    # STEP 2: Remove Package #9 & Store in `delayed_packages`
    for package in all_packages[:]:  # Iterate over a copy to avoid modifying the list while iterating
        if package.packageID == 9:
            delayed_packages.append(package)
            all_packages.remove(package)  # ✅ Remove from normal processing

    # STEP 3: Grouped Packages (Must Be Together)
    group_A_packages = [package_table.search(i) for i in [20, 13, 15, 19, 14, 16]]

    truck_1 = trucks[0]  # Truck 1 leaves at 8:00 AM

    load_truck(truck_1, sort_packages_by_deadline_and_distance(group_A_packages), package_table, assigned_packages)

    assigned_packages.update(pkg.packageID for pkg in group_A_packages)  # ✅ Track assigned packages

    # Remove assigned packages before filling Truck 1
    remaining_packages = [pkg for pkg in all_packages if pkg.packageID not in assigned_packages]

    load_truck(truck_1, remaining_packages, package_table, assigned_packages)

    # STEP 4: Truck 2 (Delayed Departure at 9:05 AM)
    truck_2 = trucks[1]
    truck_2.current_time = datetime.combine(datetime.today(), time(9, 5))  # Delay truck 2's departure
    
    delayed_packages_truck2 = [package_table.search(i) for i in [6, 25, 28, 32]]
    delayed_packages_truck2 = sort_packages_by_deadline_and_distance(delayed_packages_truck2)

    load_truck(truck_2, delayed_packages_truck2, package_table, assigned_packages)

    remaining_packages = [pkg for pkg in remaining_packages if pkg.packageID not in assigned_packages]
    load_truck(truck_2, remaining_packages, package_table, assigned_packages)

    # STEP 5: Truck 3 (Waits for Driver After First Truck Returns)
    truck_3 = trucks[2]

    #print("\n🚛 Truck 3 is waiting at the hub until a driver is available...")

    # STEP 6: Deliver Packages in Order
    deliver_packages(truck_1, package_table)
    deliver_packages(truck_2, package_table)

    # ✅ Dynamically Assign Delayed Packages (like Package #9)
    truck_3.current_time = max(truck_1.returnTime, truck_2.returnTime)

    for package in delayed_packages:
        if package.packageID == 9:
            #print("\n🚨 AT 10:20 AM: Corrected address for Package 9 received!")
            package.address = "410 S State St, Salt Lake City, UT 84111"  # ✅ Update address

    # ✅ Reintegrate Delayed Packages Into The System
    load_truck(truck_3, delayed_packages, package_table, assigned_packages)

    remaining_packages = [pkg for pkg in all_packages if pkg.packageID not in assigned_packages]

    load_truck(truck_3, remaining_packages, package_table, assigned_packages)

    deliver_packages(truck_3, package_table)


    print("\n🎉 ALL PACKAGES DELIVERED! DAY COMPLETE.")



