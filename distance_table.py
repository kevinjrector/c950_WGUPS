import csv

def loadDistanceTable(file):
    """Loads the distance table from a CSV file into a 2D matrix and a location dictionary."""
    
    location_map = {}  # Maps location names to an index
    distance_matrix = []  # 2D list for distances

    with open(file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)  # Read header row

        # Create mapping of locations to indices (skip "Location Name" & "Address")
        for i, location in enumerate(headers[2:]):  
            location_map[location.strip()] = i  

        # Read distances into a 2D list
        for row in csv_reader:
            location_name = row[0].strip()
            if location_name not in location_map:
                continue  

            row_distances = [0.0] * len(location_map)  # Initialize row with zeros

            for col_index in range(2, len(row)):  
                if row[col_index]:  
                    try:
                        distance = float(row[col_index])
                        row_distances[col_index - 2] = distance  
                    except ValueError:
                        print(f"Warning: Invalid distance value at {location_name} -> {headers[col_index]}")

            distance_matrix.append(row_distances)  

    # **Mirroring the matrix AFTER importing**
    num_locations = len(distance_matrix)
    for i in range(num_locations):
        for j in range(i + 1, num_locations):
            if distance_matrix[i][j] == 0.0 and distance_matrix[j][i] != 0.0:
                distance_matrix[i][j] = distance_matrix[j][i]
            elif distance_matrix[j][i] == 0.0 and distance_matrix[i][j] != 0.0:
                distance_matrix[j][i] = distance_matrix[i][j]

    return location_map, distance_matrix  # Return dictionary and matrix

def get_distance(location1, location2, location_map, distance_matrix):
    """Returns the distance between two locations using the distance matrix."""
    index1 = location_map.get(location1)
    index2 = location_map.get(location2)
    if index1 is None or index2 is None:
        return None  
    return distance_matrix[index1][index2]  