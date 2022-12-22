# This module works with integers

import random
import rsa_generator
import mgf1


global public_key


def compute_parameters():
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
    e = public_key[1]
    n = public_key[0]
    return pow(plaintext, e, n)


def decrypt_rsa(ciphertext, private_key):  # ciphertext is assumed to be an integer
    d = private_key[2]
    n = public_key[0]
    return pow(ciphertext, d, n)


# "all or nothing"
def oaep_padding_encode(message, zeros, rand_bits):  # message is assumed to be an integer
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
    total_len = message_len + zeros + rand_bits
    cipher = str(bin(cipher))[2:]
    x_y_message = ''.join(['0' for _ in range(total_len - len(cipher))]) + cipher
    X = x_y_message[:message_len + zeros]
    Y = x_y_message[message_len + zeros:]
    rand_seed = int(Y, 2) ^ int(mgf1.mgf(rand_bits, int(X, 2)), 2)
    padded_message = int(X, 2) ^ int(mgf1.mgf(message_len + zeros, rand_seed), 2)
    return int(str(bin(padded_message))[2:][:message_len], 2)


def encrypt_rsa_oaep(plaintext):  # plaintext is assumed to be an integer
    X, Y = oaep_padding_encode(plaintext, 24, 64)
    # we know X has 128+24 bits, Y has 64 bits
    binary_seed = str(bin(Y))[2:]
    binary_seed = ''.join(['0' for _ in range(64 - len(binary_seed))]) + binary_seed
    return encrypt_rsa(int(str(bin(X))[2:] + binary_seed, 2))


def decrypt_rsa_oaep(ciphertext, private_key, expected_len):  # plaintext is assumed to be an integer
    x_y_message = decrypt_rsa(ciphertext, private_key)
    return oaep_padding_decode(x_y_message, expected_len, 24, 64)
