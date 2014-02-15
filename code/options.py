# We don't actually need this to be a class, Python modules 
# (which this automatically is by virtue of being in a separate 
# file) already separate out things into their own namespace etc.
# -TW


from browser.local_storage import storage
# The storage dictionary is actually a front-end for html5 local storage
# which can be then read back by any page on the same domain. The 
# underlying support is only for *strings* however and it seems that any 
# other type of data is likely to get mangled, so remember to encode it.

import json

# First we define the module's functions

def load_options():
    # Loads options from local storage, deserialising etc.
    
    # If there's something in local storage, return it
    if 'options' in storage:
        d = json.loads(storage['options'])
        if type(d) == dict:
            return d
            
    # If nothing is found in local storage, return an empty dictionary
    return {}
    
def save_options():
    # Serialise, then save to local storage
    
    # There's no point in saving an empty dictionary (empty dictionaries are false in python)
    if options_dictionary:
        storage['options'] = json.dumps(options_dictionary)
        return None
    
    # If there was nothing in scores_list but something in local storage, we erase local storage
    if 'options' in storage:
        del storage['options']
        return None
        
    # If we reach this, then both storage locations are empty, so just return
    return None
        
def clear_options():
    # Effectively restores default settings
    
    global options_dictionary
    options_dictionary = {}
    
    save_options()
    
    return None
    
def get_option(key):
    # Returns a setting's value, either from local storage, or a sensible default.
    
    if key in options_dictionary:
        return options_dictionary[key]
        
    if key in default_options:
        return default_options[key]
        
    return None
    
def set_option(key, value):
    # Sets a key to a value
    assert type(key) == str   
    
    options_dictionary[key] = value
    save_options()
    
    return None
        
def reset_option(key):
    # Clears a single option
    del options_dictionary[key]
    save_options()
    
    return None


# Then we set some sensible defaults for each option

default_options = { 
    'max_flights' : 2,
    'number_of_waypoints' : 15,
    'horizontal_separation_distance' : 9000,
    'vertical_separation_distance' : 300,
    'debug_mode' : False
    # and so on
}


# Now we retrieve the stored values from local storage and load them back
# into the dictionary for the rest of this module to use. This code should only
# get run on import.

options_dictionary = load_options()