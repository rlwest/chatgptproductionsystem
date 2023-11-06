
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
buffer_chunk1 = {'test':'cat'}
buffer_chunk2 = {'test': 'one'}


# Productions
productions = []


# Test Production 1: Simple positive match
def action_test_production1(buffer1, buffer2):
    buffer2['test'] = 'two'
test_production1 = {
    'match1': {'test': 'cat'},
    'match2': {'test': 'one'},
    'negative1': {},
    'negative2': {},
    'utility': 10,
    'action': action_test_production1,
    'report': 'Test Production 1 fired: Simple positive match passed.'}
productions.append(test_production1)



# Test Production 2: Match with wildcard
def action_test_production2(buffer1, buffer2):
    buffer2['test'] = 'three'
test_production2 = {
    'match1': {'test': '*'},
    'match2': {'test': 'two'},
    'negative1': {},
    'negative2': {},
    'utility': 20,
    'action': action_test_production2,
    'report': 'Test Production 2 fired: Match with wildcard passed.'}
productions.append(test_production2)



# Test Production 3: Negative match
def action_test_production3(buffer1, buffer2):
    buffer2['test'] = 'four'
test_production3 = {
    'match1': {},
    'match2': {'test': 'three'},
    'negative1': {'test': 'dog'},
    'negative2': {},
    'utility': 30,
    'action': action_test_production3,
    'report': 'Test Production 3 fired: Negative match passed.'}
productions.append(test_production3)



# Test Production 4: Combination of positive, wildcard, and negative matches
def action_test_production4(buffer1, buffer2):
    buffer2['test'] = 'five'
test_production4 = {
    'match1': {'test': '*'},
    'match2': {'test': 'four'},
    'negative1': {'test': 'dog'},
    'negative2': {},
    'utility': 40,
    'action': action_test_production4,
    'report': 'Test Production 4 fired: Combination of matches passed.'}
productions.append(test_production4)

#print(productions)



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
