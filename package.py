import datetime

class Package:
    def __init__(self, packageID, address, deadline, city, state, zipCode, weight, status, deliveryTime=None):
        self.packageID = packageID
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state  
        self.zipCode = zipCode
        self.weight = weight
        self.status = status
        self.deliveryTime = deliveryTime

    def __str__(self):
        return "Package ID {}: {}, {}, {}, {} | Deadline: {} | Weight: {} kilos | Status: {} | Delivery Time: {}".format(
            self.packageID, self.address, self.city, self.state, self.zipCode, 
            self.deadline, self.weight, self.status, 
            self.deliveryTime
        )
    
    def get_deadline(self):
        """Returns the package's delivery deadline as a time object for sorting."""
        if self.deadline == 'EOD' or not self.deadline:
            # Set EOD packages to the end of the day (11:59 PM) instead of float('inf')
            return datetime.time(23, 59)  # 11:59 PM
        return datetime.datetime.strptime(self.deadline, '%I:%M %p').time()
    
    def get_delivery_time(self, current_time, distance, truck_speed):
        #Returns the time the package will be delivered
        #current_time is the time the truck leaves the hub
        #distance is the distance from the hub to the package's address
        #truck_speed is the average speed of the truck in mph
        delivery_time = current_time + datetime.timedelta(hours=distance/truck_speed)
        return delivery_time
    
    def get_address(self):
        return self.address
        
