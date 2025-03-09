from datetime import datetime

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
            print(f"  - Truck {truck.truckID} has returned to the hub.")
        else:
            print(f"  - Truck {truck.truckID} is currently en route.")


        # Packages that are delivered or still in progress
        delivered_packages = []
        remaining_packages = []

        # Check the status of each package
        for package_id in range(1, 41):
            package = package_table.search(package_id)

            if package.assignedTruck == truck.truckID:
                # Package is delivered and delivered time is before or at the report time
                if package.status == 'Delivered' and datetime.strptime(package.deliveryTime, '%I:%M %p') <= set_time:
                    delivered_packages.append(package)
                else:
                    # Package hasn't been delivered, check if it's in transit or at the hub
                    if truck.departTime <= set_time < truck.returnTime:
                        remaining_packages.append(f"Package {package.packageID}: {package.address} (En Route)")
                    elif truck.departTime > set_time:
                        remaining_packages.append(f"Package {package.packageID}: {package.address} (At Hub)")

        # Print the delivered packages
        if delivered_packages:
            print(f"  - Packages delivered by Truck {truck.truckID}:")
            for p in delivered_packages:
                print(f"    - Package {p.packageID}: {p.get_address()} at {p.deliveryTime}")
        
        # Print the remaining packages
        if remaining_packages:
            print(f"  - Packages remaining to be delivered:")
            for p in remaining_packages:
                print(f"    - {p}")

        print(f"  - Total Packages Delivered: {len(delivered_packages)}")
        print(f"  - Total Packages Remaining: {len(remaining_packages)}")
