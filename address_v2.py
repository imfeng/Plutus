import itertools
import sys
import random

# for i in itertools.combinations('1101', 4):
#     print (''.join(i),end=' ')

# factorial
def range_prod(lo,hi):
    if lo+1 < hi:
        mid = (hi+lo)//2
        return range_prod(lo,mid) * range_prod(mid+1,hi)
    if lo == hi:
        return lo
    return lo*hi

def treefactorial(n):
    if n < 2:
        return 1
    return range_prod(1,n)

def arrangement(n, m1):
    return treefactorial(n) / ( treefactorial(m1) * treefactorial(n-m1) )

# bits = 256

# for idx in range(0, bits):
#     print(f"{arrangement(bits - 1, idx)}")

# findPermutations

def findPermutations_old(ele):
    length = len(ele)
    if length < 2:
        return ele

    permutationsArray = [] 
    for idx in range(0, length):
        char = ele[idx]

        if ele.index(char) != idx:
            continue
        remainder = ele[:idx] + ele[idx+1:]
        
        for permutation in findPermutations(remainder):
            permutationsArray.append(char + permutation)

    return permutationsArray


def generateBinSource(bits, one_nums, isList = False):
    # startI = bits - one_nums
    # return str.join('', ['0' if idx < startI else '1' for idx in range(bits)])
    startI = bits - one_nums
    l = ['0' if idx < startI else '1' for idx in range(bits)]
    random.shuffle(l)
    # numpy.random.shuffle(l)
    # return l
    return l if isList else str.join('', l)

# print(hex(int('1' + generateBinSource(255, 122), 2)))
# import time
# import numpy as np 

# summ = dict()
# times = 10000000
# for idx in range(0, times):
#     ran = random.randrange(0, 10)
#     if ran in summ:
#         summ[ran] += 1
#     else:
#         summ[ran] = 1
# listr = [] 

# for value in summ.values(): 
#     listr.append(value) 
          
# calculating standard deviation using np.std 
# print(summ )
# print(np.std(listr) )

# old = ''
# cnt = 0
# times = 1
# bits = 63
# capture = 19
# origin = generateBinSource(bits,capture, True)
# start_time = time.time()
# cur_time = start_time
# chunk = 1000000
# duptimes = 0
# for idx in range(0, times):
#     maxDup = 0
#     dbset = set()
#     while True:
#         random.shuffle(origin)
#         new = str.join('', origin)
#         cnt += 1
#         if new in dbset:
#             maxDup += 1
#             duptimes += 1
#             # break
#         else:
#             dbset.add(new)
#         if cnt > chunk * 50:
#             print(f'duptimes={duptimes}, time={round(time.time() - start_time, 2)}')
#             break
#         if cnt % chunk == 0:
#             print(f"total={cnt}, time={round(time.time() - start_time, 2)}, avr={round(1 / ((time.time() - cur_time) / chunk), 2)}, duptimes={duptimes}")
#             cur_time = time.time()
# print(f'END: percent={(cnt/times)/arrangement(bits, capture)} avr={cnt/times}, bits={bits}, capture={capture} max={arrangement(bits, capture)}')
# while True:
# print(cnt)
# for idx in range(0, 5):
#     print(len(findPermutations(generateBinSource(256,idx))))
# for s in findPermutations('1110'):
#     print(hex(int(s, 2)))
# print(sys.argv[1])

def findPermutationsIter(ele):
    length = len(ele)
    if length == 1:
        yield ele
        return

    for idx in range(0, length):
        char = ele[idx]

        if ele.index(char) != idx:
            continue

        yield from (char + rest for rest in findPermutationsIter(ele[:idx] + ele[idx+1:]))
