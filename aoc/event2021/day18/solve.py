from itertools import permutations
from math import floor, ceil

########
# PART 1

class SnailfishNumber():
    parent = None
    left = None
    right = None
    value = None


    def __init__(self, list_source = None, parent = None, value = None) -> None:
        self.parent = parent

        if value is not None:
            self.value = value
        elif list_source:
            if isinstance(list_source, str):
                list_source = eval(list_source)

            if isinstance(list_source, list):
                self.left = list_source[0]
                self.right = list_source[1]

                if isinstance(self.left, list):
                    self.left = SnailfishNumber(self.left, self)
                else:
                    self.left = SnailfishNumber(parent = self, value = self.left)
                
                if isinstance(self.right, list):
                    self.right = SnailfishNumber(self.right, self)
                else:
                    self.right = SnailfishNumber(parent = self, value = self.right)

            else:
                raise ValueError("list source must be string or list (" + list_source + ")")


    def __repr__(self) -> str:
        return __class__.__qualname__ + "(" + str(self) + ", "+ str(self.value) + ")"


    def __str__(self) -> str:
        return str(self.value) if self.value is not None else "[" + str(self.left) + "," + str(self.right) + "]"


    def __add_backward__(self, value) -> bool:
        if self.value is not None:
            self.value += value
            return True

        return self.right.__add_backward__(value) or self.left.__add_backward__(value)


    def __add_forward__(self, value) -> bool:
        if self.value is not None:
            self.value += value
            return True

        return self.left.__add_forward__(value) or self.right.__add_forward__(value)


    def __add_left__(self, value) -> bool:
        current = self
        while current.parent is not None:
            if current.parent.left != current:
                return current.parent.left.__add_backward__(value)

            current = current.parent

        return False


    def __add_right__(self, value) -> bool:
        current = self
        while current.parent is not None:
            if current.parent.right != current:
                return current.parent.right.__add_forward__(value)

            current = current.parent

        return False


    def __explode__(self, level = 0) -> bool:
        if level >= 4 and self.value is None:
            value = self.left.value
            self.left = None
            self.__add_left__(value)

            value = self.right.value
            self.right = None
            self.__add_right__(value)

            self.value = 0

            return True
        else:
            if self.value is not None:
                return False

            return self.left.__explode__(level + 1) or self.right.__explode__(level + 1)


    def __split__(self) -> bool:
        if self.value is not None:
            if self.value >= 10:
                self.left = SnailfishNumber(parent = self, value = floor(self.value / 2))
                self.right = SnailfishNumber(parent = self, value = ceil(self.value / 2))
                self.value = None

                return True

            return False
        
        return self.left.__split__() or self.right.__split__()


    def __apply_reduce__(self):
        while self.__explode__() or self.__split__():
            pass

        return self


    def __add__(self, o):
        new_number = SnailfishNumber()
        new_number.left = SnailfishNumber(str(self), new_number)
        new_number.right = SnailfishNumber(str(o), new_number)

        return new_number.__apply_reduce__()
    

    def magnitude(self):
        return self.value if self.value is not None else self.left.magnitude() * 3 + self.right.magnitude() * 2



def read(filename):
    with open("event2021/day18/" + filename, "r") as file:
        return [SnailfishNumber(s.strip()) for s in file.readlines()]


def sumList(lst):
    sum = lst[0]

    for x in lst[1:]:
        sum += x

    return sum


assert str(SnailfishNumber("[1,2]")) == "[1,2]"
assert str(SnailfishNumber("[[1,2],3]")) == "[[1,2],3]"
assert str(SnailfishNumber("[9,[8,7]]")) == "[9,[8,7]]"
assert str(SnailfishNumber("[[1,9],[8,5]]")) == "[[1,9],[8,5]]"
assert str(SnailfishNumber("[[[[1,2],[3,4]],[[5,6],[7,8]]],9]")) == "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]"
assert str(SnailfishNumber("[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]")) == "[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]"
assert str(SnailfishNumber("[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]")) == "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"

