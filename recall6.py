# chooses highest utility or random
# wild card works with negation
# chunks that do not have a specific slot:wildcard are not rejected based
# on not having that slot, instead the slot is created and the value is None
# this is consistent with ACT-R theory that the slot names do not play a role

import random


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


# Redefining the functions and variables as the code execution state was reset

def buffer_match_eval_diagnostic(buffer_dict, matching_dict, negation_dict, wildcard='*'):
    wildcard_values = {}  # Initialize a dictionary to capture wildcard values

    print(f"\nEvaluating buffer: {buffer_dict}")
    print(f"Against matching criteria: {matching_dict} and negation criteria: {negation_dict}")

    # Check for positive matches
    for key, match_value in matching_dict.items():
        if match_value == wildcard:
            print(f"Wildcard for key: {key}, any value is acceptable.")
            wildcard_values[key] = buffer_dict.get(key, None)  # Capture the actual value from the buffer
            continue  # Skip to the next iteration

        print(f"Checking match for key: {key} with value: {match_value}")
        if key not in buffer_dict or buffer_dict[key] != match_value:
            print("Match failed!")
            return False, {}  # Return False and an empty wildcard values dictionary
        print("Match succeeded!")

    # Check for negations
    for key, neg_value in negation_dict.items():
        print(f"Checking negation for key: {key} with value: {neg_value}")
        if key in buffer_dict and buffer_dict[key] == neg_value:
            print("Negation failed!")
            return False, {}  # Return False and an empty wildcard values dictionary
        print("Negation succeeded!")

    print("Buffer item passed all criteria.")
    return True, wildcard_values  # Return both the result and the captured wildcard values


def match_chunks_with_diagnostics(buffer, cue):
    matched_chunks_data = []  # To hold full data of matched chunks

    for buffer_key, buffer_value in buffer.items():
        print(f"\nProcessing buffer item: {buffer_key}")
        match, wildcard_values = buffer_match_eval_diagnostic(buffer_value, cue['matches'], cue['negations'])
        if match:
            matched_chunk_data = buffer_value.copy()  # Copy the full chunk data
            matched_chunk_data.update(wildcard_values)  # Update with wildcard values
            matched_chunks_data.append(matched_chunk_data)  # Add full chunk data to the list
            print(f"Appending {buffer_key} to matches with wildcard values: {wildcard_values}")

    # Apply find_max to select the best chunk based on utility
    best_chunk_data = find_max(matched_chunks_data)

    # Return only the best matching chunk and its wildcard values (if any)
    return best_chunk_data



DM = {
    'c1': {'animal': 'cat', 'colour': 'brown', 'utility': 25},  # Example utility values
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

