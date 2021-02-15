import re

########
# PART 1

_debug = False

class Output:
    def __init__(self, id):
        self._id = id
        self._value = None

    def add_value(self, value):
        if _debug: print("output", self._id, "got value", value)
        self._value = value

    def get_value(self):
        return self._value


class Bot:
    """ Class for a bot """
    def __init__(self, id):
        self.id = id
        self._high = None
        self._low = None
        self._values = []
        self.tested_part1_conditions = False

    def run_cycle(self):
        if len(self._values) < 2:
            return 0
        else:
            # run
            self._values.sort()

            # part 1
            if (self._values == [17,61]):
                self.tested_part1_conditions = True

            self._low.add_value(self._values[0])
            self._high.add_value(self._values[1])

            self._values = self._values[2:]

            return 1

    def add_value(self, value):
        if _debug: print("bot", self.id, "got value", value)
        self._values += [ value ]

    def low_receiver(self, low):
        self._low = low

    def high_receiver(self, high):
        self._high = high


def read_input():
    with open("event2016/day10/input.txt") as f:
        ret = []
        for line in f:
            ret += [ line[:-1] if line[-1] == '\n' else line ]

    return ret


def run_code(lines, nBots = 100, nOutputs = 100):
    pvalue = re.compile(r'value (\d+) goes to bot (\d+)')
    ptransfer = re.compile(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')

    bots = [Bot(i) for i in range(nBots)]
    outputs = [Output(i) for i in range(nOutputs)]

    for line in lines:
        m = re.match(pvalue, line)
        if m:
            value = int(m.group(1))
            bot = int(m.group(2))

            bots[bot].add_value(value)
        else:
            m = re.match(ptransfer, line)
            if m:
                bot = int(m.group(1))

                low_recv = m.group(2)
                low_id = int(m.group(3))
                high_recv = m.group(4)
                high_id = int(m.group(5))

                low = bots[low_id] if low_recv == 'bot' else outputs[low_id]
                high = bots[high_id] if high_recv == 'bot' else outputs[high_id]

                bots[bot].low_receiver(low)
                bots[bot].high_receiver(high)
            else:
                raise NotImplementedError(line)

    # bots run
    done = False
    while not done:
        done = True
        for bot in bots:
            if (bot.run_cycle() == 1):
                done = False

    return bots, outputs


bots, outputs = run_code(['value 5 goes to bot 2',
'bot 2 gives low to bot 1 and high to bot 0',
'value 3 goes to bot 1',
'bot 1 gives low to output 1 and high to bot 0',
'bot 0 gives low to output 2 and high to output 0',
'value 2 goes to bot 2'])

# In the end, output bin 0 contains a value-5 microchip,
assert outputs[0].get_value() == 5
# output bin 1 contains a value-2 microchip,
assert outputs[1].get_value() == 2
# and output bin 2 contains a value-3 microchip.
assert outputs[2].get_value() == 3
# In this configuration, bot number 2 is responsible for comparing value-5 microchips with value-2 microchips.

#print("part 1! bot ", self._id, " tested 17,61")


bots, outputs = run_code(read_input(), 500, 500)

answer = [bot.id for bot in bots if bot.tested_part1_conditions]
print("Part 1 =", answer)
assert answer == [47] # check with accepted answer

########
# PART 2

answer = outputs[0].get_value() * outputs[1].get_value() * outputs[2].get_value()
print("Part 2 =", answer)
assert answer == 2666 # check with accepted answer
