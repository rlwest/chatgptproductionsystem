import random

# ... (other function definitions such as buffer_match_eval, find_max, etc.) ...

# Action functions
def action_test_production1(buffers):
    # ... (implementation of action_test_production1) ...

# ... (other action functions) ...

# Productions list
productions = [
    # ... (list of productions as provided in your original code) ...
]

# Buffers
buffers = {'buffer1': {'animal': 'cat', 'colour': 'brown'}, 'buffer2': {'test': 'one', 'number': 5}, 'buffer3': {'fruit': 'pear'}}

# Function to process productions
def process_productions(productions, buffers):
    while True:
        production_matched = False
        match_list = []
        
        for production in productions:
            is_match_for_all_buffers = True
            
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
            max_match['action'](buffers)
            print(max_match.get('report'))  # Print the report here
            for buffer_key in buffers.keys():
                print(f"Updated {buffer_key}: {str(buffers[buffer_key])}")
        else:
            print("No matching production found.")
            break

# Using the function in the main script
process_productions(productions, buffers)
