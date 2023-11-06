def buffer_match_eval(buffer_dict, matching_dict, negation_dict, wildcard='*'):
    for key, match_value in matching_dict.items():
        if match_value != wildcard:
            if key not in buffer_dict or buffer_dict[key] != match_value:
                return False
    for key, neg_value in negation_dict.items():
        if key in buffer_dict and buffer_dict[key] == neg_value:
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
    buffers[2]['fruit'] = 'apple'

def action_test_production6(buffers):
    buffers[1]['test'] = 'seven'


productions = [
    {
        'matches': [{'animal': 'cat', 'colour': 'brown'}, {'test': 'one'}],
        'negations': [{}, {}],
        'utility': 10,
        'action': action_test_production1,
        'report': 'Test Production 1 fired: Match on one of two key value pairs in buffer.'
    },
    {
        'matches': [{'animal': '*'}, {'test': 'two'}],
        'negations': [{}, {}],
        'utility': 20,
        'action': action_test_production2,
        'report': 'Test Production 2 fired: Match with wildcard passed.'
    },
    {
        'matches': [{}, {'test': 'three'}],
        'negations': [{'animal': 'dog'}, {}],
        'utility': 30,
        'action': action_test_production3,
        'report': 'Test Production 3 fired: Negative match passed.'
    },
    {
        'matches': [{'animal': '*'}, {'test': 'four'}],
        'negations': [{'animal': 'dog'}, {}],
        'utility': 40,
        'action': action_test_production4,
        'report': 'Test Production 4 fired: Combination of matches passed.'
    },
    {
        'matches': [{}, {'test': 'five'}],
        'negations': [{}, {}],
        'utility': 10,
        'action': action_test_production5,
        'report': 'Test Production 5 fired: changed the third buffer contents.'
    },
    {
        'matches': [{}, {'test': 'six'}, {'fruit': 'apple'}],
        'negations': [{}, {}],
        'utility': 10,
        'action': action_test_production6,
        'report': 'Test Production 6 fired: Third buffer used.'
    }
]

buffers = [{'animal': 'cat', 'colour': 'brown'}, {'test': 'one'}, {'fruit': 'pear'}]

reports = []

while True:
    production_matched = False
    match_list = []
    
    for production in productions:
        is_match_for_all_buffers = True
        
        for i, buffer in enumerate(buffers):
            if i < len(production['matches']):
                matches = production['matches'][i]
            else:
                matches = {}
            
            if i < len(production['negations']):
                negations = production['negations'][i]
            else:
                negations = {}
            
            if not buffer_match_eval(buffer, matches, negations):
                is_match_for_all_buffers = False
                break
        
        if is_match_for_all_buffers:
            match_list.append(production)
            production_matched = True

    if production_matched:
        max_match = find_max(match_list)
        report_info = max_match.get('report')
        max_match['action'](buffers)
        reports.append(report_info)
        for i, buffer in enumerate(buffers):
            reports.append(f"Updated buffer chunk{i+1}: {str(buffer)}")
    else:
        reports.append("No matching production found.")
        break

for report in reports:
    print(report)
