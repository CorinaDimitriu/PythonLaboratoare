"""
This module performs AES-128 symmetric encryption.
Plaintext, ciphertext and keys are considered to be in hexadecimal
"""

import concurrent.futures
import numpy as np
import random

plaintext_blocks = ['']
ciphertext_blocks = ['']

s_box = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
         ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
         ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
         ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
         ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
         ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
         ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
         ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
         ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
         ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
         ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
         ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
         ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
         ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
         ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
         ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]

s_box_inverse = [['52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb'],
                 ['7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb'],
                 ['54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e'],
                 ['08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25'],
                 ['72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92'],
                 ['6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84'],
                 ['90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06'],
                 ['d0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b'],
                 ['3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73'],
                 ['96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e'],
                 ['47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b'],
                 ['fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4'],
                 ['1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f'],
                 ['60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef'],
                 ['a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61'],
                 ['17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d']]

r_con = ['01000000', '02000000', '04000000', '08000000', '10000000', '20000000', '40000000',
         '80000000', '1B000000', '36000000']


def divide_plaintext(plaintext):
    """
    Plaintext is divided into blocks of 128 bits each. Last block might contain less than 128 bits.

    :param plaintext: the original message (the one which is being symmetrically encrypted)
    :type plaintext: str
    """
    global plaintext_blocks
    # padding_bytes = 32 - len(plaintext) % 32
    # if padding_bytes == 32:
    #     padding_bytes = 0
    # plaintext += ''.join(['0' for x in range(padding_bytes)])
    plaintext_blocks = [plaintext[i:i + 32] for i in range(0, len(plaintext), 32)]


def divide_ciphertext(ciphertext):
    """
    Plaintext is divided into blocks of 128 bits each. Last block might contain less than 128 bits.

    :param ciphertext: the encrypted message (which is about to be decrypted)
    :type ciphertext: str
    """
    global ciphertext_blocks
    ciphertext_blocks = [ciphertext[i:i + 32] for i in range(0, len(ciphertext), 32)]


def key_schedule(key):
    """
    Implementation of the key scheduling algorithm from the AES-128 standard.

    :param key: the base key
    :type key: str
    :return: all 11 round keys, the first one being the base key
    :rtype: list[str]
    """
    round_keys = [key]
    for key_round in range(1, 11):
        round_key = compute_round_key(round_keys[key_round - 1], key_round)
        round_keys.append(round_key)
    return round_keys


def compute_round_key(ante_key, key_round):
    """
    Computes one round key. There are 10 rounds in the key scheduling algorithm and
    this function contains repetitive steps that apply for each of them.

    :param ante_key: the key generated at the previous round (round 0 is the base round)
    :type ante_key: str
    :param key_round: the index of the current round
    :type key_round: int
    :return: the generated round key
    :rtype: str
    """
    w = [ante_key[i:i + 8] for i in range(0, 32, 8)]
    w[3] += (w[3][0:2])
    third_inverse = ''.join([w[3][i + 2:i + 4] for i in range(0, 8, 2)])
    w[3] = w[3][0:8]
    round_key = ''.join([s_box_transformation(third_inverse[i:i + 2]) for i in range(0, 8, 2)])
    round_key = xor_stream(round_key, r_con[key_round - 1])
    round_key = xor_stream(round_key, w[0])
    round_key += xor_stream(round_key[0:8], w[1])
    round_key += xor_stream(round_key[8:16], w[2])
    round_key += xor_stream(round_key[16:24], w[3])
    return round_key


def pad_with_zeros(block):
    """
    This function aims to add additional zeros to the blocks which are less
    than 128 bits in length. Due to the fact that blocks are encoded in base16, the required length
    becomes 32 hexadecimal units.

    :param block: the block to be padded
    :type block: str
    :return: the padded block
    :rtype: str
    """
    padding_bytes = 32 - len(block) % 32
    if padding_bytes == 32:
        padding_bytes = 0
    block += ''.join(['0' for x in range(padding_bytes)])
    return block


