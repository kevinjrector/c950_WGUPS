import datetime, time

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
