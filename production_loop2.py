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
    """
    This loop continuously checks the buffer_chunk against a list of production rules (productions).
    If a production rule matches the buffer_chunk, it updates the buffer based on the highest utility matching production.

    The loop continues indefinitely (until explicitly broken) to handle continuous matching and updating.
    
    The loop breaks if no matching production is found, indicating the end of the processing.

    Variables:
    - buffer_chunk (dict): The current state of the buffer.
    - productions (list): A list of production rules to match against the buffer_chunk.
    """
    production_matched = False  # Flag to track if a production has been matched in this iteration
    
    match_list = []  # List to store productions that match the buffer_chunk
    
    for production in productions:  # Iterate through each production rule
        # Check if the buffer_chunk matches the production's match conditions
        if buffer_match_eval(buffer_chunk, production['match'], production['negative']):
            #print("The production is matching.")
            match_list.append(production)  # Add matching production to the list
            production_matched = True  # Set the flag to True since a match was found
            #print(production['report'])  # Print the report statement
    
    if production_matched:  # If a production was matched
        # If a production matched, update buffer contents based on the highest utility matching production
        max_match = find_max(match_list)  # Find the production with the highest utility
        update_info = max_match.get('update', {})  # Get the update information
        report_info = max_match.get('report') # Get the report
        buffer_chunk.update(update_info)  # Update the buffer_chunk with the highest utility production's changes
        print(report_info)  # Print the report statement
        print("Updated buffer chunk:", buffer_chunk) # Print updated buffer content
    else:
        print("No matching production found.")
        break  # Break the loop if no matching production is found




