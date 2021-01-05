from time import sleep
from event2019.day13.computer_v4 import Computer_v4
from queue import Queue
from threading import Thread

########
# PART 1

computer = Computer_v4()
computer.load_code("event2019/day13/input.txt")
computer.run()
output = computer.get_output()
screen = {(x, y): t for x, y, t in (zip(*(iter(output),) * 3))}

answer = len({p: t for p, t in screen.items() if t == 2}.keys())
print("Part 1 =", answer)
assert answer == 335 # check with accepted answer

########
# PART 2

def print_screen(screen):
    w, h = 0, 0
    for x, y in screen.keys():
        w = max(w, x)
        h = max(h, y)

    for y in range(h + 1):
        for x in range(w + 1):
            c = screen.get((x, y), 0)
            if (c == 1):
                print(end="█")
            elif (c == 2):
                print(end="░")
            elif (c == 3):
                print(end="_")
            elif (c == 4):
                print(end="∙")
            else:
                print(end=" ")
        print()

    print("Score = ", screen.get((-1, 0), 0))

#print_screen(screen)
screen = {}

def get_player_processor():
    def input_player(input_func):
        ball_x = [x for (x, _), t in screen.items() if t == 4][0]
        paddle_x = [x for (x, _), t in screen.items() if t == 3][0]

        if paddle_x < ball_x:
            return 1
        elif paddle_x > ball_x:
            return -1
        else:
            return 0

    return input_player

def get_update_screen_processor():
    current_command = []
    def update_screen(val):
        current_command.append(val)

        if (len(current_command) == 3):
            screen[(current_command[0], current_command[1])] = current_command[2]
            current_command.clear()

    return update_screen

# setup the brain on a different thread
computer = Computer_v4()
computer.load_code("event2019/day13/input.txt")
computer.set_memory_value(0, 2)
computer_in = Queue()
computer_out = Queue()
computer.set_input_processor(get_player_processor())
computer.set_output_processor(get_update_screen_processor())
t = Thread(target=computer.run, daemon=True, args=(computer_in, computer_out))
t.start()

print("Running")

# wait to complete
t.join()

# get the score
answer = screen[(-1, 0)]
print("Part 2 =", answer)
assert answer == 15706 # check with accepted answer

#print_screen(screen)
