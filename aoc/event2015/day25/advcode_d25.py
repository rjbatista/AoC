########
# PART 1

# on python 3.7+ can just call pow(base, exp, mod), no need to implement anything!
def modexp(base, exp, mod):
    ''' mod exp by repeated squaring '''
    res = 1
    cur = base
    while (exp > 0):
        if (exp % 2 == 1):
            res = (res * cur) % mod

        exp = exp >> 1
        cur = (cur * cur) % mod

    return res


# To continue, please consult the code grid in the manual.  Enter the code at row 2981, column 3075.
row, col = (2981, 3075)

firstcode = 20151125
base = 252533
mod = 33554393
diag = row + col - 1

exp = diag * (diag - 1) // 2 + col - 1

answer = modexp(base, exp, mod) * firstcode % mod
print("Part 1 =", answer)
assert answer == 9132360 # check with accepted answer