def apply_main_transformations(plaintext_block, round_keys, original_block, mode='encrypt'):
    """
    Applies the transformation per 128-bits (or less) block, known as:
    substitution bytes, shift rows, mix columns and addition of round constants.
    There are 10 rounds, preceded by an initial addition of round constant. The last
    round lacks the mix columns operation.

    :param plaintext_block: the target block (derived from the counter)
    :type plaintext_block: str
    :param round_keys: the round keys previously returned by the key scheduling algorithm
    :type round_keys: list[str]
    :param original_block: the initial text (provided that CTR operation mode is used)
    :type original_block: str
    :param mode: indicates whether transformations are performed during encryption or decryption.
        It has 2 possible values, namely encrypt and decrypt, first one being the default value
    :type mode: str
    :return: the encrypted/decrypted block
    :rtype: str
    """
    original_block = pad_with_zeros(original_block)
    state_matrix = convert_text_into_matrix(plaintext_block)
    if mode == 'encrypt':
        state_matrix = add_round_key(state_matrix, round_keys[0])
        for plain_round in range(1, 11):
            state_matrix = apply_round_transformation(state_matrix, round_keys[plain_round], plain_round)
    elif mode == 'decrypt':
        for plain_round in range(10, 0, -1):
            state_matrix = apply_decryption_round_transformation(state_matrix, round_keys[plain_round], plain_round)
        state_matrix = add_round_key(state_matrix, round_keys[0])
    return xor_stream(get_ciphertext(np.transpose(state_matrix)), original_block)


def convert_text_into_matrix(block):
    """
    Hexadecimal string is converted into 4x4 matrix. The matrix takes two hexa units for each
    of its elements.

    :param block: the 32 hexadecimal units block
    :type block: str
    :return: the (transposed) matrix derived from the block
    :rtype: list[list[str]]
    """
    matrix = [[block[i:i + 2] for i in range(j, j + 8, 2)] for j in range(0, 32, 8)]
    matrix = np.transpose(matrix)
    return matrix


def get_ciphertext(transposed_final_matrix):
    """
    AES 4x4 matrix is converted back to hexadecimal string.

    :param transposed_final_matrix: the matrix to be converted
    :type transposed_final_matrix: list[list[str]]
    :return: the (transposed) matrix as hexadecimal string
    :rtype: str
    """
    return ''.join(transposed_final_matrix[i][j]
                   for i in range(0, 4) for j in range(0, 4))


def apply_round_transformation(state_matrix, key, round_no):
    """
    This function performs the round transformations on specified block. The block is kept as
    4x4 state matrix. The same matrix is changed during each round.

    :param state_matrix: the state matrix
    :type state_matrix: list[list[str]]
    :param key: the round key
    :type key: str
    :param round_no: the index of the round
    :type round_no: int
    :return: the new state of the block matrix
    :rtype: list[list[str]]
    """
    state_matrix = substitution_bytes(state_matrix, 'standard')
    state_matrix = shift_rows(state_matrix, [0, 1, 2, 3])
    if round_no != 10:
        state_matrix = mix_columns(state_matrix)
    state_matrix = add_round_key(state_matrix, key)
    return state_matrix


def apply_decryption_round_transformation(state_matrix, key, round_no):
    """
    The customized succession of operations for decryption. Encryption operations are
    performed in reverse order (first comes the addition of round constants etc.)

    :param state_matrix: the state matrix of the block being decrypted
    :type state_matrix: list[list[str]]
    :param key: the round key
    :type key: str
    :param round_no: the round's index
    :type round_no: int
    :return: the new state of the block matrix after performing the required operations
    :rtype: list[list[str]]
    """
    state_matrix = add_round_key(state_matrix, key)
    if round_no != 10:
        state_matrix = mix_columns(state_matrix, 'inverse')
    state_matrix = shift_rows(state_matrix, [0, 3, 2, 1])
    state_matrix = substitution_bytes(state_matrix, 'inverse')
    return state_matrix


def add_round_key(state_matrix, key):
    """
    The addition of round constants.

    :param state_matrix: the block's state matrix
    :type state_matrix: list[list[str]]
    :param key: the round key
    :type key: str
    :return: the new state of the block matrix
    :rtype: list[list[str]]
    """
    key_matrix = [[key[i:i + 2] for i in range(j, j + 8, 2)] for j in range(0, 32, 8)]
    key_matrix = np.transpose(key_matrix)
    state_matrix = xor_matrix(key_matrix, state_matrix)
    return state_matrix


def substitution_bytes(state_matrix, mode):
    """
    The bytes substitution operation. The hexadecimal units are replaced with
    combinations provided by the special s-box matrix.

    :param state_matrix: the block's state matrix
    :type state_matrix: list[list[str]]
    :param mode: standard or inverse (every word but standard will be perceived as inverse)
        There are different s-box matrices depending on the nature of the operation (encryption or decryption)
    :type mode: str
    :return: the new state of the block matrix
    :rtype: list[list[str]]
    """
    return [[s_box_transformation(state_matrix[i][j], mode) for j in range(4)] for i in range(4)]


