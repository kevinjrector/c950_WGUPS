import csv
from package import Package



with open('./data/address_file.csv', newline='') as csvfile:
    CSV_Address = csv.reader(csvfile)
    CSV_Address = list(CSV_Address)

with open('./data/distance_file.csv', newline='') as csvfile:
    CSV_Distance = csv.reader(csvfile)
    CSV_Distance = list(CSV_Distance)


def loadPackageData(file, hash_table):
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

            package = Package(packageID, address, deadline, city, state, zipCode, weight, status)
            hash_table.insert(packageID, package)


def distanceBetween(x_value, y_value):

    if x_value is None or y_value is None:
        return 0.0  # Return safe default value

    try:
        if x_value >= len(CSV_Distance) or y_value >= len(CSV_Distance):
            return 0.0

        # Read the value and check reverse direction if missing
        distance = CSV_Distance[x_value][y_value].strip() if CSV_Distance[x_value][y_value] else ''
        if not distance:
            distance = CSV_Distance[y_value][x_value].strip() if CSV_Distance[y_value][x_value] else ''

        return float(distance) if distance else 0.0  # Return 0.0 if still missing
    except (IndexError, ValueError):
        return 0.0  # Default safe value


def extract_address(address):
    """
    Finds the index of an address in CSV_Address.
    Normalizes addresses by stripping spaces and converting to lowercase.
    """
    normalized_address = address.strip().lower()

    for index, row in enumerate(CSV_Address):
        if len(row) < 2:  # Ensure row has an address
            continue  # Skip malformed rows
        
        row_address = row[1].strip().lower()  # Normalize CSV address

        if row_address == normalized_address:
            return index  # Index corresponds to distance matrix

    return None  # Return None if not found




