"""
 This module works with integers and implements the RSA-OAEP scheme.
 OAEP is the padding method being used.
"""

import random
import rsa_generator
import mgf1


global public_key


def compute_parameters():
    """
    This function uses lower layers such as *rsa_generator* and *miller_rabin* in order to
    generate large RSA keys. The size of ``p`` and ``q`` is established inside this function, so is ``e`` from
    the public key. There is a code block which enforces that e and (p-1), (q-1) are relatively prime to each other.

    :return: the pair consisting of one public and one private generated key
    :rtype: (int, int)
    """
    global public_key
    target_e = 2 ** 16 + 1
    p, q = rsa_generator.gen_rsa_prime_parameters(512)
    phi_n = (p - 1) * (q - 1)
    while target_e % phi_n == 0 or phi_n % target_e == 0:
        p, q = rsa_generator.gen_rsa_prime_parameters(512)
        phi_n = (p - 1) * (q - 1)
    n_gen = p * q
    # public key - established and visible
    public_key = (n_gen, target_e)
    # private key - established and hidden
    private_key = (p, q, pow(public_key[1], -1, phi_n))
    return public_key, private_key


def encrypt_rsa(plaintext):  # plaintext is assumed to be an integer
    """
    Implements the classic RSA encryption step, by raising the plaintext (as integer) to the power of ``e`` from
    the public key.

    :param plaintext: the information to be encrypted
    :type plaintext: int
    :return: the result of the encryption operation described above as an exponentiation
    :rtype: int
    """
    e = public_key[1]
    n = public_key[0]
    return pow(plaintext, e, n)


def decrypt_rsa(ciphertext, private_key):  # ciphertext is assumed to be an integer
    """
    Implements the classic RSA decryption step, by raising the ciphertext (as integer) to the power of ``d`` from
    the private key. It is known that ``d`` from private key is the modular inverse of ``e`` from public key
    (modulo ``(p-1) * (q-1)``, which makes d hard to guess), making the whole process result into
    the initial plaintext.

    :param ciphertext: the encrypted information which is to be decrypted
    :type ciphertext: str
    :param private_key: the private key which serves for decryption
    :type private_key: (int, int, int)
    :return: initial data being decrypted
    :rtype: int
    """
    d = private_key[2]
    n = public_key[0]
    return pow(ciphertext, d, n)


# "all or nothing"
def oaep_padding_encode(message, zeros, rand_bits):  # message is assumed to be an integer
    """
    Implementation of the encoding step of the OAEP padding scheme.
    The message is randomized before encryption in order
    to force the encryption method **not** to be deterministic.

    :param message: the message to be padded (before encryption)
    :type message: int
    :param zeros: the number of zero bits being added at the end of *message*
    :type zeros: int
    :param rand_bits: the number of random bits contained by the seed
    :type: int
    :return: the padded version of the message, consisting of two bit
        subsequences, which are individually converted to integers
    :rtype: (int, int)
    """
    message_len = len(str(bin(message))[2:])
    message = str(bin(message))[2:] + ''.join(['0' for _ in range(zeros)])
    message = int(message, 2)
    rand_seed = random.randint(2 ** (rand_bits - 1), 2 ** rand_bits - 1)
    hash_per_random = mgf1.mgf(message_len + zeros, rand_seed)
    xor_message = int(hash_per_random, 2) ^ message
    hash_per_message = mgf1.mgf(rand_bits, xor_message)
    xor_random = int(hash_per_message, 2) ^ rand_seed
    return xor_message, xor_random


def oaep_padding_decode(cipher, message_len, zeros, rand_bits):
    """
    Implementation of the encoding step of the OAEP padding scheme. Some additional information
    such as the initial message's length is required.

    :param cipher: the data being subject to decoding
    :type cipher: int
    :param message_len: the length of the initial message (the one which was encoded)
    :type message_len: int
    :param zeros: the number of zero bits which were added at the end of the initial message
        during encoding (established by the protocol)
    :type zeros: int
    :param rand_bits: the number of random bits contained by the seed (established by the protocol)
    :type rand_bits: int
    :return: not anymore padded message
    :rtype: int
    """
    total_len = message_len + zeros + rand_bits
    cipher = str(bin(cipher))[2:]
    x_y_message = ''.join(['0' for _ in range(total_len - len(cipher))]) + cipher
    X = x_y_message[:message_len + zeros]
    Y = x_y_message[message_len + zeros:]
    rand_seed = int(Y, 2) ^ int(mgf1.mgf(rand_bits, int(X, 2)), 2)
    padded_message = int(X, 2) ^ int(mgf1.mgf(message_len + zeros, rand_seed), 2)
    return int(str(bin(padded_message))[2:][:message_len], 2)


def encrypt_rsa_oaep(plaintext):  # plaintext is assumed to be an integer
    """
    Implementation of the RSA-OAEP encryption step. First OAEP padding is performed,
    followed by RSA encryption on the padded plaintext.

    :param plaintext: the information to be encrypted
    :type plaintext: int
    :return: the result of the encryption operation described above
    :rtype: int
    """
    X, Y = oaep_padding_encode(plaintext, 24, 64)
    # we know X has 128+24 bits, Y has 64 bits
    binary_seed = str(bin(Y))[2:]
    binary_seed = ''.join(['0' for _ in range(64 - len(binary_seed))]) + binary_seed
    return encrypt_rsa(int(str(bin(X))[2:] + binary_seed, 2))


def decrypt_rsa_oaep(ciphertext, private_key, expected_len):  # plaintext is assumed to be an integer
    """
    Implementation of the RSA-OAEP decryption step. First RSA decryption on the ciphertext is performed,
    followed by OAEP decoding.

    :param ciphertext: the encrypted information which is to be decrypted
    :type ciphertext: int
    :param private_key: the private key which serves for decryption
    :type private_key: (int, int, int)
    :param expected_len: the expected length of the result (this influences the internal
    transformations made by the algorithm and, therefore, the overall result)
    :type expected_len: int
    :return: initial data being decrypted
    :rtype: int
    """
    x_y_message = decrypt_rsa(ciphertext, private_key)
    return oaep_padding_decode(x_y_message, expected_len, 24, 64)
