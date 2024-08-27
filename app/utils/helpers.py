import random

def get_random_position():
    return {
        'left': random.randint(0, 100),
        'top': random.randint(0, 100)
    }