def shift_rows(state_matrix, shift_per_column):
    """
    The rows shifting operation. Rows are left shifted with number of elements
    provided by *shift_per_column* depending on the row index.

    :param state_matrix: the block's state matrix
    :type state_matrix: list[list[str]]
    :param shift_per_column: the number of elements which have to be shifted for each row (index)
    :type shift_per_column: list[int]
    :return: the new state of the block matrix
    :rtype: list[list[str]]
    """
    new_state_matrix = []
    for i in range(0, 4):
        state_matrix[i] += state_matrix[i]
        new_state_matrix.append([state_matrix[i][j + shift_per_column[i]]
                                 for j in range(0, 4)])
    return new_state_matrix


def mix_columns(state_matrix, mode='standard'):
    """
    The addition of round constants.

    :param state_matrix: the block's state matrix
    :type state_matrix: list[list[str]]
    :param mode: standard or inverse (every word but standard will be perceived as inverse)
        The fixed matrix required at this step, which is constant, depends on the operation performed
        (encryption or decryption)
    :type mode: str
    :return: the new state of the block matrix
    :rtype: list[list[str]]
    """
    if mode == 'standard':
        fixed_matrix = [['02', '03', '01', '01'],
                        ['01', '02', '03', '01'],
                        ['01', '01', '02', '03'],
                        ['03', '01', '01', '02']]
    else:
        fixed_matrix = [['0E', '0B', '0D', '09'],
                        ['09', '0E', '0B', '0D'],
                        ['0D', '09', '0E', '0B'],
                        ['0B', '0D', '09', '0E']]
    return multiply_matrices(fixed_matrix, state_matrix)


def s_box_transformation(pair, mode='standard'):
    """
    The s-box atomic substitution.

    :param pair: a pair of two hexa units identifying the row and column in the (inverse) s-box matrix
    :type pair: (str, str)
    :param mode: standard or inverse (every word but standard will be perceived as inverse)
        The mode corresponds to the operation performed (encryption or decryption)
    :type mode: str
    :return: the element located at the intersection of row pair[0] and column pair[1]
    :rtype: str
    """
    if mode == 'standard':
        return s_box[int(pair[0], 16)][int(pair[1], 16)]
    else:
        return s_box_inverse[int(pair[0], 16)][int(pair[1], 16)]


def xor_stream(key, rcon):
    """
    This function is built with the purpose of xoring two hexa strings.

    :param key: the first hexa string
    :type key: str
    :param rcon: the second hexa string
    :type rcon: str
    :return: the result as hexa string
    :rtype: str
    """
    hexadecimal = hex(int('0x' + key, 16) ^ int(rcon, 16))[2:]
    zeros = ''.join(['0' for _ in range(len(key) - len(hexadecimal))])
    return zeros + hexadecimal


def xor_matrix(text, key):
    """
    This function is built with the purpose of xoring two 4x4 hexa matrices.

    :param text: the first matrix
    :type text: list[list[str]]
    :param key: the second matrix
    :type key: list[list[str]]
    :return: the result as 4x4 hexa matrix
    :rtype: list[list[str]]
    """
    return [[xor_stream(key[i][j], text[i][j])
             for j in range(4)] for i in range(4)]


def multiply_stream(y, x):
    """
    This function is built with the purpose of multiplying two hexa strings.

    :param x: the first hexa string
    :type x: str
    :param y: the second hexa string
        It only takes values from {01, 02, 03, 09, 0B, 0D, 0E},
        due to the structure of the fixed matrix used at the mix columns operation
    :type y: str
    :return: the result as hexa string
    :rtype: str
    """
    # y comes from static matrix
    hexadecimal = hex(int('0x' + x, 16) * int('0x' + y, 16))[2:]
    if y == '02':
        hexadecimal = multiply_by_02(x)
    elif y == '03':
        hexadecimal = xor_stream(multiply_by_02(x), x)
    elif y == '09':
        hexadecimal = xor_stream(multiply_by_02(multiply_by_02(multiply_by_02(x))), x)
    elif y == '0B':
        hexadecimal = xor_stream(multiply_by_02
                                 (xor_stream(multiply_by_02(multiply_by_02(x)), x)), x)
    elif y == '0D':
        hexadecimal = xor_stream(multiply_by_02
                                 (multiply_by_02(xor_stream(multiply_by_02(x), x))), x)
    elif y == '0E':
        hexadecimal = multiply_by_02(xor_stream
                                     (multiply_by_02(xor_stream(multiply_by_02(x), x)), x))
    zeros = ''.join(['0' for _ in range(len(x) - len(hexadecimal))])
    return zeros + hexadecimal


