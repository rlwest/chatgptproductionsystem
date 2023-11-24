import random

# This function checks if the conditions for a production rule are met in a given buffer.
# It considers both positive matches (what should be there) and negations (what should not be there).
def buffer_match_eval(buffer_dict, matching_dict, negation_dict, wildcard='*'):
    # Check for positive matches. If a value is specified in matching_dict, it must be present in buffer_dict.
    for key, match_value in matching_dict.items():
        if match_value != wildcard:  # The wildcard indicates any value is acceptable for this key.
            if key not in buffer_dict or buffer_dict[key] != match_value:
                return False  # If the specific key-value pair is not found, return False.

    # Check for negations. If a key-value pair is present in negation_dict, it must not be in buffer_dict.
    for key, neg_value in negation_dict.items():
        if key in buffer_dict and buffer_dict[key] == neg_value:
            return False  # If a negated key-value pair is found, return False.

    return True  # If all conditions are met, return True.


# This function selects a production with the highest utility from a list of matching productions.
def find_max(match_list):
    highest_utility = float('-inf')
    highest_utility_productions = []
    for item in match_list:
        utility = item.get('utility', float('-inf'))  # Retrieve the utility of the production.
        # Update the list of highest utility productions based on the current production's utility.
        if utility > highest_utility:
            highest_utility = utility
            highest_utility_productions = [item]
        elif utility == highest_utility:
            highest_utility_productions.append(item)
    # Randomly choose one production if there are multiple productions with the highest utility.
    return random.choice(highest_utility_productions) if highest_utility_productions else None



def match_productions(buffers, prodsys):
    matched_productions = []

    # Decrease the delay for each production system and check for matches.
    for prod_system_key, prod_system_value in prodsys.items():
        if prod_system_value[1] > 0:
            prod_system_value[1] -= 1

        prod_system = prod_system_value[0]  # List of production rules.
        delay = prod_system_value[1]  # Current delay for the system.

        if delay > 0:
            continue

        random.shuffle(prod_system)  # Shuffle for randomness.

        for production in prod_system:
            is_match_for_all_buffers = True
            for buffer_key in production['matches'].keys():
                matches = production['matches'].get(buffer_key, {})
                negations = production['negations'].get(buffer_key, {})
                if not buffer_match_eval(buffers.get(buffer_key, {}), matches, negations):
                    is_match_for_all_buffers = False
                    break

            if is_match_for_all_buffers:
                matched_productions.append((prod_system_key, production))
                print('PRODUCTION FIRED')
                print(f"Matched Production in {prod_system_key}: {production.get('report')}")

                
    return matched_productions


pending_actions = []  # Global list to track pending actions


def execute_actions(buffers, matched_productions, prodsys, original_delays):
    global pending_actions

    # Process pending actions with non-zero delay
    for i in range(len(pending_actions) - 1, -1, -1):
        prod_system_key, production, delay = pending_actions[i]
        if delay <= 1:
            production['action'](buffers)  # Execute action
            report_info = production.get('report')
            print('ACTION TAKEN')
            print(report_info)
            prodsys[prod_system_key][1] = original_delays[prod_system_key]
            del pending_actions[i]
        else:
            pending_actions[i] = (prod_system_key, production, delay - 1)

    # Process newly matched productions
    for prod_system_key, production in matched_productions:
        delay = production['action'](buffers)  # Get delay from the action
        if delay > 0:
            # Add to pending actions if delay is non-zero
            pending_actions.append((prod_system_key, production, delay))
        else:
            # Execute immediately if delay is zero
            report_info = production.get('report')
            print('ACTION TAKEN')
            print(report_info)
            prodsys[prod_system_key][1] = original_delays[prod_system_key]


### production system 1

prodsys_1_cycles=5


def action_test_production1(buffers):
    buffers['buffer2']['test'] = 'two'
    buffers['buffer1']['animal'] = buffers['buffer2']['number']
    return 0  # Delay for 2 cycles

def action_test_production2(buffers):
    buffers['buffer2']['test'] = 'three'
    buffers['buffer2']['number'] = buffers['buffer2']['number'] + 2
    return 0  # Delay for 2 cycles

def action_test_production3(buffers):
    buffers['buffer2']['test'] = 'four'
    A = 2 + 2
    buffers['buffer2']['number'] = A
    return 2  # Delay for 2 cycles

def action_test_production4(buffers):
    buffers['buffer2']['test'] = 'five'
    return 2  # Delay for 2 cycles

