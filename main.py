from package import Package
from data_loader import loadPackageData
from hash_table import ChainingHashTable

myHashTable = ChainingHashTable()

loadPackageData('./data/package_file.csv', myHashTable)

print("Print Packages from Hash Table")

packageID = 1

for packageID in range(1, 41):
    package = myHashTable.search(packageID)
    if package:
        print(package)
    else:
        print("Package not found!")
