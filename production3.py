class ProductionRule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def is_triggered(self, environment):
        return self.condition(environment)

    def perform_action(self, environment):
        self.action(environment)

# Updated conditions and actions
def condition1(environment):
    return environment.get("state") == "A"

def action1(environment):
    print("Action 1 performed")
    environment["state"] = "B"

def condition2(environment):
    return environment.get("state") == "B"

def action2(environment):
    print("Action 2 performed")
    environment["state"] = "A"

# Sample environment
environment = {"state": "A"}

# Sample production rules
rule1 = ProductionRule(condition1, action1)
rule2 = ProductionRule(condition2, action2)

# List of production rules
production_rules = [rule1, rule2]

# Run the production system
def run_production_system(environment, production_rules):
    while True:
        for rule in production_rules:
            if rule.is_triggered(environment):
                rule.perform_action(environment)
                break

        # Uncomment the next line to exit the loop after a certain number of cycles
        # break

# Simulate the production system
run_production_system(environment, production_rules)
