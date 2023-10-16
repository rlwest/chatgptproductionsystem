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

# Buffers
buffer_chunk = {'planning_unit': 'ham&cheese', 'unit_task': 'bread_bottom'}

# Productions
production1 = {'match': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_bottom'}, 'negative': {}, 'utility': 1,
               'update': {'unit_task': 'cheese'},
               'report': 'Production 1 fired: Changed unit_task to cheese'}
production2 = {'match': {'planning_unit': 'ham&cheese', 'unit_task': 'cheese'}, 'negative': {}, 'utility': 3,
               'update': {'unit_task': 'ham'},
               'report': 'Production 2 fired: Changed unit_task to ham'}
production3 = {'match': {'planning_unit': 'ham&cheese', 'unit_task': 'ham'}, 'negative': {}, 'utility': 5,
               'update': {'unit_task': 'bread_top'},
               'report': 'Production 3 fired: Changed unit_task to bread_top'}
production4 = {'match': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_top'}, 'negative': {}, 'utility': 2,
               'update': {'unit_task': 'stop'},
               'report': 'Production 4 fired: Changed unit_task to stop'}

productions = [production1, production2, production3, production4]

# Run continuously while there are matching productions
while True:
    production_matched = False
    match_list = []
    
    for production in productions:
        if buffer_match_eval(buffer_chunk, production['match'], production['negative']):
            print("The production is matching.")
            match_list.append(production)
            production_matched = True
            print(production['report'])  # Print the report statement
    
    if production_matched:
        # If a production matched, update buffer contents based on the highest utility matching production
        max_match = find_max(match_list)
        update_info = max_match.get('update', {})
        buffer_chunk.update(update_info)
        print("Updated buffer chunk:", buffer_chunk)
    else:
        print("No matching production found.")
        break  # Break the loop if no matching production is found
