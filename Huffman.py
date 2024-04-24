import os
from collections import Counter
import heapq
from io import BytesIO

class HuffmanNode:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_codes = {}

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if other == None:
                return False
            if not isinstance(other, HeapNode):
                return False

            return self.freq == other.freq

    def set_reverse_codes(self, reverse_codes):
        self.reverse_codes = reverse_codes

    def make_frequency_dict(self, text):
        return Counter(text)


    def make_heap(self, frequency):
        for key, count in frequency.items():
            node = self.HeapNode(key, count)
            heapq.heappush(self.heap, node)

    def merge_codes(self):
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_rec(self, node, current_node ):
        if node == None :
            return
        if node.char != None: #leaf aka caractères
            self.codes[node.char] = current_node
            self.reverse_codes[current_node] = node.char

        self.make_codes_rec(node.left, current_node + "0")
        self.make_codes_rec(node.right, current_node + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_rec(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    #return a string of bytes, you'll have to convert
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if (len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2)) #convert a byte string into byte code ()
        return b

    def compress(self, text):

        frequency = self.make_frequency_dict(text)

        self.make_heap(frequency)

        self.merge_codes()

        self.make_codes()

        encoded_text = self.get_encoded_text(text)

        padded_encoded_text = self.pad_encoded_text(encoded_text)

        return bytes(self.get_byte_array(padded_encoded_text))


    def get_string_of_binary_from_binary(self, binary_code):

        bit_string = ""

        byte_stream = BytesIO(binary_code)

        byte = byte_stream.read(1)
        while (len(byte) > 0):
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = byte_stream.read(1)
        return bit_string

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]
        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if (current_code in self.reverse_codes):
                character = self.reverse_codes[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, binary_code):

        padded_encoded_text = self.get_string_of_binary_from_binary(binary_code)
        encoded_text = self.remove_padding(padded_encoded_text)
        decoded_text = self.decode_text(encoded_text)
        return decoded_text







