import re

########
# PART 1

class Cpu:
    _debug = True
    _step = False

    def __init__(self, code):
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.ip = 0
        self.code = code

    def cpy(self, x, y):
        """ cpy x y copies x (either an integer or the value of a register) into register y. """
        if type(x) == str:
            setattr(self, y, int(getattr(self, x)))
        else:
            setattr(self, y, x)

        self.ip += 1

    def inc(self, r):
        """ inc x increases the value of register x by one. """
        setattr(self, r, getattr(self, r) + 1)
        self.ip += 1

    def dec(self, r):
        """  dec x decreases the value of register x by one. """
        setattr(self, r, getattr(self, r) - 1)
        self.ip += 1

    def jnz(self, r, offset):
        """ jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero. """
        if type(r) == str:
            v = getattr(self, r)
        else:
            v = r

        if type(offset) == str:
            offset = getattr(self, offset)

        if v != 0:
            self.ip += offset
        else:
            self.ip += 1

    def tgl_and_advance(self, r):
        self.tgl(r)
        self.ip += 1

    def tgl(self, r):
        if type(r) == str:
            v = getattr(self, r)
        else:
            v = r

        if self.ip < 0 or self.ip + v >= len(self.code):
            return

        instr = self.code[self.ip + v]
        self.code[self.ip + v] = '_' + instr if instr[0] != '_' else instr[1:]

    def mul(self, x, y, r):
        """ multiply x*y and put on r. """
        if type(x) == str:
            vx = getattr(self, x)
        else:
            vx = x

        if type(y) == str:
            vy = getattr(self, y)
        else:
            vy = y

        setattr(self, r, vx*vy)

        self.ip += 1

    def nop(self):
        self.ip += 1

    def run(self):
        regs = {'a': self.a,
                'b': self.b,
                'c': self.c,
                'd': self.d,
                'cpy': self.cpy,
                'inc': self.inc,
                'dec': self.dec,
                'jnz': self.jnz,
                'tgl': self.tgl_and_advance,

                # toggled
                '_inc': self.dec,
                '_dec': self.inc,
                '_tgl': self.inc,
                '_cpy': self.jnz,
                '_jnz': self.cpy,

                # extra
                'mul': self.mul,
                'nop': self.nop,
                }

        deadlock_det = 0
        last_ip = self.ip
        while self.ip < len(self.code):
            if Cpu._debug: print(self)
            if Cpu._debug: print(self.code[self.ip])
            if Cpu._step: input("...")
            exec(self.code[self.ip], regs)

            if last_ip == self.ip:
                deadlock_det += 1
                if deadlock_det == 2:
                    print("DEADLOCKED!")
                    break
            else:
                last_ip = self.ip
                deadlock_det = 0

    def __str__(self):
        return "a=%8d\tb=%8d\tc=%8d\td=%8d\tip=%d" % (self.a, self.b, self.c, self.d, self.ip)


def process_line(line):
    line = re.sub(r"(inc|dec) ([a-d])", r"\1('\2')", line)
    line = re.sub(r"(cpy|jnz) ((?:\+?|-?)\d+) ((?:\+?|-?)\d+)", r"\1(\2, \3)", line)
    line = re.sub(r"(cpy|jnz) ((?:\+?|-?)\d+) ([a-d])", r"\1(\2, '\3')", line)
    line = re.sub(r"(jnz) ([a-d]) ((?:\+?|-?)\d+)", r"\1('\2', \3)", line)
    line = re.sub(r"(cpy|jnz) ([a-d]) ([a-d])", r"\1('\2', '\3')", line)
    line = re.sub(r"(tgl) ((?:\+?|-?)\d+)", r"\1(\2)", line)
    line = re.sub(r"(tgl) ([a-d])", r"\1('\2')", line)

    line = re.sub(r"(mul) ([a-d]) ([a-d]) ([a-d])", r"\1('\2', '\3', '\4')", line)
    line = re.sub(r"(mul) ((?:\+?|-?)\d+) ([a-d]) ([a-d])", r"\1(\2, '\3', '\4')", line)
    line = re.sub(r"(mul) ([a-d]) ((?:\+?|-?)\d+) ([a-d])", r"\1('\2', \3, '\4')", line)
    line = re.sub(r"(mul) ((?:\+?|-?)\d+) ((?:\+?|-?)\d+) ([a-d])", r"\1(\2, \3, '\4')", line)
    line = re.sub(r"(nop)", r"\1()", line)

    return line if line[-1] != '\n' else line[:-1]


def process_file(fn):
    f = open(fn)
    code = []
    for line in f:
        line = process_line(line)
        code += [line]

    return code


def example():
    code = []

    code += [process_line("cpy 2 a")]
    code += [process_line("tgl a")]
    code += [process_line("tgl a")]
    code += [process_line("tgl a")]
    code += [process_line("cpy 1 a")]
    code += [process_line("dec a")]
    code += [process_line("dec a")]

    return code


#cpu = Cpu(example())
#cpu.run()
#print(cpu.a, cpu.b, cpu.c, cpu.d)

code = process_file("event2016/day23/input_with_mul.txt")
cpu = Cpu(code)
cpu.a = 7
Cpu._debug = False
cpu.run()
#print(cpu.a, cpu.b, cpu.c, cpu.d)

answer = cpu.a
print("Part 1 =", answer)
assert answer == 10152 # check with accepted answer

########
# PART 2


code = process_file("event2016/day23/input_with_mul.txt")
cpu = Cpu(code)
cpu.a = 12
Cpu._debug = False
cpu.run()
#print(cpu.a, cpu.b, cpu.c, cpu.d)

answer = cpu.a
print("Part 2 =", answer)
assert answer == 479006712 # check with accepted answer
