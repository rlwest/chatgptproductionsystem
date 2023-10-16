import random

def buffer_match_eval(buffer_dict, matching_dict, negation_dict, wildcard='*'):
    """
    Compares two dictionaries, matching_dict and negation_dict, with buffer_dict
    Returns True if
        all matching_dict contents are in buffer_dict ...
        AND none of the negation_dict contents are in buffer_dict
    Returns False if not
    Uses * as a wild card for matching_dict key values
    """
    for key in matching_dict.keys():
        if key not in buffer_dict:
            return False
        if matching_dict[key] != buffer_dict[key] and matching_dict[key] != wildcard:
            return False
    for key in negation_dict.keys():
        if key in buffer_dict and negation_dict[key] == buffer_dict[key]:
            return False
    return True

def find_max(match_list):
    highest_utility = float('-inf')
    highest_utility_production = None

    for item in match_list:
        utility = item.get('utility', float('-inf'))

        if utility > highest_utility:
            highest_utility = utility
            highest_utility_production = item

    return highest_utility_production

def production_eval(productions, buffer_chunk):
    match_list = []
    for production in productions:
        if buffer_match_eval(buffer_chunk, production['match'], production['negative']):
            print("The production is matching.")
            match_list.append(production)
        else:
            print("The production is different.")
    max_match = find_max(match_list)
    print("Maximum match value:", max_match)

    if max_match:
        # Update buffer contents based on the highest utility matching production
        update_info = max_match.get('update', {})
        buffer_chunk.update(update_info)

# Buffers
buffer_chunk = {'planning_unit': 'ham&cheese', 'unit_task': 'bread_bottom'}

# Productions
production1 = {'match': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_bottom'}, 'negative': {}, 'utility': 1,
               'update': {'unit_task': 'cheese', 'newkey': 7}}
production2 = {'match': {'planning_unit': 'ham&cheese', 'unit_task': 'cheese'}, 'negative': {}, 'utility': 3,
               'update': {'new_key': 'new_value2'}}
production3 = {'match': {'planning_unit': 'ham&cheese', 'unit_task': 'ham'}, 'negative': {}, 'utility': 5,
               'update': {'unit_task': 'new_task3'}}
production4 = {'match': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_top'}, 'negative': {}, 'utility': 2,
               'update': {'new_key2': 'new_value4'}}

productions = [production1, production2, production3, production4]

# Run
production_eval(productions, buffer_chunk)
print("Updated buffer chunk:", buffer_chunk)  # Print the updated buffer contents
