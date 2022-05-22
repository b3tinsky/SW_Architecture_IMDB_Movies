from random import randint


# S - Single responsibility: Handles generating the preference key
class PreferenceAlgorithm():
    def keyGenerator(preference_1, preference_2, preference_3):
        pref_key = ((preference_1 * preference_2 * preference_3) % 5) + 1

        # Movie list does not have 5 as a preference key
        if(pref_key == 5):
            pref_key -= 1

        return pref_key