import sys
from browser import doc
from browser.local_storage import storage # used to backup and restore scores before and after the tests

from high_scores import *


# Redefine the print keyword to append to our textarea
def write(something):
    doc['output'].text += something
    
sys.stdout.write = sys.stderr.write = write

# We need to start with a clean slate!
if 'high_scores' in storage:
    storage['hs_backup'] = storage['high_scores']   
clear_scores()


print("== Test-Highscores.py ==\n")
    
    
print("Adding some high scores, then testing to see if they are returned properly")
print("Scores are 30, 20, 10, 42")

add_score(30)
add_score(20)
add_score(10)
add_score(42)

if get_scores() == [42, 30, 20, 10]:
    print("PASS: Scores returned successfully")
    
else:
    print("FAIL: Scores not returned or returned unsorted")
    print("      Return value was: " + str(get_scores()))
    
    
print("")


print("Adding another score (2013), to see if list can be modified correctly")

add_score(2013)

if get_scores() == [2013, 42, 30, 20, 10]:
    print("PASS: Scores returned successfully")
    
else:
    print("FAIL: Scores not returned or returned unsorted")
    print("      Return value was: " + str(get_scores()))
    
    
print("")
    
        
print("Clearing scores, then adding a single score back")

clear_scores()
add_score(100)

if get_scores() == [100]:
    print("PASS: Scores cleared and re-added successfully")
    
else:
    print("FAIL: Scores not cleared properly")
    print("      Return value was: " + str(get_scores()))
    
    
print("")
   

print("Attempting to save some scores to local storage and then read them back")

clear_scores()

add_score(30)
add_score(20)
add_score(10)
add_score(42)

# Should have been saved automatically

load_scores()

if get_scores() == [42, 30, 20, 10]:
    print("PASS: Scores returned successfully")
    
else:
    print("FAIL: Scores not returned or returned unsorted")
    print("      Return value was: " + str(get_scores()))
    
    
# We need to not pollute the actual game scores
clear_scores()

if 'hs_backup' in storage:
    storage['high_scores'] = storage['hs_backup']
    del storage['hs_backup']
