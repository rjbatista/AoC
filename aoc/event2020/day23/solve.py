########
# PART 1

def do_round(inp):
    current = inp.pop(0)
    cups, rest = inp[0:3], inp[3:]
    dest = current - 1
    max_list = max(inp)

    while True:
        if dest == 0:
            dest = max_list

        if dest not in cups:
            break

        dest -= 1

    dest_idx = rest.index(dest)

    return rest[:dest_idx + 1] + cups + rest[dest_idx + 1:] + [current]


def get_result_after(inp, moves = 100):
    lst = inp[:]
    for _ in range(moves):
        lst = do_round(lst)

    one = lst.index(1)

    return ''.join(map(str, lst[one + 1:] + lst[:one]))


assert get_result_after(list(map(int, "389125467")), 10) == "92658374"

inp = list(map(int, "315679824")) # the puzzle input
answer = get_result_after(inp)
print("Part 1 =", answer)
assert answer == "72496583"  # check with accepted answer


########
# PART 2

class Node:
    def __init__(self, value, prev = None, next = None):
        self.value = value
        self.prev = prev
        self.next = next


class SearchableLinkedList:
    def __init__(self):
         # since these are all integers, would probably more efficent an array instead of dictionary
         # ...probably even more if instead of a linked list an array containing the "next index" - but this solution works for all cases
        self._all_nodes = {}
        self.head = None
        self._tail = None
        self._closed = False
        self.max_value = 0


    def add(self, value):
        assert not self._closed

        self.max_value = max(self.max_value, value)

        new_node = Node(value, prev = self._tail)
        self._all_nodes[value] = new_node
        
        if not self.head:
            self.head = new_node
        
        if self._tail:
            self._tail.next = new_node

        self._tail = new_node
    

    def close(self):
        self.head.prev = self._tail
        self._tail.next = self.head


    def get_node_with_value(self, value):
        return self._all_nodes[value]


    def move_head_to_value(self, value):
        self.head = self._all_nodes[value]


    def advance(self):
        self.head = self.head.next


def create_cups(initial_cups, total_cups = 1000000):
    linked_list = SearchableLinkedList()

    for cup in initial_cups:
        linked_list.add(cup)

    for cup in range(max(initial_cups) + 1, total_cups + 1):
        linked_list.add(cup)
    
    # circle around
    linked_list.close()

    return linked_list


def do_round_p2(linked_list):
    current_node = linked_list.head
    dest_value = current_node.value - 1

    picked_nodes = [current_node.next, current_node.next.next, current_node.next.next.next]
    cups = [cup.value for cup in picked_nodes]

    while True:
        if dest_value == 0:
            dest_value = linked_list.max_value

        if dest_value not in cups:
            break

        dest_value -= 1

    dest_node = linked_list.get_node_with_value(dest_value)

    # remove nodes from list
    picked_nodes[0].prev.next = picked_nodes[-1].next
    picked_nodes[-1].next.prev = picked_nodes[0].prev
    
    picked_nodes[-1].next = dest_node.next
    dest_node.next.prev = picked_nodes[-1]

    dest_node.next = picked_nodes[0]
    picked_nodes[0].prev = dest_node
    
    linked_list.advance()


def get_result_after_p2(inp, moves = 100):
    linked_list = create_cups(inp)
    for _ in range(moves):
        do_round_p2(linked_list)

    linked_list.move_head_to_value(1)
    
    return linked_list.head.next.value * linked_list.head.next.next.value


answer = get_result_after_p2(inp, 10000000)
print("Part 2 =", answer)
assert answer == 41785843847 # check with accepted answer
