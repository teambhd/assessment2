class Waypoint:
    # The static waypoints that populate our airspace.

    def __init__(self, name, x, y, w_type):
        self.name = name # e.g. 'Alpha' or 'North'
        
        # The waypoint's location within the airspace
        self.x = x
        self.y = y
        
        self.w_type = w_type # 'simple', 'edge' or 'airport'
        
    def __repr__(self):
        return "Waypoint at location "+str(self.x)+":"+str(self.y)+". Of type: "+str(self.w_type)+". Named: "+str(self.name)
        
        
# The Nato phonetic alphabet, as used in ATC worldwide and used here for waypoint names
phonetic_alphabet = [
    'Alpha',    'Bravo',    'Charlie',  'Delta',
    'Echo',     'Foxtrot',  'Golf',     'Hotel',
    'India',    'Juliet',   'Kilo',     'Lima', 
    'Mike',     'November', 'Oscar',    'Papa',
    'Quebec',   'Romeo',    'Sierra',   'Tango',
    'Uniform',  'Victor',   'Whisky',   'Xray',
    'Yankee',   'Zulu' 
]
        