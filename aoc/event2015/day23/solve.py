import re

########
# PART 1

class Cpu:
    def __init__(self, code):
        self.a = 0
        self.b = 0
        self.ip = 0
        self.code = code


    def hlf(self, r):
        '''sets register r to half its current value, then continues with the next instruction.'''
        setattr(self, r, getattr(self, r) // 2)
        self.ip += 1


    def tpl(self, r):
        '''sets register r to triple its current value, then continues with the next instruction.'''
        setattr(self, r, getattr(self, r) * 3)
        self.ip += 1


    def inc(self, r):
        ''' increments register r, adding 1 to it, then continues with the next instruction.'''
        setattr(self, r, getattr(self, r) + 1)
        self.ip += 1


    def jmp(self, offset):
        '''is a jump; it continues with the instruction offset away relative to itself.'''
        self.ip += offset


    def jie(self, r, offset):
        '''is like jmp, but only jumps if register r is even ("jump if even").'''
        if (getattr(self, r) % 2 == 0):
            self.ip += offset
        else:
            self.ip += 1


    def jio(self, r, offset):
        '''is like jmp, but only jumps if register r is 1 ("jump if one", not odd).'''
        if (getattr(self, r) == 1):
            self.ip += offset
        else:
            self.ip += 1


    def run(self):
        regs = { 'a': self.a,
                'b': self.b,
                'hlf': self.hlf,
                'tpl': self.tpl,
                'inc': self.inc,
                'jmp': self.jmp,
                'jie': self.jie,
                'jio': self.jio
        }

        deadlockdet = 0
        lastip = self.ip
        while (self.ip < len(code)):
            exec(self.code[self.ip], regs)

            if (lastip == self.ip):
                deadlockdet += 1
                if (deadlockdet == 2):
                    print("DEADLOCKED!")
                    break
            else:
                lastip = self.ip
                deadlockdet = 0

    def __str__(self):
        return "a=%8d\tb=%8d\tip=%d" % (self.a, self.b, self.ip)

def processline(line):
    line = re.sub(r"(hlf|tpl|inc) (\w+)", r"\1('\2')", line)
    line = re.sub(r"(jmp) ((?:\+?|\-?)\d+)", r"\1(\2)", line)
    line = re.sub(r"(jie|jio) (\w+), ((?:\+?|\-?)\d+)", r"\1('\2', \3)", line)

    return line


def processfile(fn):
    with open(fn) as f:
        code = []
        for line in f:
            line = processline(line)
            code.append(line)

    return code


def example():
    code = []
    code += [processline("inc a")]
    code += [processline("jio a, +2")]
    code += [processline("tpl a")]
    code += [processline("inc a")]

    return code


code = processfile("event2015/day23/input.txt")
cpu = Cpu(code)
cpu.run()
answer = cpu.b
print("Part 1 =", answer)
assert answer == 184 # check with accepted answer

########
# PART 2

code.insert(0, 'inc("a")')
cpu = Cpu(code)
cpu.run()
answer = cpu.b
print("Part 2 =", answer)
assert answer == 231 # check with accepted answer
