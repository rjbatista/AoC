import re
from functools import reduce

########
# PART 1

def read_file(fn):
    with open("event2020/day16/" + fn) as file:
        pattern = re.compile(r"^([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)$")

        # read rules
        rules = {}
        for line in file:
            if line == '\n':
                break

            m = pattern.match(line)
            if m:
                rules[m.group(1)] = tuple(zip(*(iter(map(int, m.groups()[1:])),) * 2))
            else:
                raise RuntimeError("invalid input")

        # read my ticket
        file.readline()
        ticket = list(map(int, file.readline()[:-1].split(',')))
        file.readline()

        # read nearby tickets
        file.readline()
        nearby = []
        for line in file:
            nearby.append(list(map(int, line[:-1].split(','))))
    
        return rules, ticket, nearby


def is_valid_field(rules, value):
    for _, ((min_a, max_a), (min_b, max_b)) in rules.items():
        if min_a <= value <= max_a or min_b <= value <= max_b:
            return True
    
    return False


def is_valid_ticket(rules, ticket):
    for value in ticket:
        if not is_valid_field(rules, value):
            return False

    return True

def get_ticket_scanning_error_rate(rules, tickets):
    return sum([value for ticket in tickets for value in ticket if not is_valid_field(rules, value)])

    
rules, _, nearby = read_file("example1.txt")
assert get_ticket_scanning_error_rate(rules, nearby) == 71

rules, ticket, nearby = read_file("input.txt")
answer = get_ticket_scanning_error_rate(rules, nearby)
print("Part 1 =", answer)
assert answer == 32835


########
# PART 2

def get_order(rules, ticket, nearby):
    valid_tickets = [ticket for ticket in nearby if is_valid_ticket(rules, ticket)] + [ticket]

    impossible_indexes = {}
    for ticket in valid_tickets:
        for idx, value in enumerate(ticket):
            for name, ((min_a, max_a), (min_b, max_b)) in rules.items():
                impossible = impossible_indexes.get(name, [])
                
                if not (min_a <= value <= max_a or min_b <= value <= max_b):
                        impossible += [idx]

                impossible_indexes[name] = impossible

    possible_indexes = []
    for idx in range(len(ticket)):
        valid_rules = set()
        for rule in rules.keys():
            if idx not in impossible_indexes[rule]:
                valid_rules.add(rule)

        possible_indexes.append(valid_rules)

    def get_next_position(used, possible_indexes):
        if possible_indexes:
            for possibility in possible_indexes[0]:
                if possibility not in used:
                    attempt = [possibility] + get_next_position(used + [possibility], possible_indexes[1:])

                    if len(attempt) == len(possible_indexes):
                        return attempt
        
        return []

    return get_next_position([], possible_indexes)


orders = get_order(*read_file("input.txt"))
ticket_name_value = [(rule_name, ticket[idx]) for idx, rule_name in enumerate(orders) if rule_name.startswith("departure")]
answer = reduce(lambda x, y : x * y, [value for _, value in ticket_name_value])
print("Part 2 =", answer)
assert answer == 514662805187