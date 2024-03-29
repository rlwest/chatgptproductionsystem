# this all work
# print statements could be better

import random
     
# create the ProductionCycle class ###########################################################################


class ProductionCycle:
    def __init__(self):
        self.pending_actions = []


    # buffer_match_eval checks if a cue chunk matches any chunks in a given buffer.
    # It considers both positive matches (what should be there) and negations (what should not be there).
    # buffer_dict is the target buffer
    # matching_dict and negation_dict and wildcard specifie the cue
    # these functions are needed by buffer_match_eval

    # Check if a single key-value pair matches in the target dictionary
    def check_match(self, key, value, target_dict, wildcard='*'):
        return key in target_dict and (value == wildcard or target_dict[key] == value)

    # Check all positive matches in the matching dictionary against the buffer
    def check_positive_matches(self, buffer_dict, matching_dict, wildcard='*'):
        return all(self.check_match(key, value, buffer_dict, wildcard) for key, value in matching_dict.items())

    # Check all negations in the negation dictionary against the buffer
    def check_negative_matches(self, buffer_dict, negation_dict):
        return not any(self.check_match(key, value, buffer_dict) for key, value in negation_dict.items())

    # Evaluate if a buffer matches given positive and negative conditions
    def buffer_match_eval(self, buffer_dict, matching_dict, negation_dict, wildcard='*'):
        return self.check_positive_matches(buffer_dict, matching_dict, wildcard) and self.check_negative_matches(buffer_dict, negation_dict)

    # buffer_match_eval
    def buffer_match_eval(self, buffer_dict, matching_dict, negation_dict, wildcard='*'):
        """Evaluate if a buffer matches given positive and negative conditions."""
        return self.check_positive_matches(buffer_dict, matching_dict, wildcard) and self.check_negative_matches(buffer_dict, negation_dict)


    # This function selects a production with the highest utility from a list of matching productions.
    def find_max(self, match_list):
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




    def match_productions(self, working_memory, AllProductionSystems):
        """Finds and groups matched productions."""
        grouped_matched_productions = {key: [] for key in AllProductionSystems}  # Initialize the dictionary

        # Decrease the delay for each production system and check for matches.
        for prod_system_key, prod_system_value in AllProductionSystems.items():
            if prod_system_value[1] > 0:
                prod_system_value[1] -= 1

            prod_system = prod_system_value[0]  # List of production rules.
            delay = prod_system_value[1]  # Current delay for the system.

            if delay > 0:
                continue

            for production in prod_system:
                is_match_for_all_buffers = True
                for buffer_key in production['matches'].keys():
                    matches = production['matches'].get(buffer_key, {})
                    negations = production['negations'].get(buffer_key, {})
                    if not self.buffer_match_eval(working_memory.get(buffer_key, {}), matches, negations):
                        is_match_for_all_buffers = False
                        break

                if is_match_for_all_buffers:
                    grouped_matched_productions[prod_system_key].append(production)
                    print('PRODUCTION MATCHED')
                    print(f"Matched Production in {prod_system_key}: {production.get('report')}")

        return grouped_matched_productions



    def process_pending_actions(self, working_memory, AllProductionSystems, ProductionSystemDelays):
        """
        Processes pending actions that are scheduled to be executed.
        Deals with the execution and management of actions that were previously scheduled and are now due

        This method iterates through the list of pending actions in reverse order,
        executing those that have completed their delay period and updating the delay
        for others.

        Args:
            working_memory (dict): The current state of all buffers.
            AllProductionSystems (dict): Dictionary containing production systems and their current delays.
            ProductionSystemDelays (dict): Dictionary containing the original delays for each production system.
        """
        for i in range(len(self.pending_actions) - 1, -1, -1):
            prod_system_key, production, delay = self.pending_actions[i]
            
            # Check if the delay period is completed
            if delay <= 1:
                # Execute the action associated with the production
                production['action'](working_memory)
                report_info = production.get('report')
                print(f'[ACTION TAKEN] Executing action for production {production.get("report")}.')
                print(f'[REPORT] {report_info}')
                
                # Reset the delay for the production system to its original value
                AllProductionSystems[prod_system_key][1] = ProductionSystemDelays[prod_system_key]
                print(f'[INFO] Delay for production system {prod_system_key} reset to original value.')

                # Remove the action from pending actions
                del self.pending_actions[i]
            else:
                # If the delay is not yet completed, decrement it
                self.pending_actions[i] = (prod_system_key, production, delay - 1)
                print(f'[INFO] Delay for action in production {production.get("report")} decremented. Remaining delay: {delay - 1}')


    
    def filter_and_execute_productions(self, grouped_productions, working_memory, AllProductionSystems, ProductionSystemDelays):
        """
        Selects the production with the highest utility matched production for each production system.
        Executes the selected production's action if there is no delay
        Manages action delays by scheduling them for future execution
        Resetting the production system delay for production systems that fired

        Args:
            grouped_productions (dict): A dictionary of matched productions grouped by production system.
            working_memory (dict): The current state of all buffers.
            AllProductionSystems (dict): Dictionary containing production systems and their current delays.
            ProductionSystemDelays (dict): Dictionary containing the original delays for each production system.
        """
        for prod_system_key, productions in grouped_productions.items():
            # Find the production with the highest utility in the current production system
            highest_utility_production = self.find_max(productions)
            
            if highest_utility_production:
                # Reporting the selected production
                print(f"[INFO] Production System '{prod_system_key}' selected production: '{highest_utility_production.get('report')}'")

                # Execute the action associated with the selected production
                delay = highest_utility_production['action'](working_memory)

                if delay > 0:
                    # If the action has a delay, add it to the pending actions
                    self.pending_actions.append((prod_system_key, highest_utility_production, delay))
                    print(f"[INFO] Action from production '{highest_utility_production.get('report')}' has been scheduled with a delay of {delay} cycles.")
                else:
                    # If no delay, print the action report and reset the production system delay
                    report_info = highest_utility_production.get('report')
                    print('[ACTION TAKEN] ' + report_info)
                    AllProductionSystems[prod_system_key][1] = ProductionSystemDelays[prod_system_key]
                    print(f"[INFO] Production System '{prod_system_key}' delay reset to its original value.")



    def execute_actions(self, working_memory, matched_productions, AllProductionSystems, ProductionSystemDelays):
        """
        Executes actions based on matched productions.
        """

        # Process any actions that are pending from previous cycles
        print("[INFO] Processing pending actions.")
        self.process_pending_actions(working_memory, AllProductionSystems, ProductionSystemDelays)

        # The matched_productions dictionary is already grouped by production system keys
        print("[INFO] Filtering and executing matched productions.")
        self.filter_and_execute_productions(matched_productions, working_memory, AllProductionSystems, ProductionSystemDelays)




