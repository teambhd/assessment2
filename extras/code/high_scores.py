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

def load_scores():
    # Load scores from local storage, decoding from json
    
    # If there's something in local storage, return it
    if 'high_scores' in storage:
        l = json.loads(storage['high_scores'])
        assert type(l) == list
        return l
    
    # If nothing is found in local storage, return an empty list
    return []
    
def save_scores():
    # Serialise, then save to local storage
    
    # There's no point in saving an empty list (empty lists are false in python)
    if scores_list:
        storage['high_scores'] = json.dumps(scores_list)
        return None
    
    # If there was nothing in scores_list but something in local storage, we erase local storage
    if 'high_scores' in storage:
        del storage['high_scores']
        return None
        
    # If we reach this, then both storage locations are empty, so just return
    return None
    
def clear_scores():
    # Clear scores from both the scores list... 
    global scores_list
    scores_list = []
    
    # ... and local storage
    save_scores()
    
    return None
    
def get_scores():
    # Fetch scores from scores_list and sort in descending order
    return sorted(scores_list, reverse=True)
    
def get_top_score():
    # Return the current highest score
    return get_scores()[0]

def add_score(score):
    # Sanity check, then add score to scores_list
    assert type(score) == int
    assert score > 0
        
    scores_list.append(score)
    save_scores()
    
    return None
    
    
# Now we retrieve the stored values from local storage and load them back
# into the array for the rest of this module to use. This code should only
# get run on import.

scores_list = load_scores()