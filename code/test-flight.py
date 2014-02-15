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

from flight import *
print("\n== test-flight.py ==")


# ========================================================================================
# SET UP THE TEST FLIGHT, AND IN DOING SO, TEST THE FLIGHT CLASS'S INITIALISATION FUNCTION 
# ========================================================================================

print("\nAttempting to create our test flight, and testing to see if input values are loaded into the correct class properties.")

args = [5000, 5000, 1000, 100, ['North', 'South'], 0, 1000, 'AB123', 'Test', 'small', aircraft_specs['small']]
props = ['x', 'y', 'altitude', 'speed', 'waypoints', 'bearing', 'fuel', 'code', 'name', 'size', 'limitations']

# argh, this really isn't elegant but it saves lots of typing!
cmd = 'Flight(' + str(args)[1:-1] + ')' 
print('Executing: test_flight = ' + cmd)
test_flight = eval(cmd)

failures = 0
for arg, prop in zip(args, props):
    value = eval('test_flight.' + prop)
    if value != arg:
        print("FAIL: " + prop + "not returned successfully.")
        print("      Expected " + str(arg) + "but received " + str(value))
        failures += 1
        
if failures == 0:
    print("PASS: All values read back successfully")

    
# ====================================
# TESTS ON THE UPDATE_BEARING FUNCTION
# ====================================
    
print("\nTesting the update_bearing function. Issue a target bearing of 90 and see if the plane eventually reaches it.")

test_flight.target_bearing = 90

# Give the plane the equivalent of 100 seconds worth of flying, which should be more than enough to make the turn
for i in range(1, 2000):
    test_flight.update_bearing(0.05) # = 20fps
    
if test_flight.bearing == 90:
    print("PASS: Plane turned to 90 degree heading successfully")
    
else:
    print("FAIL: Plane ended up on a heading of " + str(test_flight.bearing) + " degrees")
    
    
print("\nAlso test turning through 0 degrees to 271 degrees, to check if bearings remain within bounds correctly.")

test_flight.target_bearing = 271

# Give the plane the equivalent of 100 seconds worth of flying, which should be more than enough
for i in range(1, 2000):
    test_flight.update_bearing(0.05) # = 20fps
    
if test_flight.bearing == 271:
    print("PASS: Plane turned to 271 degree heading successfully")
    
else:
    print("FAIL: Plane ended up on a heading of " + str(test_flight.bearing) + " degrees")
    
    
print("\nTurning to exactly 0 degrees has been problematic at various points during development, so we'll test that specific case as well.")

test_flight.target_bearing = 0

# Give the plane the equivalent of 100 seconds worth of flying, which should be more than enough
for i in range(1, 2000):
    test_flight.update_bearing(0.05) # = 20fps
    
if test_flight.bearing == 0:
    print("PASS: Plane turned to 0 degree heading successfully")
    
else:
    print("FAIL: Plane ended up on a heading of " + str(test_flight.bearing) + " degrees")


# =====================================
# TESTS ON THE UPDATE_ALTITUDE FUNCTION
# =====================================

print("\nTesting the update_altitude function. First we'll try descending to 500m.")

test_flight.target_altitude = 500

# Give the plane the equivalent of 100 seconds worth of flying, which should be more than enough
for i in range(1, 2000):
    test_flight.update_altitude(0.05) # = 20fps
    
if test_flight.altitude == 500:
    print("PASS: Plane descended to 500m successfully")
    
else:
    print("FAIL: Plane ended up on at " + str(test_flight.altitude) + "m")
    
    
print("\nNow we'll try ascending to an altitude of 2000m")

test_flight.target_altitude = 2000

# Give the plane the equivalent of 100 seconds worth of flying, which should be more than enough
for i in range(1, 2000):
    test_flight.update_altitude(0.05) # = 20fps
    
if test_flight.altitude == 2000:
    print("PASS: Plane ascended to 2000m successfully")
    
else:
    print("FAIL: Plane ended up on at " + str(test_flight.altitude) + "m")


# ==========================
# TESTS ON THE MOVE FUNCTION
# ==========================

# To save cpu cycles we'll only have one go at calling the move function and use that for all the following tests.
for i in range(1, 2000):
    test_flight.move(50) # = 20fps


print("\nTest that fuel is reducing as distance is covered")
    
if test_flight.fuel < 1000:
    print("PASS: Fuel is decreasing")

else:
    print("FAIL: Currently has " + str(test_flight.fuel) + "l of fuel")
    
    
print("\nTest that aircraft is moving along the correct axis (should still have a bearing of 0)")

if (test_flight.x == 5000) and (test_flight.y > 5000):
    print("PASS: Plane appears to be moving in the correct direction")
    
else:
    print("FAIL: Plane appears to be moving erratically. Position is ("+ str(test_flight.x) + ", " + str(test_flight.y) + ")")
    