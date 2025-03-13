# Kevin J Rector - Student ID: 000958309  
"""
This is the main file that executes the delivery routing program. It loads the package data, plans the deliveries, and runs the user interface.

- I have defined the constants for the trucks, drivers, and hub location.
- Initalizes the Hash Table with the package data from our package_file.csv.
- Creates the truck objects with our defined constants and departure times.
- Plans the deliveries for the trucks.
- Loads the user interface to interact with the program.

"""

from datetime import datetime, time
from data_handler import load_package_data
from routing import plan_deliveries
from truck import Truck
import user_interface

# Constants for the delivery routing program
TRUCK_SPEED = 18  # MPH
TRUCK_CAPACITY = 16
TOTAL_TRUCKS = 3
TOTAL_DRIVERS = 2
HUB_LOCATION = "4001 South 700 East"
PACKAGE_FILE = './data/package_file.csv'

# Load the package data from the CSV file and initialize the hash table
package_hashTable = load_package_data(PACKAGE_FILE)

# Departure times for each truck
departure_times = [
    datetime.combine(datetime.today(), time(8, 0)),  
    datetime.combine(datetime.today(), time(9, 5)),   
    None  # Truck 3 waits for an available driver
]


# Truck objects are created with the defined constants and departure times
trucks = [
    Truck(
        truckID=i+1,
        speed=TRUCK_SPEED,
        currentLocation=HUB_LOCATION,  
        departTime=departure_times[i] if departure_times[i] else datetime.max,  # Avoid `None` issue
        capacity=TRUCK_CAPACITY
    ) for i in range(TOTAL_TRUCKS)
]


# Plan the deliveries for the trucks
plan_deliveries(trucks, package_hashTable)


# Load the user interface to interact with the program
user_interface.userInterface(trucks, package_hashTable)  


