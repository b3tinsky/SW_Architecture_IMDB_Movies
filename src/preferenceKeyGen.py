from random import randint

# TODO: Change rands to parameters given by user 
def preference_key_gen():
    rand1 = randint(1, 5)
    rand2 = randint(1, 5)
    rand3 = randint(1, 5)
    
    pref_key = ((rand1 * rand2 * rand3) % 5) + 1
    
    # Movie list does not have 5 as a preference key
    if(pref_key == 5): pref_key -= 1

    return pref_key