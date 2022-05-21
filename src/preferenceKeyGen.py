from random import randint

def preference_key_gen(preference_1, preference_2, preference_3):
    pref_key = ((preference_1 * preference_2 * preference_3) % 5) + 1
    
    # Movie list does not have 5 as a preference key
    if(pref_key == 5): pref_key -= 1

    return pref_key