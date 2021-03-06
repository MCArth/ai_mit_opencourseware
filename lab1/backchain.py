from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables, RuleExpression
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    statements = [hypothesis]
    for rule in rules:
        data_match = None
        for con in rule.consequent():
            data_match = match(con, hypothesis)
            if data_match != None:
                break
        if data_match != None:
            antecedent = rule.antecedent()
            if isinstance(antecedent, RuleExpression):
                for i in range(len(antecedent)):
                    antecedent[i] = populate(antecedent[i], data_match)
                    antecedent[i] = backchain_to_goal_tree(rules, antecedent[i])
            else:
                antecedent = populate(antecedent, data_match)
                antecedent = backchain_to_goal_tree(rules, antecedent)
            statements.append(antecedent)
    return simplify(OR(statements))

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
#print(ZOOKEEPER_RULES)
