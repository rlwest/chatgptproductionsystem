# Define a Buffer class to encapsulate the attributes of a buffer.
class Buffer:
    def __init__(self, **kwargs):
        # Use the provided keyword arguments to update the buffer's attributes.
        self.__dict__.update(kwargs)

# Define a base Production class to represent a production rule.
class Production:
    def __init__(self, match, negative, utility, report):
        # Initialize the production with matching criteria, negation criteria, utility value, and a report message.
        self.match = match
        self.negative = negative
        self.utility = utility
        self.report = report

    def action(self, buffer1, buffer2):
        # Define an action method that should be implemented by subclasses.
        raise NotImplementedError("Subclasses should implement this!")

    def matches(self, buffer1, buffer2):
        # Check if the production matches the current buffer states.
        # It uses the buffer_match_eval function to check for both positive and negative matching criteria.
        return buffer_match_eval(buffer1.__dict__, self.match['match1'], self.negative, 'negative1') and \
               buffer_match_eval(buffer2.__dict__, self.match['match2'], self.negative, 'negative2')

# Define the buffer matching function.
def buffer_match_eval(buffer_dict, matching_dict, negation_dict, negation_key, wildcard='*'):
    # Check if the buffer matches the positive criteria.
    for key, value in matching_dict.items():
        if key not in buffer_dict or (buffer_dict[key] != value and value != wildcard):
            return False
    # Check if the buffer does not match any negative criteria.
    for key, value in negation_dict.get(negation_key, {}).items():
        if key in buffer_dict and negation_dict[negation_key][key] == buffer_dict[key]:
            return False
    return True

# Define the function to find the production with the maximum utility.
def find_max(match_list):
    highest_utility = float('-inf')
    highest_utility_production = None
    for production in match_list:
        if production.utility > highest_utility:
            highest_utility = production.utility
            highest_utility_production = production
    return highest_utility_production

# Subclass Production to create specific production rules with custom actions.

class Production1(Production):
    def action(self, buffer1, buffer2):
        # Define the specific action for Production1.
        buffer1.unit_task = 'cheese'
        buffer2.counting = 'two'
        
class Production2(Production):
    def action(self, buffer1, buffer2):
        buffer1.unit_task = 'ham'
        buffer2.counting = 'three'

class Production3(Production):
    def action(self, buffer1, buffer2):
        buffer2.counting = buffer1.unit_task
        buffer1.unit_task = 'bread_top'

class Production4(Production):
    def action(self, buffer1, buffer2):
        buffer1.unit_task = 'stop'
        buffer2.counting = 'stop'
# Define Production2, Production3, and Production4 subclasses with their specific actions.
# ...

# Instantiate Buffers with initial states.
buffer1 = Buffer(planning_unit='ham&cheese', unit_task='bread_bottom')
buffer2 = Buffer(counting='one')

