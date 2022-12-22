# This module works with binary representations of numbers
import math
import sha256


def mgf(mask_length, seed):  # seed is assumed to be an integer
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
