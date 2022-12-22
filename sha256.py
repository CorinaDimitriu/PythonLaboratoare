# This module uses binary format for plaintext and hash

plaintext = ''
original_plaintext = ''
plaintext_blocks = ['']
hashes = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
round_constants = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
                   0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
                   0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
                   0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
                   0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
                   0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
                   0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
                   0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]


def initialize_sha256():
    global hashes
    hashes = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
    convert_hashes_to_binary()


def convert_hashes_to_binary():
    global hashes
    hashes = [str(bin(hashes[i]))[2:] for i in range(8)]
    hashes = [''.join('0' for _ in range(32 - len(hashes[i]))) + hashes[i] for i in range(8)]


def add_one():
    global plaintext
    plaintext += '1'


def add_length():
    global plaintext
    len_in_binary = str(bin(len(original_plaintext)))[2:]
    len_in_binary = ''.join(['0' for _ in range(64 - len(len_in_binary))]) \
                    + len_in_binary
    plaintext += len_in_binary


def padding_until_512_less64():
    global plaintext
    padding = 512 - len(plaintext) % 512
    if padding < 64:
        padding += 512
    plaintext += ''.join(['0' for _ in range(padding)])
    plaintext = plaintext[:-64]


def pre_processing():
    add_one()
    padding_until_512_less64()
    add_length()


def split_plaintext_into_blocks():
    global plaintext_blocks
    plaintext_blocks = [plaintext[i:i + 512] for i in range(0, len(plaintext), 512)]


def apply_main_transformations():
    split_plaintext_into_blocks()
    for plain_block in plaintext_blocks:
        apply_main_block_transformation(plain_block)
    return compute_digest(hashes)


def apply_main_block_transformation(plain_block):
    global hashes
    bytes_array32 = [plain_block[i:i + 32] for i in range(0, 512, 32)]
    bytes_array32 += [''.join(['0' for _ in range(32)])
                      for _ in range(48)]
    bytes_array32 = create_message_schedule(bytes_array32)
    particular_hashes = create_hashes()
    for counter in range(0, 64):
        particular_hashes = compression(bytes_array32[counter],
                                        counter, particular_hashes)
    modify_hashes_within_chunk_loop(particular_hashes)


def create_hashes():
    particular_hashes = list(hashes)
    return particular_hashes


def modify_hashes_within_chunk_loop(particular_hashes):
    global hashes
    hashes = [addition(hashes[i], particular_hashes[i]) for i in range(8)]


def create_message_schedule(bytes_array32):
    for counter in range(16, 64):
        s0 = xor(xor(right_rotate(bytes_array32[counter - 15], 7),
                     right_rotate(bytes_array32[counter - 15], 18)),
                 right_shift(bytes_array32[counter - 15], 3))
        s1 = xor(xor(right_rotate(bytes_array32[counter - 2], 17),
                     right_rotate(bytes_array32[counter - 2], 19)),
                 right_shift(bytes_array32[counter - 2], 10))
        bytes_array32[counter] = addition(addition(
            addition(bytes_array32[counter - 16], s0),
            bytes_array32[counter - 7]), s1)
    return bytes_array32


def compression(bytes32, counter, copy_hashes):
    copy_k = [str(bin(round_constants[i]))[2:] for i in range(64)]
    S1 = xor(xor(right_rotate(copy_hashes[4], 6),
                 right_rotate(copy_hashes[4], 11)),
             right_rotate(copy_hashes[4], 25))
    ch = xor(and_operation(copy_hashes[4], copy_hashes[5]),
             and_operation(not_operation(copy_hashes[4]), copy_hashes[6]))
    temp1 = addition(addition(addition(addition(copy_hashes[7], S1), ch),
                              copy_k[counter]), bytes32)
    S0 = xor(xor(right_rotate(copy_hashes[0], 2),
                 right_rotate(copy_hashes[0], 13)),
             right_rotate(copy_hashes[0], 22))
    maj = xor(xor(and_operation(copy_hashes[0], copy_hashes[1]),
                  and_operation(copy_hashes[0], copy_hashes[2])),
              and_operation(copy_hashes[1], copy_hashes[2]))
    temp2 = addition(S0, maj)
    copy_hashes[7] = copy_hashes[6]
    copy_hashes[6] = copy_hashes[5]
    copy_hashes[5] = copy_hashes[4]
    copy_hashes[4] = addition(copy_hashes[3], temp1)
    copy_hashes[3] = copy_hashes[2]
    copy_hashes[2] = copy_hashes[1]
    copy_hashes[1] = copy_hashes[0]
    copy_hashes[0] = addition(temp1, temp2)
    return copy_hashes


def compute_digest(particular_hashes):
    return ''.join(particular_hashes[i] for i in range(8))


def right_rotate(text, bits):
    to_be_moved = text[-bits:]
    text = to_be_moved + text[:-bits]
    return text


def right_shift(text, bits):
    return ''.join(['0' for _ in range(bits)]) + text[:-bits]


def xor(bytes1, bytes2):
    binary = str(bin(int(bytes1, 2) ^ int(bytes2, 2)))[2:]
    binary = ''.join('0' for _ in range(32 - len(binary))) + binary
    return binary


def addition(bytes1, bytes2):
    binary = str(bin((int(bytes1, 2) + int(bytes2, 2)) % (2 ** 32)))[2:]
    binary = ''.join('0' for _ in range(32 - len(binary))) + binary
    return binary


def and_operation(bytes1, bytes2):
    binary = str(bin(int(bytes1, 2) & int(bytes2, 2)))[2:]
    binary = ''.join('0' for _ in range(32 - len(binary))) + binary
    return binary


def not_operation(bytes_only):
    return ''.join([str(int('1') - int(bytes_only[i]))
                    for i in range(0, len(bytes_only))])


def execute_sha256(user_plaintext):
    global plaintext
    global original_plaintext
    initialize_sha256()
    plaintext = user_plaintext
    original_plaintext = user_plaintext
    pre_processing()
    return apply_main_transformations()
