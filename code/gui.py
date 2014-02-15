from browser import doc, html, prompt

class GUI:

    def __init__(self, airspace, debug):
        self.airspace = airspace
        self.active_flight = None
        
        # Are we in debug mode? 
        # Debug mode causes more information, some of which will hopefully be useful to testers, to be displayed.
        self.debug = debug
        
        # Bind event handlers for the control buttons
        doc['turn-left'].bind('click', self.turn_left_clicked)
        doc['set-heading'].bind('click', self.set_heading_clicked)
        doc['turn-right'].bind('click', self.turn_right_clicked)
        
        doc['descend'].bind('click', self.descend_clicked)
        doc['set-altitude'].bind('click', self.set_altitude_clicked)
        doc['climb'].bind('click', self.climb_clicked)
        
    # The leading _ indicates a private function    
    def _pixels_to_percentage(self, number, axis):
        if axis == 'x':
            return str((number/self.airspace.x)*100)+'%'
        if axis == 'y':
            return str((number/self.airspace.y)*100)+'%'
    
    def draw_waypoints(self):
        # Draw all current waypoints to the screen, and delete the elements representing deleted waypoints.
        # At present, the waypoints are generated and drawn only once - but there is no (technical) reason 
        # why they can't be altered dynamically.
                    
        parent = doc['waypoints']
        
        children = parent.children
        children_ids = []
        
        # Remove any deleted waypoints from the airspace
        for c in children:
            if c.Id not in self.airspace.waypoints:
                del c
            else:
                children_ids.append(c.Id)
                
        for w in self.airspace.waypoints.values():                            
            style = {
                'left': self._pixels_to_percentage(w.x, 'x'), 
                'bottom': self._pixels_to_percentage(w.y, 'y')
            }
            
            # If the waypoint already exists
            if w.name in children_ids:
                div = doc[w.name]
            
            # If the waypoint doesn't already exist    
            else:
                div = html.DIV(w.name, Id=w.name, Class='waypoint '+w.w_type)
                if self.debug:
                    div.text += ' ('+ str(w.x) + ', ' + str(w.y) + ')'                
                parent <= div
            
            div.style = style
                                        
        return None
        
    def draw_flights(self):
        # Draw all current flights to the screen, and delete the elements representing deleted flights,
        # also handles the case when the current active_flight no longer exists. This will ended being called
        # on a very frequent timer,
        
        flights = self.airspace.flights
        
        parent = doc['flights']
        
        children = parent.children
        children_ids = []
            
        # Remove any deleted flights from the airspace
        for c in children:
            if c.Id not in flights:
                if (self.active_flight != None) and (self.active_flight.code not in flights):
                    self.active_flight = None
                    doc['current-flight'].style = {'display' : 'none'}
                    doc['current-flight-placeholder'].style = {'display' : 'block'}
                del c
            else:
                children_ids.append(c.Id)
                    
        for f in flights:
            code = f
            heading = flights[f].bearing
                            
            style = {
                'left': self._pixels_to_percentage(flights[f].x, 'x'),
                'bottom': self._pixels_to_percentage(flights[f].y, 'y'),
                '-webkit-transform': 'rotate(' + str(heading) + 'deg)',
                   '-moz-transform': 'rotate(' + str(heading) + 'deg)',
                	'-ms-transform': 'rotate(' + str(heading) + 'deg)',
                	 '-o-transform': 'rotate(' + str(heading) + 'deg)',
                	    'transform': 'rotate(' + str(heading) + 'deg)'
            }
            
            # If the flight already exists
            if code in children_ids:
                div = doc[code]
                alt = doc[code + '-altitude']
            
            # If the flight doesn't already exist    
            else:
                div = html.DIV(Id=code, Class='flight')                
                alt = html.DIV(Id=code+'-altitude')
                div.bind('click', self.select_flight)
                div <= alt
                parent <= div
            
            div.style = style
            alt_text = str(round(flights[f].altitude)) + 'm'
            
            if self.debug:
                alt_text += ' ('+ str(round(flights[f].x)) + ', ' + str(round(flights[f].y)) + ')'                
            
            if alt.text != alt_text:
                alt.text = alt_text
                
            class_str = div.Class
                
            if flights[f].flag and (not 'flagged' in class_str):
                div.Class += ' flagged'
            
            elif (not flights[f].flag) and ('flagged' in class_str):
                div.Class = class_str.replace('flagged', '')
                                        
        return None
    
    def select_flight(self, event):
        # Called when a flight is clicked on by the user. Displays information about that flight in the controls
        # area and draws an orange border around the flight icon within the airspace.
        
        if self.active_flight != None:
            # De-select the previous active flight
            class_str = doc[self.active_flight.code].Class
            doc[self.active_flight.code].Class = class_str.replace('active', '')
            
        else:
            # We are the first flight to be selected, so hide the placeholder text and display the info template
            doc['current-flight-placeholder'].style = {'display' : 'none'}
            doc['current-flight'].style = {'display' : 'block'}
        
        # Select the new flight    
        self.active_flight = self.airspace.flights[event.target.Id]
        event.target.Class += ' active' # This class causes the orange background to be drawn
        
        # Update information in controls window
        doc['flight-code'].text = self.active_flight.code
        doc['aircraft-type'].text = self.active_flight.name
        doc['aircraft-size'].text = self.active_flight.size
        
        w_ul = doc['flight-plan']
        
        # Delete the previous flight's displayed waypoints
        for c in w_ul.children:
            del c
        
        # Add elements for the new flight's waypoints
        for w in self.active_flight.waypoints:
            w_ul <= html.LI(w.name, Class="flight-plan-item") 
        
        # This function displays non-static information (e.g. fuel, altitude etc. relating to the new flight)
        self.update_controls()
        
        return None
        
    def update_controls(self):
        
        # If the current flight has been terminated, there's no sense going any further
        if self.active_flight == None:
            return None
        
        altitude = str(round(self.active_flight.altitude))
        speed = str(round(self.active_flight.speed))
        heading = str(round(self.active_flight.bearing))
        
        target_altitude = str(round(self.active_flight.target_altitude))
        target_speed = str(round(self.active_flight.target_speed))
        target_heading = str(round(self.active_flight.target_bearing))
                        
        # Display actual altitude, speed, bearing and their targets (if different)
        for actual, target, element, target_element in zip([altitude, speed, heading], [target_altitude, target_speed, target_heading], ['flight-altitude', 'flight-speed', 'flight-heading'], ['target-altitude', 'target-speed', 'target-heading']):
            # Set the actual value
            if doc[element].text != actual:
                doc[element].text = actual
            
            if actual != target:
                doc[target_element+'-parent'].style = {'display' : 'table-cell'}
                if doc[target_element].text != target:
                    doc[target_element].text = target
            else:
                doc[target_element+'-parent'].style = {'display' : 'none'}
        
        current_fuel = self.active_flight.fuel
        max_fuel = self.active_flight.limitations['max_fuel']
        doc['fuel-counter'].style = {'width' : str((current_fuel/max_fuel)*100)+'%'}
        doc['current-fuel'].text = str(round(current_fuel))
        doc['max-fuel'].text = str(max_fuel)
        
        # Update the active waypoint marker
        for li in doc['flight-plan'].children:
            class_str = li.Class
            if li.text == self.active_flight.next_waypoint.name:
                if not 'active' in class_str:
                    li.Class += ' active'
            elif 'active' in class_str:
                li.Class = class_str.replace('active', '')
        
        return None
        
    def update_interface(self):
        # This function is called on a timer by the main loop of the program
        self.draw_flights()
        self.update_controls()
        
    def draw_timer(self):
        # This function should be called every second by the main loop. It updates the main game timer accordingly.
        s = int(doc['seconds'].text)
        
        if s != 59:
            s = str(s + 1)
            # The zfill function is probably more appropriate here (and below), but seems broken in Brython
            if len(s) == 1:
                s = "0" + s 
            doc['seconds'].text = s
       
        else:
            doc['seconds'].text = '00'
            m = int(doc['minutes'].text)
            m = str(m + 1)
            if len(m) == 1: 
                m = "0" + m
            doc['minutes'].text = m
            
    def game_over_message(self, plane_one, plane_two=None):
        message = doc['game-over-message']
        
        if plane_two != None:
            # If two planes were involved in the crash event, then they must have collided
            message.text = "Flights " + plane_one.code + " and " + plane_two.code + " have collided."
        
        else:
            # Otherwise, a single plane must have run out of fuel
            message.text = "Flight " + plane_one.code + " has run out of fuel and crashed."
        
        doc['game-over-box'].style = {'display' : 'block'}
        return None
            
    def turn_left_clicked(self, event):
        current_target = self.active_flight.target_bearing
        if current_target >= 15:
            self.active_flight.target_bearing = current_target - 15
        else:
            self.active_flight.target_bearing = 345 + current_target
        return None        
        
    def turn_right_clicked(self, event):
        current_target = self.active_flight.target_bearing
        if current_target < 345:
            self.active_flight.target_bearing = current_target + 15
        else:
            self.active_flight.target_bearing = 15 - (360 - current_target)    
        return None
    
    def descend_clicked(self, event):
        self.active_flight.target_altitude = max(self.active_flight.target_altitude - 500, 100)
        return None
        
    def climb_clicked(self, event):
        current_target = self.active_flight.target_altitude
        max_altitude = self.active_flight.limitations['max_altitude']
        self.active_flight.target_altitude = min(current_target + 500, max_altitude)
        return None
        
    def set_heading_clicked(self, event):
        target = self.active_flight.target_bearing
        
        heading = prompt("Enter a heading in degrees (e.g. 45 or 270)", target)
        while not ((heading.isdigit()) and (0 <= int(heading) < 360)):
            if heading == '': # If the cancel button was clicked, then we exit
                return None
            heading = prompt("Invalid Entry.\nEnter a heading in degrees (e.g. 45 or 270)", target)
            
        self.active_flight.target_bearing = int(heading)
        return None
        
    def set_altitude_clicked(self, event):
        target = self.active_flight.target_altitude
        max_altitude = self.active_flight.limitations['max_altitude']
        
        altitude = prompt("Enter a target altitude in m (e.g. 5000 or 400)", target)
        while not ((altitude.isdigit()) and (100 <= int(altitude) <= max_altitude)):
            if altitude == '': # If the cancel button was clicked, then we exit
                return None
            altitude = prompt("Invalid Entry.\nEnter a target altitude in m (e.g. 5000 or 400)", target)
            
        self.active_flight.target_altitude = int(altitude)
        return None
        