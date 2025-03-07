#handle routing here with Greedy Algorithm

import data_handler
import datetime
from hash_table import ChainingHashTable

package_table = ChainingHashTable()

data_handler.loadPackageData('./data/package_file.csv', package_table)

def sortPackages_byDeadline_and_Distance(package_list):
    """ Sorts a given list of packages by deadline first, then by distance from the hub. """
    
    hub_index = data_handler.extract_address('4001 South 700 East')  # Hub location index

    # Sort by deadline first, then by distance from the hub
    sorted_list = sorted(
        package_list, 
        key=lambda package: (
            package.get_deadline(),  # Sort by earliest deadline
            float(data_handler.distanceBetween(hub_index, data_handler.extract_address(package.get_address())))  # Then by closest distance
        )
    )

    return sorted_list  # Return sorted package list


def deliver_packages(truck, package_list):
    """Deliver packages while ensuring same-address packages have the same timestamp."""
    print(f"\n🚛 Truck {truck.truckID} STARTING route at {truck.departTime.strftime('%I:%M %p')} from {truck.currentLocation}.")

    current_time = truck.departTime
    total_distance = 0

    # Step 1: Group packages by delivery address
    deliveries_by_address = {}
    for package in package_list:
        if package.address not in deliveries_by_address:
            deliveries_by_address[package.address] = []
        deliveries_by_address[package.address].append(package)

    # Step 2: Deliver packages based on sorted order
    visited_addresses = set()
    for package in package_list:
        address = package.address

        # Skip if already delivered to this address
        if address in visited_addresses:
            continue

        # Calculate travel distance using your existing function
        hub_index = data_handler.extract_address(truck.currentLocation)
        package_index = data_handler.extract_address(address)
        distance_to_next = float(data_handler.distanceBetween(hub_index, package_index))

        # Calculate travel time
        travel_time = datetime.timedelta(minutes=(distance_to_next / truck.speed) * 60)

        # Update truck's travel state
        total_distance += distance_to_next
        current_time += travel_time
        truck.currentLocation = address
        visited_addresses.add(address)  # Mark as visited

        # Log travel information
        print(f"\nTruck {truck.truckID} TRAVELING {distance_to_next:.2f} miles to {address}.")
        print(f"   - Current Time: {current_time.strftime('%I:%M %p')}")
        print(f"   - Estimated Travel Time: {travel_time}")

        # Deliver **all packages** at this address at the same timestamp
        print(f"DELIVERED packages at {address} at {current_time.strftime('%I:%M %p')}:")
        for package in deliveries_by_address[address]:
            package.deliveryTime = current_time  # Assign the same timestamp
            package.status = "Delivered"
            truck.packageInventory.remove(package)  # ✅ Remove from truck inventory
            print(f"   - Package {package.packageID}")  # Logs all delivered packages


    if len(truck.packageInventory) == 0:
        hub_index = data_handler.extract_address("4001 South 700 East")
        last_index = data_handler.extract_address(truck.currentLocation)
        distance_back_to_hub = float(data_handler.distanceBetween(last_index, hub_index))
        return_time = current_time + datetime.timedelta(minutes=(distance_back_to_hub / truck.speed) * 60)
        truck.returnTime = return_time
        truck.atHub = True  # Mark truck as back at the hub

        print(f"\n✅ Truck {truck.truckID} returned to the Hub at {return_time.strftime('%I:%M %p')}. It is now waiting for reassignment.")


        # 🚨 Trigger next truck if waiting
        for waiting_truck in occupied_trucks:
            if waiting_truck.atHub and len(waiting_truck.packageInventory) > 0:
                print(f"🚛 Driver reassigned to Truck {waiting_truck.truckID}")
                waiting_truck.departTime = return_time
                deliver_packages(waiting_truck, waiting_truck.packageInventory)
                break