def multiply_by_02(x):
    """
    Special multiplication by ``02`` in ``GF(pow(2, 8))`` function.
    The input and output are still hexa strings.

    :param x: the number aimed to be multiplied by ``02``
    :type x: str
    :return: the result of the multiplication operation
    :rtype: str
    """
    original_x = x
    x = hex((int('0x' + x, 16) << 1) & 255)[2:]
    if int('0x' + original_x, 16) >= 128:
        x = xor_stream(x, '1B')
    return x


def multiply_matrices(static_m, dynamic_m):
    """
    Multiplication of hexa matrices required at the mix columns operation.

    :param static_m: the fixed matrix
    :type static_m: list[list[str]]
    :param dynamic_m: the state matrix
    :type dynamic_m: list[list[str]]
    :return: the result matrix
    :rtype: list[list[str]]
    """
    new_dynamic_m = []
    for new_lin_index in range(0, 4):
        dynamic_line = []
        for col in range(0, 4):
            old_xor = '00'
            for lin in range(0, 4):
                old_xor = xor_stream(old_xor, multiply_stream(static_m[new_lin_index][lin],
                                                              dynamic_m[lin][col]))
            dynamic_line.append(old_xor)
        new_dynamic_m.append(dynamic_line)
    return new_dynamic_m


def add_one(counter):
    """
    This function performs adding one operation.

    :param counter: the counter used by the CTR iteration mode
    :type counter: str
    :return: ``counter + 1`` (in hexa)
    :rtype: str
    """
    return hex(1 + int('0x' + counter, 16))[2:]


def encrypt_aes128(plaintext):
    """
    This function performs AES-128 encryption in CTR mode. The operations being performed are:
        * key generation
        * key scheduling => round keys
        * counter(s) generation
        * encrypting counters in AES-128 CBC mode for single words
        * xoring counters with the original blocks of plaintext

    :param plaintext: the data to be encrypted
    :type plaintext: str
    :return: encrypted data
    :rtype: str
    """
    key = generate_128bits_random()
    divide_plaintext(plaintext)
    round_keys = key_schedule(key)
    counter = generate_128bits_random()
    iterate_counter = counter
    counters = [iterate_counter]
    if len(plaintext_blocks) < 1:
        counters = []
    for i in range(len(plaintext_blocks) - 1):
        iterate_counter = add_one(iterate_counter)
        counters.append(iterate_counter)
    return key, counter, parallelize_ctr(counters, round_keys)


def parallelize_ctr(counters, round_keys, mode='encrypt'):
    """
    This function implements the CTR mode for a set of counters through parallelization
    of the encryption required for each of them.

    :param counters: list[str]
    :param round_keys: list[str]
    :param mode: encrypt or decrypt depending on the operation performed on the text blocks
    :return:
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        processes = []
        results = []
        for i in range(len(counters)):
            if mode == 'encrypt':
                processes.append(executor.submit(apply_main_transformations,
                                                 counters[i], round_keys, plaintext_blocks[i]))
            else:
                processes.append(executor.submit(apply_main_transformations,
                                                 counters[i], round_keys, ciphertext_blocks[i]))
        for p in processes:
            results.append(p.result())
        if mode == 'encrypt':
            length = len(plaintext_blocks)
            if length > 0:
                last_length = len(plaintext_blocks[length - 1])
        else:
            length = len(ciphertext_blocks)
            if length > 0:
                last_length = len(ciphertext_blocks[length - 1])
        if length > 0 and last_length < 32:
            results[len(results) - 1] = \
                results[len(results) - 1][:last_length]
        ciphertext = ''.join(result for result in results)
        executor.shutdown()
        return ciphertext


def generate_128bits_random():
    """
    Exactly 128-bits random generation.

    :return: exactly 128-bits random, converted into hexa string
    :rtype: str
    """
    return hex(random.randint(2 ** 127, 2 ** 128 - 1))[2:]


def decrypt_aes128(counter, ciphertext, key):
    """
    This function performs AES-128 decryption in CTR mode. The operations being performed are:
        * key generation
        * key scheduling => round keys
        * counter(s) generation
        * encrypting counters in AES-128 CBC mode for single words
        * xoring counters with the blocks of ciphertext provided through parameter

    :param ciphertext: encrypted data
    :type ciphertext: str
    :return: original data
    :rtype: str
    """
    divide_ciphertext(ciphertext)
    round_keys = key_schedule(key)
    iterate_counter = counter
    counters = [iterate_counter]
    if len(ciphertext_blocks) < 1:
        counters = []
    for i in range(len(ciphertext_blocks) - 1):
        iterate_counter = add_one(iterate_counter)
        counters.append(iterate_counter)
    return parallelize_ctr(counters, round_keys, 'decrypt')
