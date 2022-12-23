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


def initialize_sha256() -> None:
    """
    This function initializes the hashes list which will be used during sha-256
     digest computing and converts all 8 of them to binary format.
    """
    global hashes
    hashes = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
    convert_hashes_to_binary()


def convert_hashes_to_binary() -> None:
    """
    This function converts integers to octet strings.
    The target integers are the hashes required by the digest computing algorithm.
    """
    global hashes
    hashes = [str(bin(hashes[i]))[2:] for i in range(8)]
    hashes = [''.join('0' for _ in range(32 - len(hashes[i]))) + hashes[i] for i in range(8)]


def add_one() -> None:
    """
    This function adds a bit set on 1 at the end of the message/plaintext.
    """
    global plaintext
    plaintext += '1'


def add_length() -> None:
    """
    This function replaces the last 64 bytes of the plaintext with the length
    of the initial message in binary form.
    """
    global plaintext
    len_in_binary = str(bin(len(original_plaintext)))[2:]
    len_in_binary = ''.join(['0' for _ in range(64 - len(len_in_binary))]) \
                    + len_in_binary
    plaintext += len_in_binary


def padding_until_512_less64() -> None:
    """
    This function pads the plaintext with 0’s until data is a multiple of 512, less 64 bits (448 bits).
    """
    global plaintext
    padding = 512 - len(plaintext) % 512
    if padding < 64:
        padding += 512
    plaintext += ''.join(['0' for _ in range(padding)])
    plaintext = plaintext[:-64]


def pre_processing() -> None:
    """
    This function encapsulates the pre-processing operations performed on the plaintext before
    actually computing the hash digest: adding a one bit, padding with 0's and adding the length at the end.
    """
    add_one()
    padding_until_512_less64()
    add_length()


def split_plaintext_into_blocks() -> None:
    """
    This function splits the plaintext into 512-bits blocks.
    The blocks are encoded as octet strings.
    """
    global plaintext_blocks
    plaintext_blocks = [plaintext[i:i + 512] for i in range(0, len(plaintext), 512)]


def apply_main_transformations() -> None:
    """
    This function iterates through the 512-bit blocks and updates the hashes.
    Eventually, it computes the digest after the last block has passed through
    all the required transformations.
    """
    split_plaintext_into_blocks()
    for plain_block in plaintext_blocks:
        apply_main_block_transformation(plain_block)
    return compute_digest(hashes)


def apply_main_block_transformation(plain_block: str) -> None:
    """
    This function iterates through all the steps required for binary blocks in order to update
    hashes at the end of each round of transformations per block.
    Essentially, the so-mentioned transformations involve performing message scheduling and compression.
    Plaintext is split into 16 32-bit blocks, which are added 48 brand new 32-bit on 0 blocks. For each
    32-bit block, compression is performed.

    :param plain_block: the binary string block to perform transformations on
    :type plain_block: str
    """
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


def create_hashes() -> list[str]:
    """
    This function ensures that, at the beginning of each round of transformations per block,
    the operations start with the updated version of the hashes, which was obtained during
    the computations made for the previous message block.
    :return: the last version of the hashes list
    :rtype: list[str]
    """
    particular_hashes = list(hashes)
    return particular_hashes


def modify_hashes_within_chunk_loop(particular_hashes: list[str]) -> None:
    """
    This function performs addition between the last version of the hashes
    (last updated at the end of the previous round of transformations per block)
    and the last version of the particularly updated hashes during the transformations
    performed on the current block.

    :param particular_hashes: the last version of the hashes
        (last updated at the end of the previous round of transformations per block)
    :type particular_hashes: list[str]
    """
    global hashes
    hashes = [addition(hashes[i], particular_hashes[i]) for i in range(8)]


def create_message_schedule(bytes_array32: list[str]) -> list[str]:
    """
    This function updates the last 48 32-bit blocks of the plaintext by combining
    right rotations, right shifts and additions on the previous blocks.

    :param bytes_array32: the plaintext split into 32-bit blocks
    :type bytes_array32: list[str]
    :return: the updated plaintext as an 32-bit octet strings list
    :rtype: list[str]
    """
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


