import re
import heapq
from itertools import permutations

########
# PART 1

def read(fn):
    with open("event2020/day21/" + fn, "r") as file:
        pattern = re.compile(r"((?:\w+ ?)+) \(contains ((?:\w+(?:, )?)+)\)")

        all_allegerns = {}
        ingredients_count = {}
        for line in file:
            m = pattern.match(line)

            if m:
                ingredients = m.group(1).split(' ')
                allegerns = m.group(2).split(', ')

                for ingredient in ingredients:
                    ingredients_count[ingredient] = ingredients_count.get(ingredient, 0) + 1

                for allegern in allegerns:
                    if allegern in all_allegerns:
                        current_allegerns = all_allegerns[allegern]
                        all_allegerns[allegern] = [x for x in current_allegerns if x in ingredients]
                    else:
                        all_allegerns[allegern] = ingredients
            else:
                raise RuntimeError("invalid input " + line)
    
    return all_allegerns, ingredients_count


def count_ingredients_without_allergens(all_allegerns, ingredients_count):
    all_ingredients_with_allergens = {ingredient for ingredients in all_allegerns.values() for ingredient in ingredients}

    return sum([count for ingredient, count in ingredients_count.items() if ingredient not in all_ingredients_with_allergens])


assert count_ingredients_without_allergens(*read("example1.txt")) == 5

all_allegerns, ingredients_count = read("input.txt")
answer = count_ingredients_without_allergens(all_allegerns, ingredients_count)
print("Part 1 =", answer)
assert answer == 1930 # check with accepted answer

########
# PART 2
class Node():
    """
    node for the search tree
    """
    def __init__(self, remaining, decided):
        self.remaining = remaining
        self.decided = decided
        

    def __lt__(self, other):
        return len(self.remaining) < len(other.remaining)


def get_dangerous_list(all_allegerns):
    todo = []
    heapq.heappush(todo, Node(list(all_allegerns.items()), {}))
    while todo:
        node = heapq.heappop(todo)

        if not node.remaining:
            return node.decided

        next_alergen, possibilities = node.remaining[0]
        rest = node.remaining[1:]

        for possibility in possibilities:
            if (possibility not in node.decided):
                heapq.heappush(todo, Node(rest, {**node.decided, possibility: next_alergen }))


def canonical(dangerous_list):
    return ','.join([x for x,y in sorted(dangerous_list.items(), key = lambda x : x[1])])


assert canonical(get_dangerous_list(read("example1.txt")[0])) == "mxmxvkd,sqjhc,fvjkl"

answer = canonical(get_dangerous_list(all_allegerns))
print("Part 2 =", answer)
assert answer == "spcqmzfg,rpf,dzqlq,pflk,bltrbvz,xbdh,spql,bltzkxx" # check with accepted answer
