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
    buffers['buffer2']['test'] = 'two'

def action_test_production2(buffers):
    buffers['buffer2']['test'] = 'three'

def action_test_production3(buffers):
    buffers['buffer2']['test'] = 'four'

def action_test_production4(buffers):
    buffers['buffer2']['test'] = 'five'

def action_test_production5(buffers):
    buffers['buffer2']['test'] = 'six'
    buffers['buffer3']['fruit'] = 'apple'

def action_test_production6(buffers):
    buffers['buffer2']['test'] = 'seven'
    buffers['buffer1']['animal'] = 'dog'
    buffers['buffer1']['colour'] = 'golden'



productions = [
    {
        'matches': {'buffer1': {'animal': 'cat', 'colour': 'brown'}, 'buffer2': {'test': 'one'}},
        'negations': {},
        'utility': 10,
        'action': action_test_production1,
        'report': 'Test Production 1 fired: Match on one of two key value pairs in buffer.'
    },
    {
        'matches': {'buffer1': {'animal': '*'}, 'buffer2': {'test': 'two'}},
        'negations': {},
        'utility': 20,
        'action': action_test_production2,
        'report': 'Test Production 2 fired: Match with wildcard passed.'
    },
    {
        'matches': {'buffer2': {'test': 'three'}},
        'negations': {'buffer1': {'animal': 'dog'}, 'buffer2': {}},
        'utility': 30,
        'action': action_test_production3,
        'report': 'Test Production 3 fired: Negative match passed.'
    },
    {
        'matches': {'buffer1': {'animal': '*'}, 'buffer2': {'test': 'four'}},
        'negations': {'buffer1': {'animal': 'dog'}},
        'utility': 40,
        'action': action_test_production4,
        'report': 'Test Production 4 fired: Combination of matches passed.'
    },
    {
        'matches': {'buffer2': {'test': 'five'}},
        'negations': {},
        'utility': 10,
        'action': action_test_production5,
        'report': 'Test Production 5 fired: changed the third buffer contents.'
    },
    {
        'matches': {'buffer2': {'test': 'six'}, 'buffer3': {'fruit': 'apple'}},
        'negations': {},
        'utility': 10,
        'action': action_test_production6,
        'report': 'Test Production 6 fired: Third and first buffers used.'
    }
]

buffers = {'buffer1': {'animal': 'cat', 'colour': 'brown'}, 'buffer2': {'test': 'one'}, 'buffer3': {'fruit': 'pear'}}

reports = []

while True:
    production_matched = False
    match_list = []
    
    for production in productions:
        is_match_for_all_buffers = True
        
        # Iterating through each buffer defined in the production's 'matches' and 'negations'
        for buffer_key in production['matches'].keys():
            matches = production['matches'].get(buffer_key, {})
            negations = production['negations'].get(buffer_key, {})
            
            if not buffer_match_eval(buffers[buffer_key], matches, negations):
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
        for buffer_key in buffers.keys():
            reports.append(f"Updated {buffer_key}: {str(buffers[buffer_key])}")
    else:
        reports.append("No matching production found.")
        break

for report in reports:
    print(report)