def compression(bytes32: str, counter: int, copy_hashes: list[str]) -> list[str]:
    """
    The compression function mixes the hashes from the previous round of transformations per block
    by performing right rotations, &-operations, not-operations, switching and additions on them.
    The 32-bit plaintext block prove their utility during additions.

    :param bytes32: the current 32-bit block
    :type bytes32: str
    :param counter: the index of the block
    :type counter: int
    :param copy_hashes: the current version of the hashes
    :type copy_hashes: list[str]
    :return: the updated version of the hashes
    :rtype: list[str]
    """
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


def compute_digest(particular_hashes: list[str]) -> str:
    """
    This function joins all hashes into an octet string.

    :param particular_hashes: the final version of the hashes
    :type particular_hashes: list[str]
    :return: the digest derived from concatenating all the hashes (which are, in fact, octet strings)
    :rtype: str
    """
    return ''.join(particular_hashes[i] for i in range(8))


def right_rotate(text: str, bits: int) -> str:
    """
    This function moves to the end a couple of bits located at the beginning of the octet string.

    :param text: the octet string on which the rotation is performed
    :type text: str
    :param bits: the number of bits being moved
    :type bits: int
    :return: the updated octet string
    :rtype: str
    """
    to_be_moved = text[-bits:]
    text = to_be_moved + text[:-bits]
    return text


def right_shift(text: str, bits: int) -> str:
    """
    This function performs right-shifting with a number of bits on *text*.

    :param text: the octet string on which the shifting is performed
    :type text: str
    :param bits: the number of bits being shifted
    :type bits: int
    :return: the updated octet string
    :rtype: str
    """
    return ''.join(['0' for _ in range(bits)]) + text[:-bits]


def xor(bytes1: str, bytes2: str) -> str:
    """
    This function performs xor (particular binary addition) between two octet strings.

    :param bytes1: the first octet bit to be xored
    :type bytes1: str
    :param bytes2: the second octet bit to be xored
    :type bytes2: str
    :return: the result of the xor operation
    :rtype: str
    """
    binary = str(bin(int(bytes1, 2) ^ int(bytes2, 2)))[2:]
    binary = ''.join('0' for _ in range(32 - len(binary))) + binary
    return binary


def addition(bytes1: str, bytes2: str) -> str:
    """
    This function performs addition between two octet strings. The octet strings are firstly
    converted to integers, so that modulo ``pow(2, 32)`` addition can be performed.

    :param bytes1: the first octet bit
    :type bytes1: str
    :param bytes2: the second octet bit
    :type bytes2: str
    :return: the result of the addition operation
    :rtype: str
    """
    binary = str(bin((int(bytes1, 2) + int(bytes2, 2)) % (2 ** 32)))[2:]
    binary = ''.join('0' for _ in range(32 - len(binary))) + binary
    return binary


def and_operation(bytes1: str, bytes2: str) -> str:
    """
    This function performs *and* operation between two octet strings. The octet strings are firstly
    converted to integers and additional bytes are added if necessary to obtain a complete 32-bit block.

    :param bytes1: the first octet bit
    :type bytes1: str
    :param bytes2: the second octet bit
    :type bytes2: str
    :return: the result as octet string
    :rtype: str
    """
    binary = str(bin(int(bytes1, 2) & int(bytes2, 2)))[2:]
    binary = ''.join('0' for _ in range(32 - len(binary))) + binary
    return binary


def not_operation(bytes_only: str) -> str:
    """
    This function operates on a bit block and negates it, by reversing all its bits.
    More precisely, the length stays the same, all the 0's become 1's and all the 1's become 0's.

    :param bytes_only: the bit block to perform negation on
    :type bytes_only: str
    :return: the negated bit block
    :rtype: str
    """
    return ''.join([str(int('1') - int(bytes_only[i]))
                    for i in range(0, len(bytes_only))])


def execute_sha256(user_plaintext: str) -> str:
    """
    This function concatenates all the necessary steps for computing sha-256 binary digest.
    Details about pre-processing, 512-bit and 32-bit (*atomic*) block transformations are listed
    inside the description of the corresponding functions.

    :param user_plaintext: the plaintext on which digest is aimed to be computed
    :type user_plaintext: str
    :return: the hash digest
    :rtype: str
    """
    global plaintext
    global original_plaintext
    initialize_sha256()
    plaintext = user_plaintext
    original_plaintext = user_plaintext
    pre_processing()
    return apply_main_transformations()
