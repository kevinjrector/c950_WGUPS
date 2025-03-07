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
    if x_value is None or y_value is None or x_value >= len(CSV_Distance) or y_value >= len(CSV_Distance):
        return 0.0  # Return safe default value

    distance = CSV_Distance[x_value][y_value].strip() or CSV_Distance[y_value][x_value].strip()
    return float(distance) if distance else 0.0



address_map = {row[1].strip().lower(): index for index, row in enumerate(CSV_Address)}

def extract_address(address):
    return address_map.get(address.strip().lower(), None)





