import re

########
# PART 1

class Cpu:
    _debug = True
    _step = False
    _dump_output = False

    def __init__(self, code):
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.ip = 0
        self.code = code
        self.output = []
        self._assert_out = None

    def assert_out(self, lst):
        self._assert_out = lst

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
        """
        jnz x y jumps to an instruction y away (positive means forward;
        negative means backward), but only if x is not zero.
        """
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

        print("mul", x, y, r, vx*vy)

        setattr(self, r, vx*vy)

        self.ip += 1

    def nop(self):
        self.ip += 1

    def out(self, r):
        """ transmits x (either an integer or the value of a register) as the next value for the clock signal. """
        if type(r) == str:
            v = getattr(self, r)
        else:
            v = r

        self.output += [v]

        if self._dump_output:
            print(v)

        if self._assert_out and self.output != self._assert_out[:len(self.output)]:
            raise AssertionError("expected %s got %s" % (self._assert_out, self.output))

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
                'out': self.out,

                # toggled
                '_inc': self.dec,
                '_dec': self.inc,
                '_tgl': self.inc,
                '_cpy': self.jnz,
                '_jnz': self.cpy,

                # extra
                'mul': self.mul,
                'nop': self.nop
                }

        deadlock_det = 0
        last_ip = self.ip
        while self.ip < len(self.code):
            if Cpu._debug: print(self)
            # if Cpu._debug: print("code=", self.code)
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

            if self._assert_out == self.output:
                print("got assertion")
                break

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

    line = re.sub(r"(out) ([a-d])", r"\1('\2')", line)
    line = re.sub(r"(out) ((?:\+?|-?)\d+)", r"\1(\2)", line)

    return line if line[-1] != '\n' else line[:-1]


def process_file(fn):
    f = open(fn)
    code = []
    for line in f:
        line = process_line(line)
        code += [line]

    return code


code = process_file("event2016/day25/input.txt")

Cpu._debug = False

#cpu = Cpu(code)
#Cpu._dump_output = True
#cpu.a = 4
#cpu.run()

a = 0
while True:
    cpu = Cpu(code)
    cpu.assert_out([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    print("\rtrying", a, end="")
    cpu.a = a

    try:
        cpu.run()
        print()
    except AssertionError:
        a += 1
        continue

    break

answer = a
print("Part 1 =", answer)
assert answer == 196 # check with accepted answer
