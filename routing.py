from distance_table import loadDistanceTable
from distance_table import get_distance

file_path = "./data/distance_table.csv"
location_map, distance_matrix = loadDistanceTable(file_path)

print("Distance between WGU and Sugar House Park:",
        get_distance("Western Governors University 4001 South 700 East",
                    "Sugar House Park", location_map, distance_matrix))