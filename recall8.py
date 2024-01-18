import random

# Check if a single key-value pair matches in the target dictionary
def check_match(key, value, target_dict, wildcard='*'):
    return key in target_dict and (value == wildcard or target_dict[key] == value)

# Check all positive matches in the matching dictionary against the buffer
def check_positive_matches(buffer_dict, matching_dict, wildcard='*'):
    return all(check_match(key, value, buffer_dict, wildcard) for key, value in matching_dict.items())

# Check all negations in the negation dictionary against the buffer
def check_negative_matches(buffer_dict, negation_dict):
    return not any(check_match(key, value, buffer_dict) for key, value in negation_dict.items())

# Evaluate if a buffer matches given positive and negative conditions
def buffer_match_eval(buffer_dict, matching_dict, negation_dict, wildcard='*'):
    return check_positive_matches(buffer_dict, matching_dict, wildcard) and check_negative_matches(buffer_dict, negation_dict)


def find_max(match_list):
    highest_utility = float('-inf')
    highest_utility_productions = []
    for item in match_list:
        utility = item.get('utility', float('-inf'))
        if utility > highest_utility:
            highest_utility = utility
            highest_utility_productions = [item]
        elif utility == highest_utility:
            highest_utility_productions.append(item)
    return random.choice(highest_utility_productions) if highest_utility_productions else None


# buffer_match_eval with diagnostics
def buffer_match_eval_diagnostic(buffer_dict, matching_dict, negation_dict, wildcard='*'):
    print(f"\nEvaluating buffer: {buffer_dict}")
    print(f"Against matching criteria: {matching_dict} and negation criteria: {negation_dict}")

    # Diagnostics and wildcard handling
    wildcard_values = {}
    for key, match_value in matching_dict.items():
        if match_value == wildcard:
            print(f"Wildcard for key: {key}, any value is acceptable.")
            wildcard_values[key] = buffer_dict.get(key, None)
            continue
        print(f"Checking match for key: {key} with value: {match_value}")
        if key not in buffer_dict or buffer_dict[key] != match_value:
            print("Match failed!")
            return False, {}
        print("Match succeeded!")

    for key, neg_value in negation_dict.items():
        print(f"Checking negation for key: {key} with value: {neg_value}")
        if key in buffer_dict and buffer_dict[key] == neg_value:
            print("Negation failed!")
            return False, {}
        print("Negation succeeded!")

    print("Buffer item passed all criteria.")
    return True, wildcard_values



def match_chunks_with_diagnostics(buffer, cue):
    matched_chunks_data = []
    for buffer_key, buffer_value in buffer.items():
        print(f"\nProcessing buffer item: {buffer_key}")
        match, wildcard_values = buffer_match_eval_diagnostic(buffer_value, cue['matches'], cue['negations'])
        if match:
            matched_chunk_data = buffer_value.copy()
            matched_chunk_data.update(wildcard_values)
            matched_chunks_data.append(matched_chunk_data)
            print(f"Appending {buffer_key} to matches with wildcard values: {wildcard_values}")

    best_chunk_data = find_max(matched_chunks_data)
    return best_chunk_data

# Example data and cue
DM = {
    'c1': {'animal': 'cat', 'colour': 'brown', 'utility': 25},
    'c2': {'animal': 'cat', 'colour': 'white', 'name': 'whitney', 'utility': 20},
    'f1': {'animal': 'fish', 'colour': 'blue', 'utility': 15}
}

cue = {
    'matches': {'animal': 'cat', 'colour': '*', 'name': '*'},
    'negations': {}
}

# Call the function and save the result
best_chunk_data = match_chunks_with_diagnostics(DM, cue)

# Print the result outside the function
print("Best Chunk Data:", best_chunk_data)