##### test set ###################################################

### Production System 1 - PS1

PS1_list = []


def action_test_ProductionSystem1(working_memory):
    working_memory['buffer2']['test'] = 'two'
    working_memory['buffer1']['animal'] = working_memory['buffer2']['number']
    return 0
PS1_list.append({
    'matches': {'buffer1': {'animal': 'cat', 'colour': 'brown'}, 'buffer2': {'test': 'one'}},
    'negations': {},
    'utility': 10,
    'action': action_test_ProductionSystem1,
    'report': "PS1-Production1"
})


def action_test_ProductionSystem2(working_memory):
    working_memory['buffer2']['test'] = 'three'
    working_memory['buffer2']['number'] = working_memory['buffer2']['number'] + 2
    return 2
PS1_list.append({
    'matches': {'buffer1': {'animal': '*'}, 'buffer2': {'test': 'two'}},
    'negations': {},
    'utility': 20,
    'action': action_test_ProductionSystem2,
    'report': 'PS1-Production2'
})


def action_test_production3(working_memory):
    working_memory['buffer2']['test'] = 'four'
    A = 2 + 2
    working_memory['buffer2']['number'] = A
    return 0
PS1_list.append({
    'matches': {'buffer2': {'test': 'three'}},
    'negations': {'buffer1': {'animal': 'dog'}, 'buffer2': {}},
    'utility': 30,
    'action': action_test_production3,
    'report': 'PS1-Production3'
})


