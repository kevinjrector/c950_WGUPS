"""
This module contains the Truck class which is used to create truck objects.
A truck object contains important attributes such as the truck ID, speed, current location, and more.
"""
from datetime import timedelta

class Truck:
    def __init__(self, truckID, speed, currentLocation, departTime, capacity):
        self.truckID = truckID
        self.speed = speed 
        self.currentLocation = currentLocation 
        self.departTime = departTime
        self.capacity = capacity 
        self.packageInventory = [] 
        self.milesTotal = 0  
        self.milesTotal_list = [] 
        self.returnTime = None  
        self.current_time = departTime  
        self.atHub = True 

    def __str__(self):
        return f"Truck {self.truckID} | Speed: {self.speed} mph | Miles: {self.milesTotal} | Location: {self.currentLocation} | Depart Time: {self.departTime.strftime('%I:%M %p')} | Return Time: {self.returnTime.strftime('%I:%M %p') if self.returnTime else 'N/A'} | Packages: {len(self.packageInventory)}/{self.capacity}"

    def drive_to(self, new_location, distance):
        """
        Method to simulate driving the truck to a new location.
        Updates the truck's current location, time, and miles traveled.

        new_location: The destination location
        distance: The distance to the new location
        """
        starting_location = self.currentLocation
        travel_time = timedelta(minutes=(distance / self.speed) * 60)  # Convert hours to minutes
        self.current_time += travel_time
        self.currentLocation = new_location
        self.milesTotal += distance
        self.milesTotal_list.append(self.milesTotal)

        print(f"Time: {self.current_time.strftime('%I:%M %p')} 🚛 Truck {self.truckID} driving from {starting_location} to {new_location}")
        #print(f"   Distance: {distance} miles | Speed: {self.speed} mph with Expected travel time: {distance / self.speed:.2f} hours ({(distance / self.speed) * 60:.2f} minutes)")
        print(f" Distance: {distance}")
        
        return self.current_time


    def load_package(self, package, package_table):
        """
        Method to load a package onto the truck.
        Updates the package's status and the package table.

        package: The package to be loaded
        package_table: The hash table containing all packages

        Returns True if the package was successfully loaded, False if the truck is full.
        """
        # If the truck is not full, load the package
        if len(self.packageInventory) < self.capacity:
            self.packageInventory.append(package)
            package.status = "En Route" 
            package_table.insert(package.packageID, package)
            return True
        
        # If the truck is full, return False
        return False  

    def return_to_hub(self):
        """
        Method to simulate the truck returning to the hub.
        Updates the truck's current location, time, and
        sets the truck's return time.
        """
        self.atHub = True
        self.returnTime = self.current_time 
