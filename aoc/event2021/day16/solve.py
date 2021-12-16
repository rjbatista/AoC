from math import prod
from dataclasses import dataclass

########
# PART 1

@dataclass
class Packet:
    version: int
    type_id: int


    def __init__(self, version, type_id) -> None:
        self.version = version
        self.type_id = type_id


    def parse_hex(hex_string):
        bits = []
        for ch in hex_string:
            bits += format(int(ch, 16), '04b')

        return Packet.parse("".join(bits), 1)[0][0]


    def parse(bits, no_packets = -1):
        packets = []
        while bits and (no_packets != 0):
            version = int(bits[:3], 2)

            type_id = int(bits[3:6], 2)

            bits = bits[6:]

            if type_id == 4:
                packet = PacketType4(version, type_id)
            else:
                len_type_id = int(bits[:1], 2)
                bits = bits[1:]

                try:
                    cls = eval("PacketType" + str(type_id))
                except NameError:
                    cls = PacketOperator

                packet = cls(version, type_id, len_type_id)


            packets.append(packet)
            bits = packet.parse(bits)

            if (no_packets > 0):
                no_packets -= 1
        
        return packets, bits


    def read(filename):
        with open("event2021/day16/" + filename, "r") as file:
            return Packet.parse_hex(file.readline().strip())


    def sum_version_number(self):
        return self.version


    def get_value(self):
        raise NotImplementedError(self.type_id)



@dataclass
class PacketOperator(Packet):
    """
    Every other type of packet (any packet with a type ID other than 4)
    represent an operator that performs some calculation on one or more sub-packets contained within
    """
    len_type_id: int
    packets = None


    def parse(self, bits):
        length = 0
        no_packets = 0

        if self.len_type_id == 0:
            length = int(bits[:15], 2)
            bits = bits[15:]

            to_parse = bits[:length]
            bits = bits[length:]

            self.packets = Packet.parse(to_parse)[0]
        else:
            no_packets = int(bits[:11], 2)
            bits = bits[11:]

            self.packets, bits = Packet.parse(bits, no_packets)

        return bits


    def sum_version_number(self):
        return self.version + sum([p.sum_version_number() for p in self.packets])
    
    def __repr__(self) -> str:
        return super().__repr__() + "\n" + str(self.packets)



@dataclass
class PacketType4(Packet):
    """
    Packets with type ID 4 represent a literal value
    """
    value: int = None

    def parse(self, bits):
        value = []
        while bits[0] == '1':
            value += bits[1:5]
            bits = bits[5:]

        value += bits[1:5]
        bits = bits[5:]

        self.value = int("".join(value), 2)

        return bits


    def get_value(self):
        return self.value


# packet represents a literal value with binary representation 011111100101, which is 2021 in decimal.
ex = Packet.parse_hex("D2FE28")
assert ex.version == 6
assert ex.type_id == 4
assert ex.value == 2021

ex = Packet.parse_hex("38006F45291200")
assert ex.version == 1
assert ex.type_id == 6
assert len(ex.packets) == 2
assert ex.packets[0].type_id == 4
assert ex.packets[0].value == 10
assert ex.packets[1].type_id == 4
assert ex.packets[1].value == 20

ex = Packet.parse_hex("EE00D40C823060")
assert ex.version == 7
assert ex.type_id == 3
assert len(ex.packets) == 3
assert ex.packets[0].type_id == 4
assert ex.packets[0].value == 1
assert ex.packets[1].type_id == 4
assert ex.packets[1].value == 2
assert ex.packets[2].type_id == 4
assert ex.packets[2].value == 3

assert Packet.parse_hex("8A004A801A8002F478").sum_version_number() == 16
assert Packet.parse_hex("620080001611562C8802118E34").sum_version_number() == 12
assert Packet.parse_hex("C0015000016115A2E0802F182340").sum_version_number() == 23
assert Packet.parse_hex("A0016C880162017C3686B18A3D4780").sum_version_number() == 31

packet = Packet.read("input.txt")
answer = packet.sum_version_number()
print("Part 1 =", answer)
assert answer == 913 # check with accepted answer

########
# PART 2

class PacketType0(PacketOperator):
    """
    Packets with type ID 0 are sum packets
    their value is the sum of the values of their sub-packets.
    If they only have a single sub-packet, their value is the value of the sub-packet.
    """
    def get_value(self):
        return sum([p.get_value() for p in self.packets])


class PacketType1(PacketOperator):
    """
    Packets with type ID 1 are product packets
    their value is the result of multiplying together the values of their sub-packets.
    If they only have a single sub-packet, their value is the value of the sub-packet.
    """
    def get_value(self):
        return prod([p.get_value() for p in self.packets])


class PacketType2(PacketOperator):
    """
    Packets with type ID 2 are minimum packets
    their value is the minimum of the values of their sub-packets.
    """
    def get_value(self):
        return min([p.get_value() for p in self.packets])


class PacketType3(PacketOperator):
    """
    Packets with type ID 3 are maximum packets
    their value is the maximum of the values of their sub-packets.
    """
    def get_value(self):
        return max([p.get_value() for p in self.packets])


class PacketType5(PacketOperator):
    """
    Packets with type ID 5 are greater than packets
    their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet;
    otherwise, their value is 0. These packets always have exactly two sub-packets.
    """
    def get_value(self):
        return 1 if self.packets[0].get_value() > self.packets[1].get_value() else 0


class PacketType6(PacketOperator):
    """
    Packets with type ID 6 are less than packets
    their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet;
    otherwise, their value is 0. These packets always have exactly two sub-packets.
    """
    def get_value(self):
        return 1 if self.packets[0].get_value() < self.packets[1].get_value() else 0


class PacketType7(PacketOperator):
    """
    Packets with type ID 7 are equal to packets
    their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet;
    otherwise, their value is 0. These packets always have exactly two sub-packets.
    """
    def get_value(self):
        return 1 if self.packets[0].get_value() == self.packets[1].get_value() else 0


# C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
assert Packet.parse_hex("C200B40A82").get_value() == 3
# 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
assert Packet.parse_hex("04005AC33890").get_value() == 54
# 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
assert Packet.parse_hex("880086C3E88112").get_value() == 7
# CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
assert Packet.parse_hex("CE00C43D881120").get_value() == 9
# D8005AC2A8F0 produces 1, because 5 is less than 15.
assert Packet.parse_hex("D8005AC2A8F0").get_value() == 1
# F600BC2D8F produces 0, because 5 is not greater than 15.
assert Packet.parse_hex("F600BC2D8F").get_value() == 0
# 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
assert Packet.parse_hex("9C005AC2F8F0").get_value() == 0
# 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
assert Packet.parse_hex("9C0141080250320F1802104A08").get_value() == 1


packet = Packet.read("input.txt")
answer = packet.get_value()
print("Part 2 =", answer)
assert answer == 1510977819698 # check with accepted answer
