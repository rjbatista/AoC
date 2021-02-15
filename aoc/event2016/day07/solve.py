import re

########
# PART 1

def read_input():
    f = open("event2016/day07/input.txt")

    ret = []
    for line in f:
        ret += [ line[:-1] if line[-1] == '\n' else line ]

    f.close()

    return ret


def find_abba(addr_part):
    m = re.search(r'(\w)(?!\1)(\w)\2\1', addr_part)

    return m is not None


def parse_addr(addr_str):
    hypernets = re.findall(r'\[(\w*)\]', addr_str)
    nets = re.sub(r'\[(\w*)\]', ',', addr_str).split(',')

    return hypernets, nets


def supports_tls(addr_str):
    addr = parse_addr(addr_str)

    for hypernet in addr[0]:
        if find_abba(hypernet):
            return False

    for net in addr[1]:
        if find_abba(net):
            return True

    return False


def p1_solve_for(input):
    count = 0
    for addr in input:
        supports = supports_tls(addr)

        count += 1 if supports else 0

    return count


# abba[mnop]qrst supports TLS (abba outside square brackets).
assert supports_tls('abba[mnop]qrst') == True
# abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
assert supports_tls('abcd[bddb]xyyx') == False
# aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
assert supports_tls('aaaa[qwer]tyui') == False
# ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).
assert supports_tls('ioxxoj[asdfgh]zxcvbn') == True

assert p1_solve_for(['abba[mnop]qrst', 'abcd[bddb]xyyx', 'aaaa[qwer]tyui', 'ioxxoj[asdfgh]zxcvbn']) == 2

answer = p1_solve_for(read_input())
print("Part 1 =", answer)
assert answer == 110 # check with accepted answer

########
# PART 2

# part 2
def find_aba(net, hypernets):
    all = re.findall(r'(?=(\w)(?!\1)(\w)\1)', net)

    for each in all:
        aba = each[1] + each[0] + each[1]

        for hypernet in hypernets:
            if aba in hypernet:
                return True

    return False


def supports_ssl(addr_str):
    addr = parse_addr(addr_str)

    hypernets = addr[0]
    for net in addr[1]:
        if find_aba(net, hypernets):
            return True

    return False


def p2_solve_for(input):
    count = 0
    for addr in input:
        supports = supports_ssl(addr)

        count += 1 if supports else 0

    return count

# aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
assert supports_ssl('aba[bab]xyz') == True
# xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
assert supports_ssl('xyx[xyx]xyx') == False
# aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because the interior character must be different).
assert supports_ssl('aaa[kek]eke') == True
# zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz overlap).
assert supports_ssl('zazbz[bzb]cdb') == True

answer = p2_solve_for(read_input())
print("Part 2 =", answer)
assert answer == 242 # check with accepted answer
