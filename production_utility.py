import random
#match_list = []


def buffer_match_eval(buffer_dict, matching_dict, negation_dict, wildcard='*'):
    """
    Compares two dictionaries, matching_dict and negation_dict, with buffer_dict
    Returns True if
        all matching_dict contents are in buffer_dict ...
        AND none of the negation_dict contents are in buffer_dict
    Returns False if not
    Uses * as a wild card for matching_dict key values
    """
    for key in matching_dict.keys():  # Iterate over the keys of the matching_dict
        if key not in buffer_dict:  # check if the key in the matching_dict is NOT in the buffer_dict
            return False # if not then the match is false
        if matching_dict[key] != buffer_dict[key] and matching_dict[key] != wildcard: # check the key value
            return False # if the key value is NOT the same AND the key value is NOT * then match is false
    for key in negation_dict.keys():  # Iterate over the keys of the negation_dict
        if key in buffer_dict and negation_dict[key] == buffer_dict[key]:
            return False # if a negation key is in the buffer_dict AND the key value is the same then fail
    return True




def find_max(match_list):
    highest_utility = float('-inf')  # Initialize to negative infinity to handle any negative number
    highest_utility_productions = []  # Initialize an empty list for productions with the highest utility

    for item in match_list:
        utility = item.get('utility', float('-inf'))  # Get the 'utility' value, defaulting to negative infinity if not present

        if utility > highest_utility:
            highest_utility = utility
            highest_utility_productions = [item]
        elif utility == highest_utility:
            highest_utility_productions.append(item)

    # If there are matching productions choose one randomly from the list (if there is only one in the list it will be chosen)
    if highest_utility_productions:
        return [random.choice(highest_utility_productions)]
    else:
        return ['no_match']  # if no production matches return 'no_match'




def production_eval(productions, buffer_chunk):
    match_list = []
    for production in productions:  # Iterate over the productions list
        print(production)
        print(production['match'])
        print(production['negative'])
        if buffer_match_eval(buffer_chunk, production['match'], production['negative']):
            print("The production is matching.")
            match_list.append(production)
        else:
            print("The production is different.")
    max_match = find_max(match_list)
    print("Maximum match value:", max_match)
    return max_match

        
        



## buffers
buffer_chunk = {'a': 1, 'b': 2, 'c': 3, 'd': 5, 'e': 6}

## productions
production1 = {'match':{'a': 2, 'b': '*', 'd': 5}, 'negative':{'e': 1}, 'utility':3}
production2 = {'match':{'a': 5, 'b': '*', 'd': 1}, 'negative':{'e': 3}, 'utility':1}
production3 = {'match':{'a': 2, 'b': '*'}, 'negative':{'e': 3}, 'utility':5}

productions = [production1, production2, production3]

## run
production_eval(productions, buffer_chunk)





