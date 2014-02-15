from browser import doc, html, timer
from options import *

table = doc['options-table']
message = doc['message']


# Write out the table of options
for o in default_options:
    row = html.TR()
    
    row <= html.TD(o.replace('_', ' ')) # the option name, with underscores removed for user-friendliness
    
    input_td = html.TD()
    
    if type(default_options[o]) == bool:
        # Draw a checkbox rather than an input field for True/False options
        input_td <= html.INPUT(checked=get_option(o), type='checkbox', name=o, Id=o)
    
    else:
        input_td <= html.INPUT(value=str(get_option(o)), type='text', name=o, Id=o)
    
    row <= input_td
    table <= row
    
    
def update_displayed_values():
    for o in default_options:
        input_element = doc[o]
        
        if type(default_options[o]) == bool:
            input_element.checked = get_option(o)
            
        else:
            input_element.value = str(get_option(o))
    
    
def save_button_clicked(event):
    for o in default_options:
        default = default_options[o]
        
        if type(default_options[o]) == bool:
            set_option(o, doc[o].checked)
    
        else:
            entered = doc[o].value
            if entered.isdigit() and (type(default_options[o]) == int):
                # If we are looking for an integer, and we get one
                set_option(o, int(entered))
                
            elif type(default_options[o]) == str:
                # entered is already a str, so use it directly if we were looking for one
                set_option(o, entered)
                            
    message.text = 'Changes saved successfully'
    message.Class = 'message success'
    message.style = {'display' : 'block'}
    timer.set_timeout(message_timeout_function, 3000)
    
    update_displayed_values()
   
doc['save-button'].bind('click', save_button_clicked)   
    
    
def reset_button_clicked(event):
    clear_options()
    
    message.text = 'Options reset successfully'
    message.Class = 'message success'
    message.style = {'display' : 'block'}
    timer.set_timeout(message_timeout_function, 3000)
   
    update_displayed_values()
    
doc['reset-button'].bind('click', reset_button_clicked)

def message_timeout_function():
    message.style = {'display' : 'none'}
    message.Class = 'message'   
