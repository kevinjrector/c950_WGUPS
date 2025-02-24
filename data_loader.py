import csv
from package import Package

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
