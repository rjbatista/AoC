""" Advent of code 2023 - day 20 """
from abc import abstractmethod
from dataclasses import dataclass, field
from math import lcm
from pathlib import Path
import re
from typing import Self

########
# PART 1


@dataclass
class Module:
    """ Base module """
    name: str
    destination: list[str]
    inputs: list[str] = None

    def register_inputs(self, inputs: list[str]):
        """ Register the inputs """
        self.inputs = inputs

    @abstractmethod
    def fire(self, source: str, low: bool) -> list[tuple[str, bool]]:
        """ Fire a pulse """

    @abstractmethod
    def reset(self) -> None:
        """ Reset the module """


@dataclass
class Output(Module):
    """ Output module """

    def fire(self, source: str, low: bool) -> list[tuple[str, bool]]:
        return []

    def reset(self) -> None:
        pass


@dataclass
class Broadcaster(Module):
    """ Broadcaster module """

    def fire(self, source: str, low: bool) -> list[tuple[str, bool]]:
        """ Fire a pulse and return the generated pulses """
        return ((dest, low) for dest in self.destination)

    def register_inputs(self, inputs: list[str]):
        """ Register the inputs """
        self.destination = inputs

    def reset(self) -> None:
        pass


@dataclass
class FlipFlop(Module):
    """ Flip-flop module """
    _status: bool = False

    def fire(self, source: str, low: bool) -> list[tuple[str, bool]]:
        if low:
            self._status = not self._status
            return ((dest, not self._status) for dest in self.destination)

        return []

    def reset(self) -> None:
        self._status = False


@dataclass
class Conjunction(Module):
    """ Conjunction module """
    _inputs_low: dict[str, bool] = field(default_factory=dict)
    fired_high: bool = False

    def register_inputs(self, inputs: list[str]):
        """ Register the inputs """
        super().register_inputs(inputs)

        for module_input in inputs:
            self._inputs_low[module_input] = True

    def fire(self, source: str, low: bool) -> list[tuple[str, bool]]:
        self._inputs_low[source] = low

        all_high = True
        for input_low in self._inputs_low.values():
            if input_low:
                all_high = False
                break

        if not all_high:
            self.fired_high = True

        return ((dest, all_high) for dest in self.destination)

    def reset(self) -> None:
        self._inputs_low = {}


@dataclass
class ModuleSystem:
    """ The module system """
    modules: dict[str, Module] = field(default_factory=dict)
    low_pulses: int = 0
    high_pulses: int = 0
    _todo: list[bool] = field(default_factory=list)
    debug: bool = False

    def press_button(self):
        """ Press the button """
        self._send_pulse('button', 'broadcaster', True)
        self._stabilize()

    def _send_pulse(self, src: str, dest: str, low: bool) -> None:
        """ Sends a pulse in the system """
        self._todo.append((src, dest, low))

    def _stabilize(self):
        """ Resolve pending pulses until the system is stabilized """
        while self._todo:
            src, dest, low = self._todo.pop(0)

            if self.debug:
                print(f"{src} -{"low" if low else "high"}-> {dest}")

            self._register_pulse(low)
            if dest in self.modules:
                new_pulses = self.modules[dest].fire(src, low)
                self._todo += ((dest, new_dest, new_low) for new_dest, new_low in new_pulses)

    def _register_module(self, module: Module) -> None:
        """ Register a module on the system """
        self.modules[module.name] = module

    def _register_pulse(self, low: bool):
        """ Registers a pulse """
        if low:
            self.low_pulses += 1
        else:
            self.high_pulses += 1

    def read(self, filename: str) -> Self:
        """ Read the system from a file """

        with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
            module_expr = re.compile(r'^([%&])?(\w+) -> (.*)$')
            inputs = {}
            for line in file:
                match = module_expr.match(line)
                if match:
                    module_type, name, dests = match.groups()
                    dests = dests.split(', ')

                    for dest in dests:
                        inputs[dest] = inputs.get(dest, set())
                        inputs[dest].add(name)

                    if module_type == '%':
                        self._register_module(FlipFlop(name, dests))
                    elif module_type == '&':
                        self._register_module(Conjunction(name, dests))
                    else:
                        self._register_module(Broadcaster(name, dests))
                else:
                    raise RuntimeError("Invalid input")

            for name, module_inputs in inputs.items():
                if name in self.modules:
                    self.modules[name].register_inputs(module_inputs)
                else:
                    module = Output(name, None)
                    self._register_module(module)
                    module.register_inputs(module_inputs)

        return self


ex1 = ModuleSystem().read("example1.txt")
ex1.press_button()
assert ex1.low_pulses, ex1.high_pulses == (4, 8)
for _ in range(999):
    ex1.press_button()
assert ex1.low_pulses * ex1.high_pulses == 32000000

ex2 = ModuleSystem().read("example2.txt")
for _ in range(1000):
    ex2.press_button()
assert ex2.low_pulses * ex2.high_pulses == 11687500

inp = ModuleSystem().read("input.txt")
for i in range(1000):
    inp.press_button()
ANSWER = inp.low_pulses * inp.high_pulses
print("Part 1 =", ANSWER)
assert ANSWER == 886347020  # check with accepted answer

########
# PART 2


def count_clicks(system: ModuleSystem, node: str):
    """ Find the clicks for the specific node """
    module = system.modules[node]

    relevant_inputs = list(module.inputs)

    if len(relevant_inputs) == 1 and isinstance(system.modules[relevant_inputs[0]], Conjunction):
        #  while there is only dependency and it's a conjuction, focus on that
        return count_clicks(system, relevant_inputs[0])

    count = 0
    counts = []
    while relevant_inputs:
        system.press_button()
        count += 1

        # gather the minimum number of clicks for each of the relevant parts of the conjuction
        for relevant_input in relevant_inputs:
            if system.modules[relevant_input].fired_high:
                relevant_inputs.remove(relevant_input)
                counts.append(count)

    # the minimum number of clicks is the least common multiple between the parts
    return lcm(*counts)


ANSWER = count_clicks(ModuleSystem().read("input.txt"), 'rx')
print("Part 2 =", ANSWER)
assert ANSWER == 233283622908263  # check with accepted answer
