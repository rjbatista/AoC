from typing import List
from event2019.day13.computer_v4 import Computer_v4
from threading import Thread, Lock

########
# PART 1

class ComputerState:
    def __init__(self, computer, id) -> None:
        self.computer = computer
        self.input_data = []
        self.output_data = []

        if computer:
            self.input_data.append(id)
            self.is_idle = False
        else:
            self.is_idle = True

wanted = None


def input_processor(lock, computer_states : List[ComputerState], id):
    def processor(_):
        global wanted

        if wanted:
            computer_states[id].computer.halt()

        lock.acquire()
        try:
            computer_state = computer_states[id]
            if computer_state.input_data:
                return computer_state.input_data.pop(0)
            else:
                return -1
        finally:
            lock.release()

    return processor


def output_processor(lock, computer_states : List[ComputerState], id):
    def processor(val):
        global wanted

        lock.acquire()
        try:
            computer_state = computer_states[id]

            computer_state.output_data.append(val)

            if len(computer_state.output_data) >= 3:
                dest, x, y = computer_state.output_data.pop(0), computer_state.output_data.pop(0), computer_state.output_data.pop(0)

                if dest == 255:
                    wanted = (x, y)
                else:
                    computer_state = computer_states[dest]
                    computer_state.input_data += [x, y]

            return None
        finally:
            lock.release()

    return processor


def setup_computers(n = 50, input_processor_generator = input_processor, output_processor_generator = output_processor):
    code = Computer_v4.read_code("event2019/day23/input.txt")
    computer_states = { 255: ComputerState(None, 255) }
    lock = Lock()

    threads = []
    print("preparing....")
    for i in range(n):
        computer = Computer_v4(code)
        computer.set_debug(False)
        computer_states[i] = ComputerState(computer, i)
        computer.set_input_processor(input_processor_generator(lock, computer_states, i))
        computer.set_output_processor(output_processor_generator(lock, computer_states, i))
        t = Thread(target=computer.run, daemon=True, args=(None, None))
        threads.append(t)

    print("starting....")
    for t in threads:
        t.start()

    print("waiting....")
    for t in threads:
        t.join()


setup_computers()

answer = wanted[1]
print("Part 1 =", answer)
assert answer == 27182 # check with accepted answer

########
# PART 2


def input_processor_p2(lock, computer_states : List[ComputerState], id):
    def processor(_):
        global wanted

        if wanted and len(wanted) == 2:
            computer_states[id].computer.halt()

        lock.acquire()
        try:
            computer_state = computer_states[id]
            if computer_state.input_data:
                return computer_state.input_data.pop(0)
            else:
                if id == 0 and computer_states[255].input_data:
                    # check for idleness
                    idleness = len([1 for state in computer_states.values() if not state.is_idle]) == 0

                    if idleness:
                        x, y = computer_states[255].input_data
                        computer_state.input_data += [x, y]
                        computer_state.is_idle = False

                        if (wanted and y == wanted[0]):
                            wanted = (y, y)
                        else:
                            wanted = (y,)

                        return computer_state.input_data.pop(0)
                    else:
                        computer_state.is_idle = True
                        return -1
                else:
                    computer_state.is_idle = True
                    return -1
        finally:
            lock.release()

    return processor


def output_processor_p2(lock, computer_states : List[ComputerState], id):
    def processor(val):
        global wanted

        lock.acquire()
        try:
            computer_state = computer_states[id]

            computer_state.output_data.append(val)

            if len(computer_state.output_data) >= 3:
                dest, x, y = computer_state.output_data.pop(0), computer_state.output_data.pop(0), computer_state.output_data.pop(0)

                if dest == 255:
                    computer_states[255].input_data = [x, y]
                else:
                    computer_state = computer_states[dest]
                    computer_state.is_idle = False
                    computer_state.input_data += [x, y]

            return None
        finally:
            lock.release()

    return processor


wanted = None

setup_computers(input_processor_generator=input_processor_p2, output_processor_generator=output_processor_p2)

answer = wanted[1]
print("Part 2 =", answer)
assert answer == 19285 # check with accepted answer