# Instantiate Productions with their respective match criteria, negation criteria, utility values, and reports.
productions = [
    # Production 1 changes the unit_task to 'cheese' and counting to 'two'.
    Production1(
        match={'match1': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_bottom'}, 'match2': {'counting': 'one'}},
        negative={'negative1': {}, 'negative2': {}},
        utility=1,
        report='Production 1 fired: Changed unit_task to cheese in buffer1 and counting to two in buffer2'
    ),
        Production2(
        match={'match1': {'planning_unit': '*', 'unit_task': 'cheese'}, 'match2': {'counting': 'two'}},
        negative={'negative1': {}, 'negative2': {}},
        utility=2,
        report='Production 2 fired: Changed unit_task to ham in buffer1 and counting to three in buffer2'
    ),
    Production3(
        match={'match1': {'planning_unit': 'ham&cheese', 'unit_task': 'ham'}, 'match2': {'counting': 'three'}},
        negative={'negative1': {'unit_task': 'cat'}, 'negative2': {'counting': 'nine'}},
        utility=3,
        report='Production 3 fired: Transferred unit_task from buffer1 to counting in buffer2 and updated unit_task to bread_top in buffer1'
    ),
    Production4(
        match={'match1': {'planning_unit': 'ham&cheese', 'unit_task': 'bread_top'}, 'match2': {'counting': 'four'}},
        negative={'negative1': {}, 'negative2': {}},
        utility=4,
        report='Production 4 fired: Changed unit_task to stop in buffer1 and counting to stop in buffer2'
    )
    # Other productions should be instantiated similarly.
    # ...
]

# Main execution loop with an iteration limit to prevent infinite looping.
max_iterations = 10  # Set a maximum number of iterations.
current_iteration = 0
reports = []  # List to hold report strings.

while current_iteration < max_iterations:
    # Build a list of productions that match the current buffer states.
    match_list = [p for p in productions if p.matches(buffer1, buffer2)]
    
    # If there are matching productions, find the one with the highest utility and execute its action.
    if match_list:
        max_match = find_max(match_list)
        max_match.action(buffer1, buffer2)

        # Add the report of the executed production to the reports list.
        reports.append(max_match.report)
        # Add the updated buffer states to the reports list.
        reports.append(f"Updated buffer1: {buffer1.__dict__}")
        reports.append(f"Updated buffer2: {buffer2.__dict__}")
    else:
        # If no productions match, add a report stating so and exit the loop.
        reports.append("No matching production found.")
        break

    # Increment the iteration count.
    current_iteration += 1

# Print out each report in the reports list.
for report in reports:
    print(report)

"""
The object-oriented approach here is used to model a production system in a structured and scalable way. Here's an explanation of how the object-oriented concepts are applied in this code:

### Classes and Instances
The code defines classes to represent the different components of the production system: `Buffer` and `Production`.

#### `Buffer` Class
- **Purpose**: Represents a memory store with key-value pairs.
- **Attributes**: Dynamically added via the `__init__` method using `**kwargs`. This allows each `Buffer` instance to have its own set of attributes (or "slots").
- **Usage**: Instances of `Buffer` are created to hold the state of different memory buffers.

#### `Production` Class
- **Purpose**: Acts as a base class for production rules.
- **Attributes**:
  - `match`: The positive matching criteria for the production.
  - `negative`: The negation criteria that specify what must not be present in the buffer for the production to match.
  - `utility`: A numerical value representing the utility (or "priority") of the production.
  - `report`: A string describing the action taken when the production fires.
- **Methods**:
  - `action()`: An abstract method that is intended to be overridden by subclasses to define the specific actions of the production.
  - `matches()`: Determines whether the production's positive and negative criteria match the current state of the buffers.

#### Subclasses of `Production`
- **Purpose**: Each subclass represents a specific production rule with its own matching criteria and action.
- **Usage**: Instances of these subclasses are created to represent individual production rules. Each subclass overrides the `action()` method to perform the specific action associated with that production.

### Polymorphism
The `action()` method in the `Production` class is abstract, with the expectation that each subclass will provide its own implementation. This is an example of polymorphism, where the same method name (`action`) is used in the superclass and subclasses, but the behavior can differ between subclasses.

### Encapsulation
Each class encapsulates the data and behavior related to that particular entity. For example, the `Buffer` class encapsulates the attributes of a buffer, and the `Production` class encapsulates the logic for matching and executing a production rule.

### Inheritance
Subclasses of `Production` inherit the properties and the `matches()` method from the `Production` class. They override the `action()` method to provide specific behaviors. This is an example of inheritance, where a class (subclass) inherits attributes and behavior (methods) from another class (superclass).

### Composition
The production system is composed of instances of `Buffer` and `Production` subclasses. This composition is used in the main execution loop to simulate the production system's operation.

### Main Execution Loop
- **Logic**: Iterates over the list of production instances, checks for a match against the current buffer states, and executes the action of the production with the highest utility that matches.
- **Control Flow**: The loop has a maximum iteration limit to prevent infinite execution. It breaks out of the loop if there are no matching productions or if the iteration limit is reached.

### Scalability and Maintainability
The object-oriented design allows the system to be easily extended with new `Production` subclasses for additional rules without modifying existing code, adhering to the Open-Closed Principle, a key tenet of object-oriented design.

The overall logic is to use the object-oriented design to represent a system where production rules are checked against buffers, and the highest utility rule that matches is executed, transforming the state of the buffers. The approach provides a clear structure that models the components and their interactions, making the system more maintainable and extendable.
"""
