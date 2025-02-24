import datetime, time

EOD = time(23, 59)

class Package:
    def __init__(self, packageID, address, deadline, city, state, zipCode, weight, status, deliveryTime=None):
        self.packageID = packageID
        self.address = address
        self.deadline = self.parse_deadline(deadline)
        self.city = city
        self.state = state  
        self.zipCode = zipCode
        self.weight = weight
        self.status = status
        self.deliveryTime = self.parse_delivery_time(deliveryTime)

    def parse_deadline(self, deadline_str):
        """Converts deadline to datetime or keeps it as 'EOD'."""
        if deadline_str == "EOD":
            return "EOD"
        return datetime.datetime.strptime(deadline_str, "%I:%M %p").time()

    def parse_delivery_time(self, delivery_time):
        """Stores deliveryTime as a datetime object or 'EOD'."""
        if delivery_time is None or delivery_time == "EOD":
            return "EOD"
        return datetime.datetime.strptime(delivery_time, "%I:%M %p").time()
    
    

    def __str__(self):
        return "Package ID {}: {}, {}, {}, {} | Deadline: {} | Weight: {} kilos | Status: {} | Delivery Time: {}".format(
            self.packageID, self.address, self.city, self.state, self.zipCode, 
            self.deadline if self.deadline != "EOD" else "EOD", 
            self.weight, self.status, 
            self.deliveryTime.strftime("%I:%M %p") if self.deliveryTime != "EOD" else "EOD"
        )
