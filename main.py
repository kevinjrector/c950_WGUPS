from datetime import datetime, time
from data_handler import load_package_data
from routing import plan_deliveries
from truck import Truck
import user_interface

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
        currentLocation=HUB_LOCATION,  # Ensure all trucks start at HUB
        departTime=departure_times[i] if departure_times[i] else datetime.max,  # Avoid `None` issue
        capacity=TRUCK_CAPACITY
    ) for i in range(TOTAL_TRUCKS)
]

# 🚛 **Step 3: Run the Delivery Plan**
plan_deliveries(trucks, package_hashTable)

for truck in trucks:
    truckDepartime = truck.departTime.strftime('%I:%M %p')
    print(f"Truck {truck.truckID} Departed at {truckDepartime}")

    truckReturnTime = truck.returnTime.strftime('%I:%M %p') if truck.returnTime else "N/A"
    print(f"Truck {truck.truckID} Returned at {truckReturnTime}")


# 🚛 **Step 4: User Interface*
user_interface.userInterface(trucks, package_hashTable)  # Run the user interface