def action_test_production5(buffers):
    buffers['buffer2']['test'] = 'siprodsys_1_cycles'
    buffers['buffer3']['fruit'] = 'apple'
    return 2  # Delay for 2 cycles

def action_test_production6(buffers):
    buffers['buffer2']['test'] = 'seven'
    buffers['buffer1']['animal'] = 'dog'
    buffers['buffer1']['colour'] = 'golden'
    return 20  # Delay for 2 cycles

def action_test_production6b(buffers):
    buffers['buffer2']['test'] = 'seven'
    buffers['buffer1']['animal'] = 'rat'
    buffers['buffer1']['colour'] = 'blue'
    return 2  # Delay for 2 cycles

productions = [
    {
        'matches': {'buffer1': {'animal': 'cat', 'colour': 'brown'}, 'buffer2': {'test': 'one'}},
        'negations': {},
        'utility': 10,
        'action': action_test_production1,
        'name':'p1',
        'report': """* Test Production 1 fired:
            Match on one of two key value pairs in buffer
            Transfer value to other buffer
            Sets animal to a number"""
    },
    {
        'matches': {'buffer1': {'animal': '*'}, 'buffer2': {'test': 'two'}},
        'negations': {},
        'utility': 20,
        'action': action_test_production2,
        'name':'p2',
        'report': '''* Test Production 2 fired:
            Match with wildcard passed.
            Adds 2 to animal number'''
    },
    {
        'matches': {'buffer2': {'test': 'three'}},
        'negations': {'buffer1': {'animal': 'dog'}, 'buffer2': {}},
        'utility': 30,
        'action': action_test_production3,
        'name':'p3',
        'report': '''* Test Production 3 fired:
            Negative match passed.
            Does a calculation, puts answer in buffer'''
    },
    {
        'matches': {'buffer1': {'animal': '*'}, 'buffer2': {'test': 'four'}},
        'negations': {'buffer1': {'animal': 'dog'}},
        'utility': 40,
        'action': action_test_production4,
        'report': '* Test Production 4 fired: Combination of matches passed.'
    },
    {
        'matches': {'buffer2': {'test': 'five'}},
        'negations': {},
        'utility': 10,
        'action': action_test_production5,
        'report': '* Test Production 5 fired: changed the third buffer numbers.'
    },
    {
        'matches': {'buffer2': {'test': 'siprodsys_1_cycles'}, 'buffer3': {'fruit': 'apple'}},
        'negations': {},
        'utility': 10,
        'action': action_test_production6,
        'report': '* Test Production 6 fired: Third and first buffers used.'
    },
    {
        'matches': {'buffer2': {'test': 'siprodsys_1_cycles'}, 'buffer3': {'fruit': 'apple'}},
        'negations': {},
        'utility': 10,
        'action': action_test_production6b,
        'report': '* Test Production 6b fired: Shows random choice between equal utilities.'
    }
]

### production system 2


prodsys_2_cycles=1

def action_test_production1b(buffers):
    buffers['buffer4']['fish'] = 'salmon'
    return 0  # Delay for 2 cycles

def action_test_production2b(buffers):
    buffers['buffer4']['fish'] = 'shark'
    return 0  # Delay for 2 cycles

productions_b = [
    {
        'matches': {'buffer4': {'fish': 'tuna'}},
        'negations': {},
        'utility': 10,
        'action': action_test_production1b,
        'report': """* - Test Production 1b fired:
            Parallel production system fired:
            Match on buffer3"""
    },
    {
        'matches': {'buffer4': {'fish': 'salmon'}},
        'negations': {},
        'utility': 10,
        'action': action_test_production2b,
        'report': """* - Test Production 2b fired:
            Parallel production system fired:
            Match on buffer3"""
    }
]



# Initialize buffers and production systems
buffers = {'buffer1': {'animal': 'cat', 'colour': 'brown'}, 
           'buffer2': {'test': 'one', 'number': 5}, 
           'buffer3': {'fruit': 'pear'}, 
           'buffer4': {'fish': 'tuna'}}


prodsys = {'production1': [productions, prodsys_1_cycles],  'production2': [productions_b, prodsys_2_cycles]}

original_delays = {
    'production1': prodsys_1_cycles,
    'production2': prodsys_2_cycles}

cycles = 40
millisecpercycle = 10


for cycle_number in range(cycles):
    print('Milliseconds', (cycle_number+1) * millisecpercycle, '*******************')
    matched_productions = match_productions(buffers, prodsys)
    execute_actions(buffers, matched_productions, prodsys, original_delays)


