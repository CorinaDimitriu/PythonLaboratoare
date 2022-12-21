# This module generates rsa primes
import random
import miller_rabin


def gen_rsa_prime_parameters(size):
    p = generate_prime(size)
    q = generate_prime(size)
    return p, q


def generate_prime(size):
    while True:
        number = random.randint(2 ** (size - 1), 2 ** size - 1)
        if miller_rabin.is_prime(number):
            return number
