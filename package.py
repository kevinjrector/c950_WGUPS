class Package:
    def __init__(self, packageID, address, deadline, city, zipCode, weight, status, deliveryTime=None):
        self.packageID = packageID
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipCode = zipCode
        self.weight = weight
        self.status = status
        self.deliveryTime = deliveryTime

    def __str__(self):
        return "Package ID {}: {}, {}, {} | Deadline: {} | Weight: {} lbs | Status: {} | Delivery Time: {}".format(
            self.packageID, self.address, self.city, self.zipCode, self.deadline, 
            self.weight, self.status, self.deliveryTime if self.deliveryTime else "Not Delivered"
        )

