current_score = 0

def add_points(value):
    global current_score
    current_score += value
    return None
    
def deduct_points(value):
    global current_score
    current_score -= value
    return None

def reset_score():
    global current_score
    current_score = 0