"""
This module contains the Package Class which is used to create package objects
A package object contains important attributes such as the package ID, address, dealdline, and more
updateTime and oldAddress are used to keep track of a package's status and address changes, this is primarily for packages that are delayed or have errors

There are 3 methods the Package class contains to return the package's deadline, delivery time, and address
"""
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
        self.assignedTruck = None
        self.updateTime = None
        self.oldAddress = None
        self.lateStatus = False
        self.hubArrivalTime = None

    def __str__(self):
        return "Package ID {}: {}, {}, {}, {} | Deadline: {} | Weight: {} kilos | Status: {} | Delivery Time: {}".format(
            self.packageID, self.address, self.city, self.state, self.zipCode, 
            self.deadline, self.weight, self.status, 
            self.deliveryTime
        )
    
    def get_deadline(self):
        """
        Returns the package's delivery deadline as a time object for sorting.
        If the deadline is 'EOD' or missing, it defaults to 11:59 PM.
        """
        if self.deadline == 'EOD' or not self.deadline:
            return datetime.time(23, 59)  # 11:59 PM
        return datetime.datetime.strptime(self.deadline, '%I:%M %p').time()
    
    def get_delivery_time(self, current_time, distance, truck_speed):
        """
        Returns the estimated delivery time for a package based on the current time, distance, and truck speed.
        """

        delivery_time = current_time + datetime.timedelta(hours=distance/truck_speed)
        return delivery_time
    
    def get_address(self):
        """
        Returns the package's destination address.
        """
        return self.address
        
