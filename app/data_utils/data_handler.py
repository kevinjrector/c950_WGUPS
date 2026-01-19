"""
This module handles the loading of data from CSV files and provides utility functions for extracting address data.
"""
import csv
from app.models.package import Package
from app.models.hash_table import ChainingHashTable  # Import the custom hash table

ADDRESS_FILE = "./data/address_file.csv"
DISTANCE_FILE = "./data/distance_file.csv"

def load_package_data(file):
    """
    Loads package data from a CSV file and populates the package hash table.

    Returns the populated hash table.
    """
    # Create a hash table to store the package data
    package_table = ChainingHashTable()  

    with open(file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) 

        for row in csv_reader:
            packageID = int(row[0])
            address = row[1]  
            city = row[2]
            state = row[3]
            zipCode = row[4]
            deadline = row[5]
            weight = float(row[6])
            special_notes = row[7] if len(row) > 7 else None 
            status = "At Hub"

            # Create Package object and insert into the hash table
            package = Package(packageID, address, deadline, city, state, zipCode, weight, status)
            package.special_notes = special_notes 
            package_table.insert(packageID, package)

    # Return the populated hash table
    return package_table  


def load_address_data(file):
    """
    Loads address data from a CSV file and returns a dictionary with addresses as keys and indices as values

    Returns the populated address dictionary.
    """
    # Initialize an empty dictionary to store the address data
    address_dict = {}

    with open(file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)

        for idx, row in enumerate(csv_reader):
            if len(row) > 1:
                address = row[1].strip() # Use the second column as the address
                address_dict[address] = idx  # Assign each address a unique index
            else:
                print(f"Skipping row {idx} due to missing address.")

    # Return the populated address dictionary
    return address_dict


def load_distance_data(file):
    """
    Loads distance data from a CSV file and returns a 2D list representing the distance between locations

    Returns the populated distance matrix.
    """
    distance_matrix = []

    with open(file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            distance_matrix.append([float(cell) if cell else None for cell in row])  # Convert to floats, handle empty values

    # Fill missing values by mirroring (A → B should match B → A)
    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix[i])):
            if distance_matrix[i][j] is None and distance_matrix[j][i] is not None:
                distance_matrix[i][j] = distance_matrix[j][i]  # Mirror the value
            elif distance_matrix[i][j] is None and distance_matrix[j][i] is None:
                distance_matrix[i][j] = float('inf') 

    # Return the populated distance matrix
    return distance_matrix



def extract_address(address, address_dict):
    """
    Extracts the index of an address from the address dictionary.

    address: The address to look up
    address_dict: The dictionary containing address data

    Returns the index of the address in the dictionary.
    """
    
    # Check if the address exists in the dictionary and return the index
    if address in address_dict:
        return address_dict[address]

    print(f"ERROR: Address '{address}' not found in address_dict!")
    return None  # Prevent crashing if address is not found



def distanceBetween(index1, index2, distance_matrix):
    """
    Returns the distance between two locations based on their indices in the distance matrix.

    index1: The index of the first location
    index2: The index of the second location
    distance_matrix: The 2D list containing distance data

    Returns the distance between the two locations.
    """
    if index1 is not None and index2 is not None:
        distance = distance_matrix[index1][index2]
        return distance if distance is not None else float('inf')  # Prevents crashing if distance is missing
    return float('inf') 
