import string
import random
import math

from flight import Flight, aircraft_specs, aircraft_names
from waypoint import Waypoint, phonetic_alphabet


# ===============================
# UTILITY FUNCTIONS FOR AIRSPACES
# ===============================

def distance_between(x1, y1, x2, y2):
    # Finds the distance between two 2D points 
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2)) # ** is a power in Python - e.g x squared is x ** 2
    
        
# ==================
# THE AIRSPACE CLASS
# ==================

class Airspace:
    
    # ==============
    # INITIALISATION
    # ==============
    
    def __init__ (self, x, y, z, hsep, vsep):
        # x, y and z are the dimensions of the airspace
        self.x = x
        self.y = y
        self.z = z
                
        # dictionary flights contains a Flight object for each plane within this airspace, keyed by flight code
        self.flights = {}
                
        # these 2 dictionaries contain a Waypoint object for each waypoint (incl. airports, entry/exit points)
        self.edge_waypoints = {}
        self.simple_waypoints = {}
        
        # The horizontal and vertical separation distances in force for this airspace
        self.hsep = hsep
        self.vsep = vsep
                
        # The frequency in ms, at which the airspace is going to be updated
        self.timestep = 0
        
        
    # ==============
    # REPRESENTATION
    # ==============
     
    def __repr__ (self):
        return "Airspace of size: " + str(self.x) + "m by " + str(self.y) + "m by " + str(self.z) + "m."


    # ==============================
    # METHODS DEALING WITH WAYPOINTS
    # ==============================
    
    # when all waypoints are needed, they can be accessed at self.waypoints via the following line    
    waypoints = property(lambda self: dict(list(self.edge_waypoints.items()) + list(self.simple_waypoints.items())))
    
    def add_edge_waypoint(self, name, x, y):
        # Edge waypoints must be added on an edge, or they just don't make any sense
        assert (x == 0) or (x == self.x) or (y == 0) or (y == self.y)
        
        self.edge_waypoints[name] = Waypoint(name, x, y, 'edge')    
        return None
        
    def new_simple_waypoint(self):
        # Uses a phonetic alphabet identifier, doubling up after 26 waypoints (like MS Excel column names)
        # e.g. n = 2 gives 'Charlie', n = 27 gives 'AlphaBravo'
        n = len(self.simple_waypoints)
        f = int(math.floor(n/26))
                        
        if f == 0:
            name = phonetic_alphabet[n]
    
        else:
            name = phonetic_alphabet[f-1] + phonetic_alphabet[n-26*f]
            
        # Generate a random location, avoiding edges and other waypoints    
        while True:
            x = random.randint(3000, self.x-3000)
            y = random.randint(3000, self.y-3000)
            for w in self.simple_waypoints.values():
                if distance_between(x, y, w.x, w.y) < 3000:
                    break # out of the for loop
            else: # else statements on loops are quite a nice feature of Python - see bit.ly/1bIO6Tk for details
                break # out of the while loop
                
        self.simple_waypoints[name] = Waypoint(name, x, y, 'simple')
        return None
        
              
    # ============================
    # METHODS DEALING WITH FLIGHTS
    # ============================
        
    def new_flight(self, origin):
        # Creates a new flight, and adds it to the flights dictionary
                
        # Get a random code for this flight, looping until we get one that's not currently in use
        while True:
            # A flight code is, as in real life, two uppercase letters followed by three numbers
            # e.g. BA234 or LH940
            code  = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
            code += str(random.randint(100,999))
            if code not in self.flights:
                break    
        
        # Get size, aircraft name and limitations
        size = random.choice(['small', 'medium', 'jumbo'])
        limitations = aircraft_specs[size]
        name = random.choice(aircraft_names[size])
                
        # Get initial altitude
        altitude = random.randint(1000, limitations['max_altitude']-1000)
        
        # Let's just assume that planes always fly at their top speed
        speed = limitations['max_speed']
                
        # Select a destination for the flight, from a list of edge waypoints (excluding the entry point)
        while True:
            destination = random.choice(list(self.edge_waypoints.values()))
            if destination != origin:
                break
                
        flight_plan = [origin]
                
        # Get 2 intermediate waypoints, between the entry point and the destination
        waypoints = list(self.simple_waypoints.values())
        random.shuffle(waypoints)
        for v in waypoints:
            
            if len(flight_plan) == 3:
                break
            
            for w in waypoints:
                if w == v:
                    continue
                
                # This humungous if statement tries to ensure that doubling-back between waypoints is avoided.    
                if (distance_between(v.x, v.y, destination.x, destination.y) > distance_between(w.x, w.y, destination.x, destination.y) and distance_between(origin.x, origin.y, v.x, v.y) < distance_between(origin.x, origin.y, w.x, w.y)):
                    flight_plan.append(v)
                    flight_plan.append(w)
                    break
                                
        flight_plan.append(destination)
        
        # Calculate the bearing to the first waypoint
        bearing = round(90 - math.degrees(math.atan2(flight_plan[1].y - origin.y, flight_plan[1].x - origin.x)))
        
        # The above line generates bearings between -180 and 180, 
        # we need to get a bearing between 0 and 360 to give to the new flight
        if bearing < 0:
            bearing += 360
        
        
        # Give the flight enough fuel to cover twice the optimal distance it needs to cover
        fuel = 0
                
        for a, b in zip(flight_plan[:-1], flight_plan[1:]):
            fuel += int((distance_between(a.x, a.y, b.x, b.y) * 2) / (limitations['kmpl'] * 1000))
        
        fuel = min(fuel, limitations['max_fuel']) # but not more than the aircraft's tanks will hold
        
        self.flights[code] = Flight(origin.x, origin.y, altitude, speed, flight_plan, bearing, fuel, code, name, size, limitations)
        
        return None
                        
                
    # ==============================
    # METHODS TO UPDATE THE AIRSPACE
    # ==============================
    
    def update_airspace(self):
        # Updates the positions of all aircraft within the airspace 
        # To be called on a regular basis by a timer
        
        # Move all aircraft
        for f in self.flights.values():
            f.move(self.timestep)
            
            # Check to see if the flight has reached it's next waypoint
            if distance_between(f.x, f.y, f.next_waypoint.x, f.next_waypoint.y) < 400:
                
                # If the next waypoint is the destination waypoint
                if f.next_waypoint == f.waypoints[-1]:
                    del self.flights[f.code]
                    # Here we could add some points, if this were assessment 3
                    continue
                
                else:
                    # Bump the next waypoint reference one further along in the flight plan
                    f.next_waypoint = f.waypoints[f.waypoints.index(f.next_waypoint) + 1]
                    # Here we could add some points, if this were assessment 3
            
            # Terminate flights that have left the airspace
            if (f.x > self.x) or (f.x < 0) or (f.y > self.y) or (f.y < 0):
                del self.flights[f.code]
                                
        return None
    
    def monitor_separation(self): 
        # This function monitors the separation rules, and also handles actual crashes between aircraft. 
        # Will be called frequently on a timer.
        # Return values are 1: Was there a crash, 2 and 3: the planes involved.
        
        # No sense going any further if there are no flights on screen
        if not self.flights:
            return False, None, None
        
        # Remove the flag, if separation harmony was restored by the last-but-one plane leaving the screen
        if (len(self.flights) == 1) and (list(self.flights.values())[0].flag == True):
            list(self.flights.values())[0].flag = False
        
        for a in self.flights.values():
            
            # Before we get onto checking distances, make the plane hasn't run out of fuel
            if a.fuel <= 0:
                return True, a, None
            
            for b in self.flights.values():
                
                if a == b:
                    continue
                                    
                alt_diff = abs(a.altitude - b.altitude)
                
                if alt_diff < self.vsep:
                    
                    pos_diff = distance_between(a.x, a.y, b.x, b.y)
                    
                    if (alt_diff < 50) and (pos_diff < 200): 
                        # Two aircraft have just crashed, looks like it's game over!
                        # (Completely arbitrary values in the conditional above)
                        return True, a, b           
                    
                    if pos_diff < self.hsep:
                        # Houston, we have a separation violation
                        a.flag = b.flag = True
                        continue
                                                
                if a.flag or b.flag:
                    # Remove separation violation flags if the planes are now where they should be
                    a.flag = b.flag = False
                    
        return False, None, None
                                            