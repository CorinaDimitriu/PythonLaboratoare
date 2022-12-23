"""
# This module works with binary representations of numbers and outputs masks of given size starting from given seed.
"""
import math
import sha256


def mgf(mask_length: int, seed: int) -> str:
    """
    This is a mask generation function (mgf) based on sha-256 hash function.
    Essentially, the seed is given to the hash function. This operation repeats
    multiple times, while a counter is increasing at every step in order to be concatenated
    to the seed before hashing. It is well known that slightly different messages usually
    produce totally different hashes, so the counter is used to *randomize* the seed.

    :param mask_length: the desired length of the mask (usually the mask is going to be
        xored with some other cryptographic input, so the two must be equally large)
    :type mask_length: int
    :param seed: random number given to the hash function
    :type seed: int
    :return: generated mask of exactly mask_length bits, starting from given seed, as octet string
    :rtype: str
    :raises TypeError: when the seed is not of integer type
    """
    if type(seed) != int:
        raise TypeError("Seed must have integer type, in order "
                         "to be converted using I2OSP")
    seed = str(bin(seed))[2:]
    hLen = 256
    T = ""
    for counter in range(0, math.ceil(mask_length/hLen)):
        C = str(bin(counter))[2:]
        C = ''.join(['0' for _ in range(32 - len(C))]) + C
        T += sha256.execute_sha256(seed + C)
        counter += 1
    return T[:mask_length]
