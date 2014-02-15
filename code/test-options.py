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

from browser.local_storage import storage # used to backup and restore options before and after the tests
from options import *


# We need to start with a clean slate!
if 'options_backup' in storage:
    storage['options_backup'] = storage['options']
clear_options()

print("== test-options.py ==")


# ================
# THE ACTUAL TESTS
# ================

print("\nReading back default option max_flights of type int")

if get_option('max_flights') == 2:
    print("PASS: Value read back successfully (max_flights was equal to 2)")

else:
    print("FAIL: Value not read back")
    print("      Return value was: " + str(get_option('max_flights')))
    
    
print("\nReading back default option debug_mode of type bool")

if get_option('debug_mode') == False:
    print("PASS: Value read back successfully (debug_mode was equal to False)")

else:
    print("FAIL: Value not read back")
    print("      Return value was: " + str(get_option('debug_mode')))

    
print ("\nSetting max_flights to 5 and debug_mode to True, to test over-riding of default options")

set_option('max_flights', 5)
set_option('debug_mode', True)

if (get_option('max_flights') == 5) and (get_option('debug_mode') == True):
    print("PASS: Values read back successfully")
    
else:
    print("FAIL: Values not read back")
    print("      Return values were: " + str(get_option('max_flights')) + " and " str(get_option('debug_mode')))
    

print ("\nCalling load_options() a couple of times, to ensure that state was being saved properly, then repeating the above test")

load_options()
load_options()

if (get_option('max_flights') == 5) and (get_option('debug_mode') == True):
    print("PASS: Values read back successfully")
    
else:
    print("FAIL: Values not read back")
    print("      Return values were: " + str(get_option('max_flights')) + " and " str(get_option('debug_mode')))


print("\nSetting and reading back a new option (test_option = 42), to check storage of options without defaults")

set_option('test_option', 42)

if get_option('test_option') == 42:
    print("PASS: Value read back successfully (test_option was equal to 42)")

else:
    print("FAIL: Value not read back")
    print("      Return value was: " + str(get_option('test_option')))


print("\nAttempting to access a non-existent option, to ensure None is returned")

if get_option('asdasdasd') == None:
    print("PASS: Value read back successfully (asdasdasd was equal to None)")

else:
    print("FAIL: Value not read back")
    print("      Return value was: " + str(get_option('asdasdasd')))


print("\nAttempting to reset two single options (max_flights and test_option) to ensure the appropriate values are returned, the default if there is one, otherwise None")

reset_option('max_flights')
reset_option('test_option')

if (get_option('max_flights') == 2) and (get_option('test_option') == None):
    print("PASS: Both values read back successfully")

else:
    print("FAIL: Values not read back")
    print("      Return values were: " + str(get_option('max_flights')) + " and " str(get_option('test_option')))


print("\nClearing all options, and testing to see if values are back to their defaults")

clear_options()

if (get_option('max_flights') == 2) and (get_option('debug_mode') == False):
    print("PASS: Values appear to have been reset successfully")
    
else:
    print("FAIL: Values not read back")
    print("      Return values were: " + str(get_option('max_flights')) + " and " str(get_option('debug_mode')))

    
# =======
# CLEANUP
# =======
    
# Restore saved options from our backup
if 'options_backup' in storage:
    storage['options'] = storage['options_backup']
    del storage['options_backup']
