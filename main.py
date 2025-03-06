from truck import Truck
from driver import Driver
import datetime

from routing import sortPackages_byDeadline_or_byDistance, deliver_packages, package_table




# functions

def get_packageStatus(package_table, input_time):

    print("Package Status at", input_time, ":\n")

    for packageID in range(1, 41):
        package = package_table.search(packageID)
        if package:
            delivery_time = package.deliveryTime
            status = "At Hub"

            address = package.get_address()

            #Ensure `deliveryTime` is a `datetime` object before comparing
            if isinstance(delivery_time, str):
                delivery_time = datetime.datetime.strptime(delivery_time, "%I:%M %p")
            

            # If deliveryTime is None, it means the package hasn't been scheduled for delivery yet
            if delivery_time:
                if delivery_time <= input_time:
                    status = "Delivered"
                else:
                    status = "En Route"
            
            print(f'[x] Package {packageID}: {status} | {address} | Delivered at {delivery_time.strftime("%I:%M %p") if delivery_time else "N/A"}')



# Constants such as truck speed, truck capacity, and number of trucks and drivers available
truckSpeed = 18
truckCapcaity = 16
driversAvailable = 2
trucksAvailable = 3
truck_startTime = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))

# Create truck objects based on how many trucks available
truck_list = []
for i in range(trucksAvailable):
    truck_list.append(Truck(truckID=i+1, speed=truckSpeed, milesTotal=0, currentLocation="4001 South 700 East", departTime=truck_startTime, capacity=truckCapcaity, packageInventory=[]))

# Create driver objects based on how many drivers available
drivers_list = []
for i in range(driversAvailable):
    drivers_list.append(Driver(driverID=i+1))

occupied_trucks = []
# Output the driver's details
for driver in drivers_list:
    driver.assignTruck(truck_list.pop(0))
    occupied_trucks.append(driver.truck)



sorted_package_list = sortPackages_byDeadline_or_byDistance()

input_time = datetime.datetime.strptime("10:00 AM", "%I:%M %p")

#Show trucks that have drivers assigned and are available for work
for truck in occupied_trucks:
    print(truck)

print("\nLoading packages onto trucks...")

# Special case packages - these must go on specific trucks
priority_packages = {
    1: [13, 14, 15],  # Truck 1 MUST deliver packages 13, 14, 15
    2: [16, 17],       # Truck 2 MUST deliver packages 16, 17
}

# Step 1: Manually load priority packages onto assigned trucks
for truck in occupied_trucks:
    if truck.truckID in priority_packages:
        for packageID in priority_packages[truck.truckID]:
            package = package_table.search(packageID)
            if package:
                truck.load_package(package)
                package.status = "En Route"  # Reflect change in hash table
                package_table.insert(package.packageID, package)

# Step 2: Load remaining packages based on sorted order (deadline, then distance)
truck_index = 0  # Start with the first truck

for package in sorted_package_list:
    # Skip if package was already manually assigned
    if package.packageID in sum(priority_packages.values(), []):
        continue  

    truck = occupied_trucks[truck_index]  # Get next available truck

    if truck.load_package(package):
        package.status = "En Route"  # Update status in hash table
        package_table.insert(package.packageID, package)  

    # Move to the next truck (round-robin balancing)
    truck_index = (truck_index + 1) % len(occupied_trucks)

# Show the packages loaded onto each truck
for driver in drivers_list:
    packageCount = len(driver.truck.packageInventory)
    print(f"\nDriver {driver.driverID} is driving Truck {driver.truck.truckID} with the following packages (count = {packageCount}):")
    for i, package in enumerate(driver.truck.packageInventory, start=1):
        print(f'{i}. {package}')



# Show the status of all packages after loading onto trucks
print("\nPackage Status after loading onto trucks:\n")
for packageID in range(1, 41):  # Loop over package IDs 1 to 40
    package = package_table.search(packageID)  # Search using the correct ID
    if package:
        print(f"Status: {package.status}")

    
print("\nDelivering packages...\n")
# Deliver packages
for driver in drivers_list:
    deliver_packages(driver.truck, driver.truck.packageInventory)


# Show the status of all packages after delivery
print("\nPackage Status after delivery:\n")
for packageID in range(1, 41):  # Loop over package IDs 1 to 40
    package = package_table.search(packageID)  # Search using the correct ID
    if package:
        print(f"Status: {package.status}")














