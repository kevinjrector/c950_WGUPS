import csv
from package import Package
from hash_table import ChainingHashTable  # Import the custom hash table

# Load address and distance data
with open('./data/address_file.csv', newline='') as csvfile:
    CSV_Address = list(csv.reader(csvfile))

with open('./data/distance_file.csv', newline='') as csvfile:
    CSV_Distance = list(csv.reader(csvfile))


def load_package_data(file):
    """ Creates and loads a hash table with package data from the CSV file. """
    package_table = ChainingHashTable()  # Initialize the package hash table

    with open(file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header row if it exists

        for row in csv_reader:
            packageID = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipCode = row[4]
            deadline = row[5]
            weight = float(row[6])
            status = "At Hub"

            # Create Package object and insert it into the hash table
            package = Package(packageID, address, deadline, city, state, zipCode, weight, status)
            package_table.insert(packageID, package)

    return package_table  # Return the populated package table


def distanceBetween(x_value, y_value):
    """ Returns the distance between two addresses using the CSV distance matrix. """
    if x_value is None or y_value is None or x_value >= len(CSV_Distance) or y_value >= len(CSV_Distance):
        return 0.0  # Return safe default value

    distance = CSV_Distance[x_value][y_value].strip() or CSV_Distance[y_value][x_value].strip()
    return float(distance) if distance else 0.0


# Create a mapping of addresses to their index in CSV_Address
address_map = {row[1].strip().lower(): index for index, row in enumerate(CSV_Address)}

def extract_address(address):
    """ Converts an address string to its corresponding index in the distance table. """
    return address_map.get(address.strip().lower(), None)
