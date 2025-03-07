from datetime import datetime, time
from data_handler import load_package_data
from routing import plan_deliveries
from truck import Truck

def generate_report(set_time, trucks, package_table):
    """
    Generates a report showing the status of trucks and packages at a specific time.
    set_time: datetime object indicating the time at which the report is generated
    trucks: List of Truck objects
    package_table: HashTable containing all packages
    """
    print(f"\n📅 Report at {set_time.strftime('%I:%M %p')}")
    
    # Iterate over each truck to display its progress
    for truck in trucks:
        print(f"\n🚛 Truck {truck.truckID} status:")
        
        # Show truck departure time
        print(f"  - Departed from hub at: {truck.departTime.strftime('%I:%M %p')}")
        
        # Show truck's location at set_time
        print(f"  - Current location: {truck.currentLocation}")
        
        # Show packages delivered by this truck by set_time
        delivered_packages = []
        remaining_packages = []
        
        for package in truck.packageInventory:
            # Check if the package was delivered by the set_time
            if package.deliveryTime <= set_time.strftime('%I:%M %p'):
                delivered_packages.append(package)
            else:
                remaining_packages.append(package)
        
        # Print the delivered packages
        if delivered_packages:
            print(f"  - Packages delivered:")
            for p in delivered_packages:
                print(f"    - Package {p.packageID}: Delivered at {p.deliveryTime}")
        
        # Print the remaining packages
        if remaining_packages:
            print(f"  - Packages remaining to be delivered:")
            for p in remaining_packages:
                print(f"    - Package {p.packageID}: {p.address}")
        
        print(f"  - Total Packages Delivered: {len(delivered_packages)}")
        print(f"  - Total Packages Remaining: {len(remaining_packages)}")


# 🚛 **Step 1: Initialize Data and Constants**
TRUCK_SPEED = 18  # MPH
TRUCK_CAPACITY = 16
TOTAL_TRUCKS = 3
TOTAL_DRIVERS = 2
HUB_LOCATION = "4001 South 700 East"

PACKAGE_FILE = './data/package_file.csv'

# 🚀 **Load Package Data into Hash Table**
package_hashTable = load_package_data(PACKAGE_FILE)

# 🚛 **Step 2: Create Truck Objects (Fixed)**
departure_times = [
    datetime.combine(datetime.today(), time(8, 0)),   # Truck 1 departs at 8:00 AM
    datetime.combine(datetime.today(), time(9, 5)),   # Truck 2 departs at 9:05 AM
    None  # Truck 3 waits for an available driver
]

trucks = [
    Truck(
        truckID=i+1,
        speed=TRUCK_SPEED,
        currentLocation=HUB_LOCATION,  # ✅ Ensure all trucks start at HUB
        departTime=departure_times[i] if departure_times[i] else datetime.max,  # ✅ Avoid `None` issue
        capacity=TRUCK_CAPACITY
    ) for i in range(TOTAL_TRUCKS)
]

# 🚛 **Step 3: Run the Delivery Plan**
plan_deliveries(trucks, package_hashTable)

# Set the time for the report
set_time = datetime.strptime('10:30 AM', '%I:%M %p')

# Generate the report at set_time
generate_report(set_time, trucks, package_hashTable)