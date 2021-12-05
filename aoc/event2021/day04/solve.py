########
# PART 1

class Colors:
    CHOSEN = '\033[92m'
    RESET = '\033[0m'


def read(filename):
    with open("event2021/day04/" + filename, "r") as file:
        # draw numbers
        numbers = [int(x) for x in file.readline().strip().split(",")]
        
        file.readline() # skip line
        
        # boards
        boards = []

        line = file.readline()
        while (line):
            board = []
            for _ in range(5):
                board += [[(int(x), False) for x in line.strip().split()]]
                line = file.readline()
            boards += [board]

            line = file.readline()

    return numbers, boards


def check_board(number, board):
    for row_num, row in enumerate(board):
        for col_num, column in enumerate(row):
            if column[0] == number:
                board[row_num][col_num] = number, True
                
                # check if row is done
                winning_row = True
                winning_column = True
                for p in range(5):
                    winning_row &= board[p][col_num][1]
                    winning_column &= row[p][1]

                    if (not winning_column) and (not winning_row):
                        return False
                
                return True

                
def play(numbers, boards, print_winner = False):
    for number in numbers:
        for board in boards:
            if check_board(number, board):
                if print_winner:
                    print("winner with", number, "on board:")
                    draw_board(board)

                return sum([column for row in board for column, state in row if not state]) * number

    raise AssertionError("must be a winner!")


def draw_board(board):
    for line in board:
        for column, state in line:
            if state:
                print(Colors.CHOSEN, end="")
            print("%3d" % column, end="")
            if state:
                print(Colors.RESET, end="")
        print()
    print()


def draw_boards(boards):
    for board in boards:
        draw_board(board)


ex1_numbers, ex1_boards = read("example1.txt")
assert play(ex1_numbers, ex1_boards) == 4512

inp_numbers, inp_boards = read("input.txt")
answer = play(inp_numbers, inp_boards)
print("Part 1 =", answer)
assert answer == 41503 # check with accepted answer


########
# PART 2

def play_to_lose(numbers, boards, print_winner = False):
    winners = set()
    for number in numbers:
        for index, board in enumerate(boards):
            if index not in winners:
                if check_board(number, board):
                    if print_winner:
                        print("winner with", number, "on board:")
                        draw_board(board)

                    winners.add(index)

                    if (len(winners) == len(boards)):
                        return sum([column for row in board for column, state in row if not state]) * number
    
    raise AssertionError("must be a winner!")


assert play_to_lose(ex1_numbers, ex1_boards) == 1924


answer = play_to_lose(inp_numbers, inp_boards)
print("Part 2 =", answer)
assert answer == 3178 # check with accepted answer
