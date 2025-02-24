import datetime

class Truck:
    def __init__(self, speed, milesTotal, currentLocation, departTime, packageInventory, startTime):
        self.speed = speed  # Truck speed in mph
        self.milesTotal = milesTotal  # Total miles traveled
        self.currentLocation = currentLocation  # Current truck location
        self.departTime = self.parse_datetime(departTime)  # Convert to full datetime
        self.startTime = self.parse_datetime(startTime)  # First departure from hub
        self.endTime = None  # Will be set when the truck returns to hub
        self.packageInventory = packageInventory  # List of packages on board

    def parse_datetime(self, time_str):
        """Converts a time string (e.g., '08:00 AM') to a full datetime object (today's date)."""
        today = datetime.datetime.today().date()
        return datetime.datetime.strptime(time_str, "%I:%M %p").replace(year=today.year, month=today.month, day=today.day)

    def update_departTime(self, travel_distance):
        """Updates departTime based on travel distance and speed."""
        travel_time = datetime.timedelta(hours=travel_distance / self.speed)
        self.departTime += travel_time  # Add travel time to current departTime

    def set_endTime(self):
        """Marks when the truck returns to the hub."""
        self.endTime = self.departTime  # Last departTime when all deliveries are done

    def __str__(self):
        return "Speed: {} mph | Miles Traveled: {} | Current Location: {} | Departure Time: {} | Start Time: {} | End Time: {} | Packages On Board: {}".format(
            self.speed, self.milesTotal, self.currentLocation, 
            self.departTime.strftime("%I:%M %p"), 
            self.startTime.strftime("%I:%M %p"), 
            self.endTime.strftime("%I:%M %p") if self.endTime else "Still Delivering", 
            len(self.packageInventory)
        )
