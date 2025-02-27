class Driver:

    def __init__(self, driverID):
        self.driverID = driverID
        self.truck = None

    
    def assignTruck(self, truck):
        self.truck = truck

        
    def __str__(self):
        return "Driver ID: {} | Truck: {}".format(self.driverID, self.truck)
    
    