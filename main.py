from truck import Truck
from driver import Driver
import datetime
from routing import sortPackages_byDeadline_or_byDistance, deliver_packages, package_table

# Global Simulation Clock
simulation_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))

def advance_time(minutes):
    """Advances the global simulation clock by a given number of minutes."""
    global simulation_time
    simulation_time += datetime.timedelta(minutes=minutes)
    return simulation_time

def deliver_packages_time_aware(truck):
    """Delivers packages while advancing simulation time dynamically."""
    global simulation_time
    print(f"\n🚛 {truck.truckID} STARTING route at {simulation_time.strftime('%I:%M %p')} from {truck.currentLocation}.")
    
    while truck.packageInventory:
        next_package = truck.packageInventory.pop(0)
        travel_time = truck.get_travel_time(next_package)
        advance_time(travel_time)
        
        next_package.status = "Delivered"
        next_package.deliveryTime = simulation_time.strftime('%I:%M %p')
        package_table.insert(next_package.packageID, next_package)
        
        print(f"DELIVERED Package {next_package.packageID} at {next_package.get_address()} at {simulation_time.strftime('%I:%M %p')}")

# Load and Dispatch Truck 1
print(f"\n🚛 Truck 1 is loaded and ready to depart at {simulation_time.strftime('%I:%M %p')}")
deliver_packages_time_aware(truck_1)