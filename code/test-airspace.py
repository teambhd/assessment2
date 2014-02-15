# ==============================
# STANDARD TEST FILE BOILERPLATE
# ==============================

import sys
from browser import doc

# Redefine the print keyword to append to our textarea
def write(something):
    doc['output'].text += something

sys.stdout.write = sys.stderr.write = write


# ==================
# LET'S GET STARTED!
# ==================

from airspace import *
print("\n== test-airspace.py ==")


# ==================================
# TEST THE DISTANCE_BETWEEN FUNCTION 
# ==================================

print("\nSome basic tests of the distance_between function. The distances from (1, 1) to (1, 6), from (1, 1) to (6, 1) and from (0, 0) to (3, 4) should all be 5.")

d1 = distance_between(1, 1, 1, 6)
d2 = distance_between(1, 1, 6, 1)
d3 = distance_between(0, 0, 3, 4)

if (d1 == 5) and (d2 == 5) and (d3 == 5):
    print("PASS: All three calculations returned 5")
    
else:
    print("FAIL: Returned results were " + str(d1) + ", " + str(d2) + " and " + str(d3))


# ============================================================================================
# SET UP THE TEST AIRSPACE, AND IN DOING SO, TEST THE AIRSPACE CLASS'S INITIALISATION FUNCTION 
# ============================================================================================

print("\nAttempting to create our test airspace, and testing to see if input values are loaded into the correct class properties. Calling t = Airspace(10000, 10000, 10000, 500, 500)")

t = Airspace(10000, 10000, 10000, 500, 500)

if (t.x == 10000) and (t.y == 10000) and (t.z == 10000) and (t.hsep == 500) and (t.vsep == 500):
    print("PASS: All values loaded and retrieved correctly")
    
else:
    print("FAIL: Returned values were " + str(t.x) + ", " + str(t.y) + ", " + str(t.z) + ", " + str(t.hsep) + " and " + str(t.vsep))
    
    
# =====================
# TEST WAYPOINT METHODS
# =====================

print("\nTesting the add_edge_waypoint function. Adding a waypoint then checking to see if it has been added and all properties carried across correctly.")

t.add_edge_waypoint('EntryPoint', 5000, 0)

if ('EntryPoint' in t.edge_waypoints) and (t.edge_waypoints['EntryPoint'].x == 5000) and (t.edge_waypoints['EntryPoint'].y == 0):
    print("PASS: Edge waypoint created successfully")
    
else:
    print("FAIL: Waypoint doesn't exist or has incorrect parameters.")
    