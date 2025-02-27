#handle routing here with Greedy Algorithm

import data_handler
import datetime
from hash_table import ChainingHashTable

package_table = ChainingHashTable()

data_handler.loadPackageData('./data/package_file.csv', package_table)

def sortPackages_byDeadline_or_byDistance():

    hub_index = data_handler.extract_address('4001 South 700 East')
    sorted_package_list = []

    for packageID in range(1, 41):
        package = package_table.search(packageID)
        
        if package:
            packageAddress_index = data_handler.extract_address(package.get_address())
            distance = float(data_handler.distanceBetween(hub_index, packageAddress_index))
            sorted_package_list.append((package, distance))

    sorted_package_list.sort(key=lambda x: (x[0].get_deadline(), x[1]))

    return[package[0] for package in sorted_package_list]



def deliver_packages(truck, package_table):
    hub_index = data_handler.extract_address('4001 South 700 East')
    current_time = truck.departTime

    while truck.packageInventory:
        current_location_index = data_handler.extract_address(truck.currentLocation)
        closest_package = None
        shortest_distance = float('inf')

        for package in truck.packageInventory:
            package_address_index = data_handler.extract_address(package.get_address())
            distance = data_handler.distanceBetween(current_location_index, package_address_index)

            if distance < shortest_distance:
                closest_package = package
                shortest_distance = distance

        if closest_package:
            # Calculate travel time
            travel_time = datetime.timedelta(hours=shortest_distance / truck.speed)
            delivery_time = current_time + travel_time  # Correctly update truck's departure time

            # Move truck to package location
            truck.drive_to(closest_package.get_address(), shortest_distance, travel_time)

            # Mark package as delivered and set delivery time
            closest_package.status = "Delivered"
            closest_package.deliveryTime = delivery_time

            # Remove package from truck inventory
            truck.packageInventory.remove(closest_package)

            print(f"Truck {truck.truckID} delivered package {closest_package.packageID} to {closest_package.address} at {delivery_time.strftime('%I:%M %p')}.")

            # Update current truck time
            current_time = delivery_time

    # Ensure truck's return time is correct
    return_to_hub_distance = data_handler.distanceBetween(current_location_index, hub_index)
    travel_time_to_hub = datetime.timedelta(hours=return_to_hub_distance / truck.speed)

    truck.drive_to("4001 South 700 East", return_to_hub_distance, travel_time_to_hub)

    # Always update return time
    truck.returnTime = current_time + travel_time_to_hub if current_time != truck.departTime else truck.departTime

    print(f"\nTruck {truck.truckID} completed deliveries and returned to the Hub at {truck.returnTime.strftime('%I:%M %p')}. Total miles: {truck.milesTotal:.2f} miles.\n")



