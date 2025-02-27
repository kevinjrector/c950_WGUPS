class Truck:
    def __init__(self, truckID, speed, milesTotal, currentLocation, departTime, capacity, packageInventory):
        self.truckID = truckID
        self.speed = speed  # Truck speed in mph
        self.milesTotal = milesTotal  # Total miles traveled at current time
        self.currentLocation = currentLocation  # Current truck location
        self.departTime = departTime  # departure time from hub
        self.capacity = capacity  # Truck capacity
        self.packageInventory = packageInventory  # List of packages on board
        self.returnTime = None  # Will be set when the truck returns to hub
        self.atHub = True  # Truck is at hub when initialized

       

    def __str__(self):
        return "Truck ID: {} | Speed: {} mph | Miles Traveled: {} | Current Location: {} | Departure Time: {} | Return Time: {} | Truck Capacity: {} | Packages On Board: {}".format(
            self.truckID, self.speed, self.milesTotal, self.currentLocation, self.departTime, self.returnTime, self.capacity, self.packageInventory
        )

    def drive_to(self, new_location, distance, travel_time):
        self.currentLocation = new_location
        self.milesTotal += distance
        self.departTime += travel_time
        self.atHub = False

    def load_package(self, package):

        if len(self.packageInventory) < self.capacity:
            self.packageInventory.append(package)
            return True
        else:
            return False
    