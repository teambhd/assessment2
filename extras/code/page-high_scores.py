from browser import html, doc
from high_scores import get_scores, clear_scores


# Display the scores as an ordered list on the page
scores = get_scores()
l = len(scores)

if l == 0:
    p = html.P("No high scores found, get playing and create some!")
    doc['scores'] <= p

else:
    ol = html.OL()

    # Show a maximum of 10 scores
    if l < 10:
        display = l
    else:
        display = 10

    for i in range(0, display):
        ol <= html.LI(str(scores[i]))
    
    doc['scores'] <= ol


# Bind clear scores button
def clear_button_click(event): 
    clear_scores()

doc['clear-scores'].bind('click', clear_button_click)
        
