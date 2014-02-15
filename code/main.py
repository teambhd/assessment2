import random
import math

from browser import timer, doc

from airspace import Airspace
from gui import GUI

from options import get_option


# First of all, we define some functions

def separation_logic():
    # This function is called on quite a frequent timer and handles calling the airspace's monitor separation 
    # function and then using the results to decide whether to end the game (and to reflect that in the UI)
    
    crash, plane_one, plane_two = airspace.monitor_separation()
    
    if crash:
        stop_timers()
        gui.game_over_message(plane_one, plane_two)
        doc['pause'].unbind('click') # unbinding the pause button prevents the user restarting the timers    
    
    return None

def spawn_flights():
    # This function is run on quite an infrequent timer, and will create new flights if they are needed
    
    max_flights = get_option('max_flights')
    num_flights = len(airspace.flights)
    
    if num_flights == max_flights:
        # We already have enough flights, so we'll stop here
        return None
        
    to_spawn = random.randint(1, max_flights - num_flights)
    
    entry_points = list(airspace.edge_waypoints.values())
    
    # Spawn a number of flights, making sure we don't create too many, 
    # and we don't create more than one flight at a given entry point
    for i in range(0, min(to_spawn, len(entry_points))):
        entry_point = random.choice(entry_points)
        entry_points.remove(entry_point)
        airspace.new_flight(entry_point)
    
    return None
            
def start_timers():
    global timers
    
    airspace.timestep = 50 # ms
    
    timers.append(timer.set_interval(airspace.update_airspace, airspace.timestep))
    timers.append(timer.set_interval(separation_logic, airspace.timestep * 2))
    timers.append(timer.set_interval(gui.update_interface, airspace.timestep))
    timers.append(timer.set_interval(spawn_flights, 5000))
    timers.append(timer.set_interval(gui.draw_timer, 1000))
    
def stop_timers():
    global timers
    for t in timers:
        timer.clear_interval(t)
    timers[:] = [] # Empty the timers list in place
    
def pause_button_clicked(event):
    if doc['pause'].text == 'Pause':
        stop_timers()
        doc['pause'].text = 'Resume'
    else:
        start_timers()
        doc['pause'].text = 'Pause'
    return False
    
doc['pause'].bind('click', pause_button_clicked)


# Now we initialise the game

# Now we create our airspace
hsep, vsep = get_option('horizontal_separation_distance'), get_option('vertical_separation_distance')
airspace = Airspace(40000, 30000, 13000, hsep, vsep) # these values are in m

# and initialise the GUI
gui = GUI(airspace, get_option('debug_mode'))
    
    
# Add a waypoint at a random location on each of the four edges
airspace.add_edge_waypoint('North', random.randint(5000, airspace.x-5000), airspace.y)
airspace.add_edge_waypoint('East', airspace.x, random.randint(5000, airspace.y-5000))
airspace.add_edge_waypoint('South', random.randint(5000, airspace.x-5000), 0)
airspace.add_edge_waypoint('West', 0, random.randint(5000, airspace.y-5000))

# Generate the specified number of random waypoints
for n in range(0, get_option('number_of_waypoints')):
    airspace.new_simple_waypoint()
        
# Draw those waypoints to the screen
gui.draw_waypoints()


# Activate the timers
timers = []
start_timers()