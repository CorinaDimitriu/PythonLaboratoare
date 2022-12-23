"""
This module generates rsa primes.
"""
import random
import miller_rabin


def gen_rsa_prime_parameters(size: int) -> (int, int):
    """
    Generates rsa prime parameters widely known as p and q, of size given as parameter.
    ``p`` and ``q`` are prime numbers tested 10 times against the Miller-Rabin test.

    :param size: the desired length (same length, in bits) of ``p`` and ``q``
    :type size: int
    :return: ``p`` and ``q``
    :rtype: (int, int)
    """
    p = generate_prime(size)
    q = generate_prime(size)
    return p, q


def generate_prime(size: int) -> int:
    """
    Generates prime number of exactly **size** bits. The primality is checked using the Miler-Rabin probabilistic
     primality test.

    :param size: the size of the prime which is about to be generated (in bits)
    :type size: int
    :return: the first generated prime number which passed the primality test
    :rtype: int
    """
    while True:
        number = random.randint(2 ** (size - 1), 2 ** size - 1)
        if miller_rabin.is_prime(number):
            return number
