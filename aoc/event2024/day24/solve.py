""" Advent of code 2024 - day 24 """

from pathlib import Path
import re

########
# PART 1


def read(filename: str) -> tuple[dict[str, int], list[tuple]]:
    """ Read from a file """
    operations = {
        'AND': lambda a, b: a & b,
        'OR': lambda a, b: a | b,
        'XOR': lambda a, b: a ^ b,
    }

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        values = {}
        code = []

        while True:
            line = file.readline().strip()

            if not line:
                break

            var, val = line.split(":")
            values[var] = int(val)

        code_expr = re.compile(r"^(\w+) (AND|OR|XOR) (\w+) -> (\w+)$")
        for line in file:
            op1, op, op2, res = code_expr.match(line).groups()

            code.append((op1, operations[op], op, op2, res))

        return values, code


def get_value(values: dict[str, int], key: str) -> int:
    """ Get the value for the specified key """
    result = [x for x in values.items() if x[0].startswith(key)]
    result = [v for _, v in sorted(result, reverse=True)]

    res = 0
    for bit in result:
        res = (res << 1) + bit

    return res


def run(values: dict[str, int], code: list) -> dict[str, int]:
    """ Run the code and get the result """
    todo = code[:]
    cur_values = dict(values)

    while todo:
        op1, op, oop, op2, res = todo.pop(0)

        if op1 not in cur_values or op2 not in cur_values:
            todo.append((op1, op, oop, op2, res))
            continue

        cur_values[res] = op(cur_values[op1], cur_values[op2])

    return cur_values


ex1 = read("example1.txt")
assert get_value(run(*ex1), "z") == 4

ex2 = read("example2.txt")
assert get_value(run(*ex2), "z") == 2024


inp = read("input.txt")
ANSWER = get_value(run(*inp), "z")
print("Part 1 =", ANSWER)
assert ANSWER == 46362252142374  # check with accepted answer

########
# PART 2


def find_faults(code: list) -> str:
    """
    Find faults based on the ripple carry schematic.
    Find expressions with operations that are not used in the adder,
    as those must be wrong.

    Full adder:
        (Xi XOR Yi) XOR Ci-1 = Zi
        ((Xi XOR Yi) AND Ci-1) OR (Xi AND Yi) = Ci

    So,
        XOR is only used for result or on inputs
        OR can only be of 2 ANDs
        AND cannot be of ANDs
    """
    faults = set()
    ignored = ['x00', 'y00']
    inner_ops = {
        res: op for op1, _, op, op2, res in code if op1 not in ignored and op2 not in ignored
    }
    last = max(res for res in inner_ops.keys() if res.startswith("z"))
    for op1, _, op, op2, res in code:
        # ignore first and last, as they are different
        if res != last and op1 not in ignored and op2 not in ignored:
            is_result = res.startswith("z")

            if op == "XOR":
                # XOR is only used for result or on inputs
                if not is_result and op1[0] not in "xy" and op2[0] not in "xy":
                    faults.add(res)
            else:
                # results can only come from a XOR
                if is_result:
                    faults.add(res)

                elif op == "OR":
                    # OR can ONLY be of ANDs
                    if inner_ops.get(op1, None) != 'AND':
                        faults.add(op1)
                    if inner_ops.get(op2, None) != 'AND':
                        faults.add(op2)
                elif op == "AND":
                    # AND cannot be of ANDs
                    if inner_ops.get(op1, None) == "AND":
                        faults.add(op1)

                    if inner_ops.get(op2, None) == "AND":
                        faults.add(op2)

    return ",".join(sorted(faults))


ANSWER = find_faults(inp[1])
print("Part 2 =", ANSWER)
assert ANSWER == "cbd,gmh,jmq,qrh,rqf,z06,z13,z38"  # check with accepted answer