# [[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4] (the 9 has no regular number to its left, so it is not added to any regular number).
ex = SnailfishNumber([[[[[9,8],1],2],3],4]); ex.__explode__(); assert str(ex) == "[[[[0,9],2],3],4]"
# [7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]] (the 2 has no regular number to its right, and so it is not added to any regular number).
ex = SnailfishNumber([7,[6,[5,[4,[3,2]]]]]); ex.__explode__(); assert str(ex) == "[7,[6,[5,[7,0]]]]"
# [[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3].
ex = SnailfishNumber([[6,[5,[4,[3,2]]]],1]); ex.__explode__(); assert str(ex) == "[[6,[5,[7,0]]],3]"
# [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action).
ex = SnailfishNumber([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]); ex.__explode__(); assert str(ex) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
# [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]].
ex = SnailfishNumber([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]); ex.__explode__(); assert str(ex) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"

ex = SnailfishNumber([10, 11]); ex.__split__(); ex.__split__(); assert str(ex) == "[[5,5],[5,6]]"

ex = SnailfishNumber([[[[[4,3],4],4],[7,[[8,4],9]]], [1,1]])
# after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
assert str(ex) == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
# after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
ex.__explode__(); assert str(ex) == "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"
# after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
ex.__explode__(); assert str(ex) == "[[[[0,7],4],[15,[0,13]]],[1,1]]"
# after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
ex.__split__(); assert str(ex) == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
# after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
ex.__split__(); assert str(ex) == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
# after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
ex.__explode__(); assert str(ex) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

ex = SnailfishNumber([[[[4,3],4],4],[7,[[8,4],9]]]) + SnailfishNumber([1,1])
assert str(ex) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

assert str(sumList([SnailfishNumber([n + 1, n + 1]) for n in range(4)])) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"
assert str(sumList([SnailfishNumber([n + 1, n + 1]) for n in range(5)])) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"
assert str(sumList([SnailfishNumber([n + 1, n + 1]) for n in range(6)])) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"


assert str(sumList(read("example1.txt"))) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

assert SnailfishNumber([9,1]).magnitude() == 29
assert SnailfishNumber([1,9]).magnitude() == 21
assert SnailfishNumber([[9,1],[1,9]]).magnitude() == 129


# [[1,2],[[3,4],5]] becomes 143.
assert SnailfishNumber([[9,1],[1,9]]).magnitude() == 129
# [[[[0,7],4],[[7,8],[6,0]]],[8,1]] becomes 1384.
assert SnailfishNumber([[[[0,7],4],[[7,8],[6,0]]],[8,1]]).magnitude() == 1384
# [[[[1,1],[2,2]],[3,3]],[4,4]] becomes 445.
assert SnailfishNumber([[[[1,1],[2,2]],[3,3]],[4,4]]).magnitude() == 445
# [[[[3,0],[5,3]],[4,4]],[5,5]] becomes 791.
assert SnailfishNumber([[[[3,0],[5,3]],[4,4]],[5,5]] ).magnitude() == 791
# [[[[5,0],[7,4]],[5,5]],[6,6]] becomes 1137.
assert SnailfishNumber([[[[5,0],[7,4]],[5,5]],[6,6]]).magnitude() == 1137
# [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] becomes 3488.
assert SnailfishNumber([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]).magnitude() == 3488


ex = sumList(read("example2.txt"))
assert str(ex) == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
assert ex.magnitude() == 4140


inp = sumList(read("input.txt"))
answer = inp.magnitude()
print("Part 1 =", answer)
assert answer == 4235 # check with accepted answer


########
# PART 2

def largest_magnitude(inp_list):
    largest = 0
    for a, b in permutations(inp_list, 2):
        if a != b:
            largest = max(largest, (a + b).magnitude())

    return largest


assert largest_magnitude(read("example2.txt")) == 3993

answer = largest_magnitude(read("input.txt"))
print("Part 2 =", answer)
assert answer == 4659 # check with accepted answer
