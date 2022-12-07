""" Advent of code 2017 - day 18 """
from pathlib import Path
from event2017.day18.computer import Computer

########
# PART 1

ex1 = Computer()
ex1.load(Path(__file__).parent.joinpath("example1.txt"))
assert ex1.run() == 4


inp = Computer()
inp.load(Path(__file__).parent.joinpath("input.txt"))
answer = inp.run()
print("Part 1 =", answer)
assert answer == 8600 # check with accepted answer

########
# PART 2

class Computer_v2(Computer):
    """ Extension for part 2 """
    def __init__(self, program_id):
        super().__init__()

        self._program_id = program_id
        self._registers['p'] = program_id

        self.send_count = 0
        self.attached = None
        self._queue = []
        self.paused = False

    def attach(self, another: 'Computer_v2'):
        """ Attaches the computer to another """
        self.attached = another

        if another.attached is None:
            another.attach(self)
            another.code = self.code
            another.paused = True

    def receive(self, value):
        """ receive a value from another """
        self._queue.append(value)

        if self.paused:
            self._ip -= 1
            self.paused = False
            self._resume()

    def opcode_snd(self, arg0):
        """
        snd X sends the value of X to the other program.
        These values wait in a queue until that program is ready to receive them.
        Each program has its own message queue, so a program can never receive a message it sent.
        """
        assert self.attached

        self.send_count += 1

        if not isinstance(arg0, int):
            arg0 = self._registers[arg0]

        self.attached.receive(arg0)

    def opcode_rcv(self, reg):
        """
        rcv X receives the next value and stores it in register X.
        If no values are in the queue, the program waits for a value to be sent to it.
        Programs do not continue to the next instruction until they have received a value.
        Values are received in the order they are sent.
        """
        if len(self._queue) == 0:
            self.paused = True

            return True

        self._registers[reg] = self._queue.pop(0)

        return False


ex1 = (Computer_v2(0), Computer_v2(1))
ex1[0].load(Path(__file__).parent.joinpath("example2.txt"))
ex1[0].attach(ex1[1])
ex1[0].run()

assert ex1[0].paused
assert ex1[1].paused

assert ex1[1].send_count == 3

inp = (Computer_v2(0), Computer_v2(1))
inp[0].load(Path(__file__).parent.joinpath("input.txt"))
inp[0].attach(inp[1])

inp[0].run()

answer = inp[1].send_count
print("Part 2 =", answer)
assert answer == 7239 # check with accepted answer
