"""
This module represents tha ambition to implement the Miller-Rabin primality test.
"""


import random
import math

low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
              67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
              157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
              251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
              353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449,
              457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569,
              571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661,
              673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
              797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
              911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]


def decompose_number(number):
    """
    In order to prepare for executing the Miller-Rabin primality test, the number
    is written as ``t * pow(2, s)``, where s is maximized and t is odd.

    :param number: the number to decompose, on which the Miller-Rabin test is to be performed
    :type number: int
    :return: s and t, the components of the number's decomposition as described
    :rtype:
    """
    t = number - 1
    s = 0
    while t % 2 == 0:
        t = t // 2
        s += 1
    return s, t


def miller_rabin_test(number):
    """
    The Miller-Rabin primality test implemented.

    :param number: the target number to be tested for primality
    :type number: int
    :return: True if the number is prime according to one iteration
        of the Miller-Rabin test; False, otherwise
    :rtype: bool
    """
    (s, t) = decompose_number(number)
    # number = 1 + t * 2^s
    a = random.randint(2, number - 2)
    if math.gcd(a, number) > 1:
        return False
    r = pow(a, t, number)
    if r in {1, number - 1}:
        return True
    for i in range(1, s-1):
        if pow(r, 2 ** i, number) == number - 1:
            return True
    return False


def is_prime(number):
    """
    This function tests for the primality of a number using the Miller-Rabin test. The target number is
    firstly tested against a couple of low primes. The reason behind this resides in the low performance
    and precision of the Miler-Rabin test if the target number can be factorized using at least one low prime.

    :param number: the number to be introduced in the primality test
    :type number: int
    :return: True if the number is prime according to the Miller-Rabin test; False, otherwise
    :rtype: bool
    """
    if number < 2:
        return False
    for prime in low_primes:
        if number % prime == 0:
            return False
    for trial in range(10):
        if not miller_rabin_test(number):
            return False
    return True
