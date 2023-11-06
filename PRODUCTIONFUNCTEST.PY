# Define the match evaluation function
def buffer_match_eval(buffer_dict, matching_dict, negation_dict, wildcard='*'):
    for key in matching_dict.keys():
        if key not in buffer_dict:
            return False
        if matching_dict[key] != buffer_dict[key] and matching_dict[key] != wildcard:
            return False
    for key, neg_value in negation_dict.items():
        if key in buffer_dict and negation_dict[key] == buffer_dict[key]:
            return False
    return True

# Find the production with the maximum utility
def find_max(match_list):
    highest_utility = float('-inf')
    highest_utility_production = None
    for item in match_list:
        utility = item.get('utility', float('-inf'))
        if utility > highest_utility:
            highest_utility = utility
            highest_utility_production = item
    return highest_utility_production

# Define the updated action functions to accept a list of buffers
def action_test_production1(buffers):
    buffers[1]['test'] = 'two'

def action_test_production2(buffers):
    buffers[1]['test'] = 'three'

def action_test_production3(buffers):
    buffers[1]['test'] = 'four'

def action_test_production4(buffers):
    buffers[1]['test'] = 'five'

def action_test_production5(buffers):
    buffers[1]['test'] = 'six'

# Define the production rules with lists for matches and negations
productions = [
    {
        'matches': [{'test': 'cat'}, {'test': 'one'}],
        'negations': [{}, {}],
        'utility': 10,
        'action': action_test_production1,
        'report': 'Test Production 1 fired: Simple positive match passed.'
    },
    {
        'matches': [{'test': '*'}, {'test': 'two'}],
        'negations': [{}, {}],
        'utility': 20,
        'action': action_test_production2,
        'report': 'Test Production 2 fired: Match with wildcard passed.'
    },
    {
        'matches': [{}, {'test': 'three'}],
        'negations': [{'test': 'dog'}, {}],
        'utility': 30,
        'action': action_test_production3,
        'report': 'Test Production 3 fired: Negative match passed.'
    },
    {
        'matches': [{'test': '*'}, {'test': 'four'}],
        'negations': [{'test': 'dog'}, {}],
        'utility': 40,
        'action': action_test_production4,
        'report': 'Test Production 4 fired: Combination of matches passed.'
    },
    {
        'matches': [{}, {'test': 'five'}],
        'negations': [{}, {}],
        'utility': 10,
        'action': action_test_production5,
        'report': 'Test Production 5 fired: Simple positive match with empty match condition passed.'
    }
]

# Initialize the buffers
buffers = [{'test':'cat'}, {'test': 'one'}]

# Main execution loop
reports = []  # to capture the output
while True:
    production_matched = False
    match_list = []

    for production in productions:
        if all(buffer_match_eval(buffers[i], production['matches'][i], production['negations'][i])
               for i in range(len(buffers))):
            match_list.append(production)
            production_matched = True
    
    if production_matched:
        max_match = find_max(match_list)
        report_info = max_match.get('report')

        # Call the action function for the selected production
        max_match['action'](buffers)

        # Collecting the output
        reports.append(report_info)
        for i, buffer in enumerate(buffers):
            reports.append(f"Updated buffer chunk{i+1}: {str(buffer)}")
    else:
        reports.append("No matching production found.")
        break  # No production matched, end the loop

# Prepare the report outputs
report_outputs = "\n".join(reports)
report_outputs

# Print out the reports
print(report_outputs)
