# Here's the modified code with the action functions implemented for each production.

def buffer_match_eval(buffer_dict, matching_dict, negation_dict, negation_key, wildcard='*'):
    for key in matching_dict.keys():
        if key not in buffer_dict:
            return False
        if matching_dict[key] != buffer_dict[key] and matching_dict[key] != wildcard:
            return False
    for key in negation_dict.get(negation_key, {}).keys():
        if key in buffer_dict and negation_dict[negation_key][key] == buffer_dict[key]:
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
buffer_chunk1 = {'planning_unit': 'ham&cheese', 'unit_task': 'bread_bottom'}
buffer_chunk2 = {'counting': 'one'}


# Productions with buffer updating functions

def action_production1(buffer1, buffer2):
    buffer1['unit_task'] = 'cheese'
    buffer2['counting'] = 'two'
production1 = {
    'match1': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_bottom'},
    'match2': {'counting': 'one'},
    'negative1': {},
    'negative2': {},
    'utility': 1,
    'action': action_production1,
    'report': 'Production 1 fired: Changed unit_task to cheese in buffer1 and counting to two in buffer2'
}

def action_production2(buffer1, buffer2):
    buffer1['unit_task'] = 'ham'
    buffer2['counting'] = 'three'
production2 = {
    'match1': {'planning_unit': '*', 'unit_task': 'cheese'},
    'match2': {'counting': 'two'},
    'negative1': {},
    'negative2': {},
    'utility': 2,
    'action': action_production2,
    'report': 'Production 2 fired: Changed unit_task to ham in buffer1 and counting to three in buffer2'
}
def action_production3(buffer1, buffer2):
    # Take 'unit_task' from buffer1 and put it in 'counting' of buffer2
    buffer2['counting'] = buffer1['unit_task']
    buffer1['unit_task'] = 'bread_top' # And still update buffer1's unit_task to 'bread_top'

##def action_production3(buffer1, buffer2):
##    buffer1['unit_task'] = 'bread_top'
##    buffer2['counting'] = 'four'    
production3 = {
    'match1': {'planning_unit': 'ham&cheese', 'unit_task': 'ham'},
    'match2': {'counting': 'three'},
    'negative1': {'unit_task': 'cat'},
    'negative2': {'counting': 'nine'},
    'utility': 3,
    'action': action_production3,
    'report': 'Production 3 fired: Changed unit_task to bread_top in buffer1 and counting to four in buffer2'
}

def action_production4(buffer1, buffer2):
    buffer1['unit_task'] = 'stop'
    buffer2['counting'] = 'stop'
production4 = {
    'match1': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_top'},
    'match2': {'counting': 'four'},
    'negative1': {},
    'negative2': {},
    'utility': 4,
    'action': action_production4,
    'report': 'Production 4 fired: Changed unit_task to stop in buffer1 and counting to stop in buffer2'
}


# Production list
productions = [production1, production2, production3, production4]


# Main execution loop
reports = []  # to capture the output
while True:
    production_matched = False
    match_list = []

    for production in productions:
        if buffer_match_eval(buffer_chunk1, production['match1'], production, 'negative1') and \
           buffer_match_eval(buffer_chunk2, production['match2'], production, 'negative2'):
            match_list.append(production)
            production_matched = True
    
    if production_matched:
        max_match = find_max(match_list)
        report_info = max_match.get('report')

        # Call the action function for the selected production
        max_match['action'](buffer_chunk1, buffer_chunk2)

        # Collecting the output
        reports.append(report_info)
        reports.append("Updated buffer chunk1: " + str(buffer_chunk1))
        reports.append("Updated buffer chunk2: " + str(buffer_chunk2))
    else:
        reports.append("No matching production found.")
        break  # No production matched both buffers, end the loop

#reports

# Since we collected the reports in the 'reports' list, we can now print them out in sequence.
for report in reports:
    print(report)

