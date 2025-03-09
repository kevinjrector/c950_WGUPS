import csv
from package import Package
from hash_table import ChainingHashTable  # Import the custom hash table

ADDRESS_FILE = "./data/address_file.csv"
DISTANCE_FILE = "./data/distance_file.csv"

def load_package_data(file):
    """Creates and loads a hash table with package data from the CSV file."""
    package_table = ChainingHashTable()  # Initialize the package hash table

    with open(file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            packageID = int(row[0])
            address = row[1]  # Now using the correct address column
            city = row[2]
            state = row[3]
            zipCode = row[4]
            deadline = row[5]
            weight = float(row[6])
            special_notes = row[7] if len(row) > 7 else None  # Handle special notes
            status = "At Hub"

            # Create Package object and insert into the hash table
            package = Package(packageID, address, deadline, city, state, zipCode, weight, status)
            package.special_notes = special_notes  # Store special requirements
            package_table.insert(packageID, package)

    return package_table  # Return the populated package table


def load_address_data(file):
    """Loads addresses from CSV and maps them to an index for lookups using COLUMN 1."""
    address_dict = {}

    with open(file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for idx, row in enumerate(csv_reader):
            if len(row) > 1:
                address = row[1].strip()  # Now using column 1 (actual address)
                address_dict[address] = idx  # Assign each address a unique index
            else:
                print(f"⚠️ WARNING: Skipping row {idx} due to missing address.")

    return address_dict


def load_distance_data(file):
    """Loads distance data from the CSV file into a 2D list and mirrors missing values."""
    distance_matrix = []

    with open(file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            distance_matrix.append([float(cell) if cell else None for cell in row])  # Convert to floats, handle empty values

    # Mirror missing values (if row[i][j] is missing, use row[j][i])
    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix[i])):
            if distance_matrix[i][j] is None and distance_matrix[j][i] is not None:
                distance_matrix[i][j] = distance_matrix[j][i]  # Mirror the value

    return distance_matrix


def extract_address(address, address_dict):
    """Retrieves the index of a location in the distance matrix, ensuring exact 1:1 mapping."""
    
    if address in address_dict:
        return address_dict[address]

    print(f"❌ ERROR: Address '{address}' not found in address_dict!")
    return None  # Prevent breaking logic



def distanceBetween(index1, index2, distance_matrix):
    """Fetches the distance between two locations given their indices."""
    if index1 is not None and index2 is not None:
        distance = distance_matrix[index1][index2]
        return distance if distance is not None else float('inf')  # Prevents breaking sorting
    return float('inf')  # If lookup fails, return large distance
