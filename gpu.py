import numpy
from numba import jit
import random
import time

from ecdsa import SigningKey, VerifyingKey, SECP256k1, ellipticcurve, numbertheory
from ecdsa.util import sigencode_string, sigdecode_string, sigencode_der
from binascii import unhexlify, hexlify

@jit(nopython=True)
def GPUgenerateBinSource(bits, one_nums, isList = False):
    startI = bits - one_nums
    arr = numpy.array([0 if idx < startI else 1 for idx in range(bits)])
    numpy.random.shuffle(arr)
    return arr
def generateBinSource(bits, one_nums, isList = False):
    startI = bits - one_nums
    arr = numpy.array([0 if idx < startI else 1 for idx in range(bits)])
    numpy.random.shuffle(arr)
    return arr

@jit(nopython=True)
def get_public_key(secret_exponent):
    """Returns the corresponding PublicKey"""
    key = SigningKey.from_secret_exponent(secret_exponent, curve=SECP256k1)

    verifying_key = hexlify(key.get_verifying_key().to_string())
    pri = '04' + verifying_key.decode('utf-8')
    return pri
    # return PublicKey( '04' + verifying_key.decode('utf-8') )

# print(get_public_key(3))
# print(numpy.frombuffer(numpy.random.bytes(10), dtype=numpy.uint32))
# tt = time.time()
# for idx in range(0,100000):
#     generateBinSource(64, 19)
# print(f'time={time.time() - tt}')

# tt = time.time()
# for idx in range(0,100000):
#     GPUgenerateBinSource(64, 19)
# print(f'time={time.time() - tt}')