""" Advent of code 2022 - day 07 """
from pathlib import Path

########
# PART 1

class FilesystemNode:
    """ A Filesystem node """
    def __init__(self, name, parent = None, size = None) -> None:
        self._name = name
        self._parent = parent
        self._size = size
        self.is_directory = size is None
        self._children = {}

    def add(self, dir_name, size = None) -> None:
        """ Add a directory entry """
        self._children[dir_name] = FilesystemNode(dir_name, self, size)

    def change_dir(self, dir_name) -> 'FilesystemNode':
        """ Change a child directory """
        return self._children[dir_name]

    def dir_up(self) -> 'FilesystemNode':
        """ Change to parent directory """
        return self._parent

    def size(self):
        """ Return the size of the node (including children) """
        total_size = 0
        if self._size is None:
            for child in self._children.values():
                total_size += child.size()

            self._size = total_size

        return self._size

    def find_dirs_at_most(self, at_most = 100000) -> list('Node'):
        """ Return the list of directories matching the criteria  """
        matches = []

        if self._size <= at_most:
            matches.append(self)

        for child in self._children.values():
            if child.is_directory:
                matches += child.find_dirs_at_most(at_most)

        return matches

    def get_dirs(self, at_least):
        """ return directories with at least some size """
        dirs = []

        if self._size < at_least:
            return dirs

        if self.is_directory:
            dirs.append(self)

        for child in self._children.values():
            dirs += child.get_dirs(at_least)

        return dirs

    def __str__(self) -> str:
        return str(self._parent) + '/' + self._name if self._parent else ''

    def __repr__(self) -> str:
        return f"{self} ({self._size})"

    @staticmethod
    def read(filename) -> 'FilesystemNode':
        """ Read commands from a shell and interpret the output """
        root_node = FilesystemNode('')

        with Path(__file__).parent.joinpath(filename).open("r") as file:
            current_node = root_node
            for line in file.readlines():
                line = line.strip()

                if line.startswith('$ cd'):
                    curdir = line[5:]

                    if curdir == '/':
                        current_node = root_node
                    elif curdir == '..':
                        current_node = current_node.dir_up()
                    else:
                        current_node = current_node.change_dir(curdir)

                elif line == '$ ls':
                    pass
                else:
                    entry = line.split(' ')

                    # add entry to current directory
                    current_node.add(entry[1], size = int(entry[0]) if entry[0] != 'dir' else None)

        # calc sizes
        root_node.size()

        return root_node


ex1 = FilesystemNode.read('example1.txt')
assert sum((d.size() for d in ex1.find_dirs_at_most())) == 95437


inp = FilesystemNode.read('input.txt')
answer = sum((d.size() for d in inp.find_dirs_at_most()))
print("Part 1 =", answer)
assert answer == 1084134 # check with accepted answer

########
# PART 2

TOTAL_SIZE = 70000000
UPDATE_SIZE = 30000000

ex1_needed = 30000000 - (70000000 - ex1.size())
assert min(ex1.get_dirs(ex1_needed), key = lambda n : n.size()).size() == 24933642

inp_needed = 30000000 - (70000000 - inp.size())
answer = min(inp.get_dirs(inp_needed), key = lambda n : n.size()).size()
print("Part 2 =", answer)
assert answer == 6183184 # check with accepted answer
