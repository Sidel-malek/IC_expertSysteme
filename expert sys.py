class ExpertSystem:
    
    def __init__(self, rule_file , initial_facts):
        self.rule_base = self.load_rules(rule_file)
        self.fact_base =initial_facts

    def load_rules(self, rule_file):
        with open(rule_file, 'r') as file:
            rule_lines = file.readlines()

        rule_base = []
        for line in rule_lines:
            rule_base.append(line.strip())

        return rule_base

    def parse_rule(self, rule):
     rule_parts = rule.split(':')
     a =  rule_parts[1].split(' THEN ')
     b = a[0].strip().split('IF ')
     premises = b[1]
     actions =  a[1].strip()
     return premises, actions
    
############## forward chaining functions ############
    def apply_forward_chaining(self, rules_used,fact, base):
      
     while True:
        rule_applied = False
        for rule in base:
                premise, action = self.parse_rule(rule)
                if premise in fact:
                    rules_used.append(rule.split(':')[0])
                    fact.append(action)
                    base.remove(rule)  
                    rule_applied = True

        if not rule_applied:
            break

     self.print_system_status(fact,rules_used)
     

        
############## backward chaining functions ############

    def apply_backward_chaining(self, goal , rules_used ,fact , base):
            rules = self.find_rules_for_goal(goal)
            if not rules:
                print(f"Goal cannot be achieved.")
                return

            selected_rule = rules[0]
            rules_used.append(selected_rule)
            self.apply_rule_backward(selected_rule,  rules_used,fact, base )

    def find_rules_for_goal(self, goal):
        rules_for_goal = []
        for rule in self.rule_base:
            _, actions = self.parse_rule(rule)
            
            if goal in actions:
                rules_for_goal.append(rule)
        return rules_for_goal


    def apply_rule_backward(self, rule ,rules_used ,fact, base):
        premises, actions = self.parse_rule(rule)
        fact.append(actions)
        if (premises in self.fact_base) :
            for_rules_used = []
            for i in rules_used :
                r=i.split(':')
                for_rules_used.append(r[0])
            self.print_system_status(fact,for_rules_used[::-1])
        else :
           base.remove(rule)
           self.apply_backward_chaining(premises ,rules_used ,fact, base)


    
############### print results ################

    def print_system_status(self ,fact ,rules_used):
        print(f"New Fact Base: {fact}\n")
        print(f"Rules order :"+ str(rules_used)+"\n")




################ main code ###################
initial_facts= ['pressure is low']
rule_file = 'C:/Users/ayama/OneDrive/Bureau/IC/tp2/rule.txt'  
system = ExpertSystem(rule_file , initial_facts)
goal = 'clouds'
rules_used = []
print("**************************Backward chaining***************************\n")
print(f"the goal is :"+ str(goal)+"\n")
system.apply_backward_chaining(goal ,rules_used ,system.fact_base.copy(), system.rule_base.copy())
rules_used = []
print("***************************forward chaining***************************\n")
system.apply_forward_chaining(rules_used, system.fact_base.copy(), system.rule_base.copy())





