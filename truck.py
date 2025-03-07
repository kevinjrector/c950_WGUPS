from datetime import datetime, timedelta

class Truck:
    def __init__(self, truckID, speed, currentLocation, departTime, capacity):
        self.truckID = truckID
        self.speed = speed  # Truck speed in mph
        self.currentLocation = currentLocation  # Current truck location
        self.departTime = departTime  # Initial departure time (can be updated)
        self.capacity = capacity  # Max capacity (16 packages)
        self.packageInventory = []  # Packages loaded onto the truck
        self.milesTotal = 0  # Total miles traveled
        self.returnTime = None  # Time the truck returns to hub
        self.current_time = departTime  # Tracks when deliveries occur
        self.atHub = True  # True if truck is at the hub

    def __str__(self):
        return f"🚛 Truck {self.truckID} | Speed: {self.speed} mph | Miles: {self.milesTotal} | Location: {self.currentLocation} | Depart Time: {self.departTime.strftime('%I:%M %p')} | Return Time: {self.returnTime.strftime('%I:%M %p') if self.returnTime else 'N/A'} | Packages: {len(self.packageInventory)}/{self.capacity}"

    def drive_to(self, new_location, distance):
        """
        Moves the truck to a new location, updating its time and total miles.
        """
        travel_time = timedelta(minutes=(distance / self.speed) * 60)  # Convert travel time to minutes
        self.currentLocation = new_location
        self.milesTotal += distance
        self.current_time += travel_time  # Update current time
        self.atHub = False  # The truck is no longer at the hub

        return self.current_time  # Return updated time for tracking

    def load_package(self, package, package_table):
        """
        Loads a package onto the truck if space is available.
        Also updates package status in the hash table.
        """
        if len(self.packageInventory) < self.capacity:
            self.packageInventory.append(package)
            package.status = "En Route"  # Update status
            package_table.insert(package.packageID, package)  # Update package table
            return True
        return False  # If truck is full, return False

    def return_to_hub(self):
        """
        Marks the truck as returning to the hub and updates time.
        """
        self.atHub = True
        self.returnTime = self.current_time  # Truck's return time is when it arrives back