def action_test_production4(working_memory):
    working_memory['buffer2']['test'] = 'five'
    return 3
PS1_list.append({
    'matches': {'buffer1': {'animal': '*'}, 'buffer2': {'test': 'four'}},
    'negations': {'buffer1': {'animal': 'dog'}},
    'utility': 40,
    'action': action_test_production4,
    'report': 'PS1-Production4'
})


def action_test_production5(working_memory):
    working_memory['buffer2']['test'] = 'siProductionSystem1_delay'
    working_memory['buffer3']['fruit'] = 'apple'
    return 0
PS1_list.append({
    'matches': {'buffer2': {'test': 'five'}},
    'negations': {},
    'utility': 10,
    'action': action_test_production5,
    'report': 'PS1-Production5'
})


def action_test_production6(working_memory):
    working_memory['buffer2']['test'] = 'seven'
    working_memory['buffer1']['animal'] = 'dog'
    working_memory['buffer1']['colour'] = 'golden'
    return 0
PS1_list.append({
    'matches': {'buffer2': {'test': 'siProductionSystem1_delay'}, 'buffer3': {'fruit': 'apple'}},
    'negations': {},
    'utility': 10,
    'action': action_test_production6,
    'report': 'PS1-Production6'
})


def action_test_production6b(working_memory):
    working_memory['buffer2']['test'] = 'seven'
    working_memory['buffer1']['animal'] = 'rat'
    working_memory['buffer1']['colour'] = 'blue'
    return 0
PS1_list.append({
    'matches': {'buffer2': {'test': 'siProductionSystem1_delay'}, 'buffer3': {'fruit': 'apple'}},
    'negations': {},
    'utility': 10,
    'action': action_test_production6b,
    'report': 'PS1-Production6b'
})


### Production System 2 - PS2

PS2_list = []


def action_test_ProductionSystem1b(working_memory):
    working_memory['buffer4']['fish'] = 'salmon'
    return 0
PS2_list.append({
    'matches': {'buffer4': {'fish': 'tuna'}},
    'negations': {},
    'utility': 10,
    'action': action_test_ProductionSystem1b,
    'report': "PS2-Production1"
})


def action_test_ProductionSystem2b(working_memory):
    working_memory['buffer4']['fish'] = 'shark'
    return 3
PS2_list.append({
    'matches': {'buffer4': {'fish': 'salmon'}},
    'negations': {},
    'utility': 10,
    'action': action_test_ProductionSystem2b,
    'report': "PS2-Production2"
})



# working memory - dictionary of all buffers

working_memory = {
    'buffer1': {'animal': 'cat', 'colour': 'brown'}, 
    'buffer2': {'test': 'one', 'number': 5}, 
    'buffer3': {'fruit': 'pear'}, 
    'buffer4': {'fish': 'tuna'}
}






# production system delays in ticks
ProductionSystem1_delay=1
ProductionSystem2_delay=2

# timing for all production systems
ProductionSystemDelays = {
    'ProductionSystem1': ProductionSystem1_delay,
    'ProductionSystem2': ProductionSystem2_delay}

# dictionary of all production systems and delays
AllProductionSystems = {'ProductionSystem1': [PS1_list, ProductionSystem1_delay],  'ProductionSystem2': [PS2_list, ProductionSystem2_delay]}



##### run the cycle #################################################################

# timing for tick system
cycles = 40
millisecpercycle = 10

# run ProductionCycle in tick cycles
ps = ProductionCycle()
for cycle_number in range(cycles):
    print()
    print('Milliseconds', (cycle_number+1) * millisecpercycle, '---------------------------------------')
    matched_productions = ps.match_productions(working_memory, AllProductionSystems)  # Call as a method of the instance
    ps.execute_actions(working_memory, matched_productions, AllProductionSystems, ProductionSystemDelays)

