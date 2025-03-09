from datetime import datetime

def miles_traveled(set_time, truck, delivered_count):
    """
    Calculate the total miles traveled by a truck at a specific time.
    set_time: datetime object (already converted before passing)
    truck: Truck object
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

    # Use the delivery count as an index (avoid out-of-range errors)
    return truck.milesTotal_list[min(delivered_count - 1, len(truck.milesTotal_list) - 1)]





def generate_report(set_time, trucks, package_table):
    """
    Generates a report showing the status of trucks and packages at a specific time.
    set_time: datetime object indicating the time at which the report is generated
    trucks: List of Truck objects
    package_table: HashTable containing all packages
    """

    set_time = datetime.strptime(set_time, '%I:%M %p')  # Convert user input to datetime
    
    print(f"\n📅 Report at {set_time.strftime('%I:%M %p')}")

    # Iterate over each truck to display its progress
    for truck in trucks:
        print(f"\n🚛 Truck {truck.truckID} status at {set_time.strftime('%I:%M %p')}:")

        # Check if the truck has completed deliveries or still in transit or returned to the hub
        if truck.departTime.time() > set_time.time():
            print(f"  - Truck {truck.truckID} has not left the hub yet.")
        elif truck.returnTime.time() <= set_time.time():
            print(f"  - Truck {truck.truckID} returned to the hub at {truck.returnTime.strftime('%I:%M %p')}.")
        else:
            print(f"  - Truck {truck.truckID} is currently en route.")

        # Check the status of each package **(UPDATING STATUS INSTEAD OF TRACKING IN LISTS)**
        for package_id in range(1, 41):
            package = package_table.search(package_id)

            if package.assignedTruck == truck.truckID:
                # ✅ Directly update the status
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

        # 🚚 **Print packages grouped by status**
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

        # 🚛 **Print Totals**
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
    package_table: HashTable containing all packages
    package_id: The package ID to look up
    """

    set_time = datetime.strptime(set_time, '%I:%M %p')  # Convert user input to datetime
    print(f"\n📅 Package Status Report at {set_time.strftime('%I:%M %p')}")

    package = package_table.search(package_id)

    for t in trucks:
        if package.assignedTruck == t.truckID:
            truck = t
            break
        else:
            truck = None


# ✅ Directly update the status
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

    print("\n")

    if package.status == "Erroneous":
        print(f"📦 Package {package_id} Status: {package.status} (Will be updated at {package.updateTime.strftime('%I:%M %p')})")
    else:
        print(f"📦 Package {package_id} Status: {package.status}")




