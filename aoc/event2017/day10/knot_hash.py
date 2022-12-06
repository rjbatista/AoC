
def knot_hash_round(lengths : list, list_size = 256, rounds = 1):
    """ Perform an knot hash round """
    current_input = list(range(list_size))

    pos = 0
    skip = 0

    for _ in range(rounds):
        for length in lengths:

            end_pos = pos + length
            if end_pos > list_size:
                selected = current_input[pos:] + current_input[:end_pos % list_size]
            else:
                selected = current_input[pos:end_pos]

            for p in range(length):
                current_input[(pos + p) % list_size] = selected[length - p - 1]

            pos = (pos + length + skip) % list_size
            skip += 1

    return current_input

def dense_hash(sparse_hash):
    """ Perform the dense hash """
    hash = [0] * 16

    for idx, v in enumerate(sparse_hash):
        hash[int(idx / 16)] ^= v

    return ''.join(["%02x" % x for x in hash])


def knot_hash(input_str : str):
    """ Return the know hash of the input  """
    inp_list = list(map(ord, input_str)) + [ 17, 31, 73, 47, 23 ]

    return dense_hash(knot_hash_round(inp_list, rounds = 64))
