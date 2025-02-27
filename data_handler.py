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
    distance = CSV_Distance[x_value][y_value]
    if distance == '':
        distance = CSV_Distance[y_value][x_value]

    return float(distance)

# Method to get address number from string literal of address
def extract_address(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])



