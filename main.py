from package import Package
from hash_table import ChainingHashTable

myHashTable = ChainingHashTable()

# Create a package
package = Package(1, "123 Main St", "10:30 AM", "Salt Lake City", "84101", 5.0, "At Hub")

myHashTable.insert(package.packageID, package)

package = myHashTable.search(1)

if myHashTable.search(1):
    print(package)
else:
    print("error")


