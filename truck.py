class Truck:
    def __init__(self, speed, milesTotal, currentLocation, departTime, capacity, packageInventory):
        self.speed = speed  # Truck speed in mph
        self.milesTotal = milesTotal  # Total miles traveled at current time
        self.currentLocation = currentLocation  # Current truck location
        self.departTime = departTime  # departure time from hub
        self.returnTime = None  # Will be set when the truck returns to hub
        self.capacity = capacity  # Truck capacity
        self.packageInventory = packageInventory  # List of packages on board

       

    def __str__(self):
        return "Speed: {} mph | Miles Traveled: {} | Current Location: {} | Departure Time: {} | Depart Time: {} | Return Time: {} | Truck Capacity: {} | Packages On Board: {}".format(
            self.speed, self.milesTotal, self.currentLocation, self.departTime, self.returnTime, self.capacity, self.packageInventory
        )
