import math

aircraft_specs = {
    'small'  : {'max_speed' : 120, 'climb_speed' : 25, 'max_fuel' :  3000, 'kmpl' : 0.04, 'max_altitude' :  5400},
    'medium' : {'max_speed' : 200, 'climb_speed' : 45, 'max_fuel' : 16000, 'kmpl' : 0.02, 'max_altitude' : 12500},
    'jumbo'  : {'max_speed' : 250, 'climb_speed' : 35, 'max_fuel' : 32000, 'kmpl' : 0.01, 'max_altitude' : 12500}
}

aircraft_names = {
    'small'  : ['Diamond Twin-Car', 'Chessnut Grando'],
    'medium' : ['IL-86', 'Embarasser 195', 'Epic Elite', 'Bomberman CS300', 'Topola 204'],
    'jumbo'  : ['Boring 747', 'AirBuzz A380']
}    
    
        
class Flight:
    
    def __init__ (self, x, y, altitude, speed, waypoints, bearing, fuel, code, name, size, limitations):
        
        # x and y are the position of the flight in m
        self.x = x
        self.y = y
        
        self.altitude = altitude
        self.speed = speed          # The speed of the plane in m/s
        self.bearing = bearing      # The plane's heading in degrees from 0 to 360
        self.fuel = fuel            # The current amount of fuel aboard
        self.code = code            # Flight code e.g. AB123
        self.name = name            # Aircraft name e.g Boeing 737
        self.size = size            # For scoring and typing purposes - jumbo/medium/small
        
        self.waypoints = waypoints  # The flight plan, a list of waypoints to visit in order
        self.next_waypoint = waypoints[1] # [1] is the first simple waypoint, as [0] is the entry point
        
        self.limitations = limitations # A list of limitations for the flight
        
        # These attributes are needed in the class, but not on the creation of a flight
        self.target_speed    = speed 
        self.target_altitude = altitude 
        self.target_bearing  = bearing
        
        self.flag = False           # Has this aircraft broken separation rules (here so the GUI can draw it easily)
                
        # Some basic sanity checks on initial values
        assert self.speed           <= self.limitations['max_speed']
        assert self.altitude        <= self.limitations['max_altitude']
        assert self.fuel            <= self.limitations['max_fuel']
        
    def __repr__ (self):
        return  "Flight " + str(self.code) + " has the following properties: \n" +
        "    Location: (" + str(self.x) + "," + str (self.y) + ") \n" + 
        "    Altitude: " + str (self.altitude)+ "m \n" + 
        "    Speed: " + str(self.speed) + "m/s \n" + 
        "    Flight plan: " + str(self.waypoints) + "\n" + 
        "    Bearing: " + str(self.bearing) + " degrees \n" +
        "    Current Fuel: " + str(self.fuel) + "l \n" +
        "    Size: " + str(self.size) + "\n" + 
        "    Aircraft Name: " + str(self.name) + "\n" +
        "    Limitations: " + str(self.limitations) +"\n" + 
        "    Target Speed: " + str(self.target_speed) + "m/s \n" +
        "    Target Altitude: " + str(self.target_altitude) + "m \n" +
        "    Target Heading: " + str(self.target_bearing) + "degrees \n"    
                                                            
    def update_bearing (self, step):                
        if self.bearing != self.target_bearing:
                        
            # Normalise change to not rotate a lot for a 1 degree change (i.e., change from 0 to 359 degrees)
            change = self.target_bearing - self.bearing 
            
            if change > 180:
                change -= 360 
            
            elif change < -180:
                change += 360
             
            if change > 0: # If bearing at a more acute angle
                self.bearing = round(self.bearing + (self.speed * step *0.01 * 2), 2)
            if change < 0: # If bearing at a greater angle
                self.bearing = round(self.bearing - (self.speed* step * 0.01 * 2), 2)
                
            # Prevent the bearing from oscillating when approaching its target   
            if round(self.bearing) == self.target_bearing:
                 self.bearing = self.target_bearing
            
            # Ensure that bearings always remain in the range 0 to 359     
            if self.bearing < 0:
                self.bearing += 360
                                
            elif self.bearing >= 360:
                self.bearing -= 360
                        
        return None
                        
    def update_altitude (self, step): 
        if self.altitude != self.target_altitude:
            
            # Prevent the altitude from oscillating when approaching its target
            if abs(self.altitude - self.target_altitude) <= 5:
                self.altitude = self.target_altitude
                            
            else: 
                climb_speed = self.limitations['climb_speed']
            
                if self.altitude < self.target_altitude: 
                    self.altitude = round(self.altitude + (climb_speed * step))
            
                else: 
                    self.altitude = round(self.altitude - (climb_speed * step)) 
        
        return None
                    
    def update_speed(self, step):
        # To be implemented as part of Assessment 3
        pass
                                        
    def move(self, step):
        # Update the position, and indirectly the bearing, altitude and speed of a flight
        
        # We are passed the timestep in milliseconds, need to convert it to seconds
        step *= 0.001
        
        # Update values of bearing, altitude and speed towards their targets
        self.update_bearing(step)
        self.update_altitude(step)
        self.update_speed(step)
        
        # Update fuel based on the distance travelled (in m) and the plane's consumption
        self.fuel -= (self.speed * step) / (1000 * self.limitations['kmpl'])
                                
        # Work out the plane's new position on the x and y axes
        self.x = self.x + step * self.speed * math.sin(math.radians(self.bearing))
        self.y = self.y + step * self.speed * math.cos(math.radians(self.bearing))
        
        return None 
        
    def land(self):
        # To be implemented as part of Assessment 3
        pass
        
    def take_off(self):
        # To be implemented as part of Assessment 3
        pass