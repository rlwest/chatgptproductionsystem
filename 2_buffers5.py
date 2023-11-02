import random

def buffer_match_eval(buffer_dict, matching_dict, negation_dict, negation_key, wildcard='*'):
    for key in matching_dict.keys():
        if key not in buffer_dict:
            return False
        if matching_dict[key] != buffer_dict[key] and matching_dict[key] != wildcard:
            return False
    # Now, the negation is specific to the buffer using the negation_key
    for key in negation_dict.get(negation_key, {}).keys():
        if key in buffer_dict and negation_dict[negation_key][key] == buffer_dict[key]:
            return False
    return True
    # Note that the negation must specify a slot plus content, it cannot use the wildcard
    # This is consistent with ACT-R theory about not matching on slot names
    # matching on positive slot names is assumedly supposed to be for retrieving the information
    # this is a grey area

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
buffer_chunk1 = {'planning_unit': 'ham&cheese', 'unit_task': 'bread_bottom'}
buffer_chunk2 = {'counting': 'one'}

# Productions with specific matching and updating conditions for each buffer
production1 = {
    'match1': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_bottom'},
    'match2': {'counting': 'one'},
    'negative1': {},  # Buffer-specific negation for buffer_chunk1
    'negative2': {},  # Buffer-specific negation for buffer_chunk2
    'utility': 1,
    'update1': {'unit_task': 'cheese'},  # Specific update for buffer_chunk1
    'update2': {'counting': 'two'},  # Specific update for buffer_chunk2
    'report': 'Production 1 fired: Changed unit_task to cheese in buffer1 and tomato in buffer2'
}

production2 = {
    'match1': {'planning_unit': '*', 'unit_task': 'cheese'},
    'match2': {'counting': 'two'},
    'negative1': {},  # Buffer-specific negation for buffer_chunk1
    'negative2': {},  # Buffer-specific negation for buffer_chunk2
    'utility': 2,
    'update1': {'unit_task': 'ham'},  
    'update2': {'counting': 'three'},  
    'report': 'Production 2 fired'
}

production3 = {
    'match1': {'planning_unit': 'ham&cheese', 'unit_task': 'ham'},
    'match2': {'counting': 'three'},
    'negative1': {'unit_task': 'cat'},  # Buffer-specific negation for buffer_chunk1
    'negative2': {'counting': 'nine'},  # Buffer-specific negation for buffer_chunk2
    'utility': 3,
    'update1': {'unit_task': 'bread_top'},  
    'update2': {'counting': 'four'},  
    'report': 'Production 3 fired'
}

production4 = {
    'match1': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_top'},
    'match2': {'counting': 'four'},
    'negative1': {},  # Buffer-specific negation for buffer_chunk1
    'negative2': {},  # Buffer-specific negation for buffer_chunk2
    'utility': 4,
    'update1': {'unit_task': 'stop'},  
    'update2': {'counting': 'stop'},  
    'report': 'Production 4 fired'
}

productions = [production1, production2, production3, production4]


# Main execution loop
while True:
    production_matched = False
    match_list = []

    # Check each production's specific conditions against both buffers
    for production in productions:
        # Check if production matches specific conditions for both buffers with buffer-specific negations
        if buffer_match_eval(buffer_chunk1, production['match1'], production, 'negative1') and \
           buffer_match_eval(buffer_chunk2, production['match2'], production, 'negative2'):
            match_list.append(production)
            production_matched = True
    
    if production_matched:
        max_match = find_max(match_list)
        report_info = max_match.get('report')

        # Apply specific updates for buffer_chunk1 if present, otherwise apply general update
        buffer_chunk1.update(max_match.get('update1', max_match.get('update', {})))
        
        # Apply specific updates for buffer_chunk2 if present, otherwise apply general update
        buffer_chunk2.update(max_match.get('update2', max_match.get('update', {})))

        print(report_info)  # Immediately print the report statement
        print("Updated buffer chunk1:", buffer_chunk1)
        print("Updated buffer chunk2:", buffer_chunk2)

    else:
        print("No matching production found.")
        break  # No production matched both buffers, end the loop

# The actual execution of the loop will not be run here to avoid an infinite loop.
