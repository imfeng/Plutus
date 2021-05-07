# random_test.py
# import numpy as np
import multiprocessing
import random
import time
from address_v2 import arrangement, findPermutationsIter

_log_avr_num = 100000
# from multiprocessing import shared_memory,
# from multiprocessing import shared_memory
# numrange = [0 , 10]
# dd = np.array([0 for i in range(numrange[0], numrange[1])])
# shm = shared_memory.SharedMemory(create=True, size=dd.nbytes)
# c = np.ndarray((6,), dtype=np.int64, buffer=existing_shm.buf)

# def gRandom(dd):
#     r = random.randrange(numrange[0], numrange[1])
#     dd[0] += 1
#     return dd

# if __name__ == "__main__":

#     for idx in range(5):
#         multiprocessing.Process(target=gRandom, args=(dd, )).start()
#         # time.sleep(5)
#     print(dd)

# result = len(list(findPermutations("1001011111111111101001011")))

# a = (6,6)
# print(6 in [7, 9])

def log_avr(name, cnt, start_time):
    print(f'{name}: avr={cnt / (time.time() - start_time)}')

def generateBinSource(bits, startI):
    l = ['0' if idx < startI else '1' for idx in range(bits)]
    random.shuffle(l)
    return str.join('', l)


def guess_single(bits, one_nums, addr_target, times = 1):
    min_num = 1 << 256
    max_num = -1
    total_num = 0
    total_time = 0
    for _ in range(0, times):
        t = time.time()
        cnt = 0
        while True:
            cnt += 1
            addr = generateBinSource(bits, random.randrange(ranStart, ranEnd))
            if addr_target == addr:
                time_end = time.time() - t
                min_num = min(min_num, cnt)
                max_num = max(max_num, cnt)
                total_num += cnt
                total_time += time_end
                break
            # if cnt % _log_avr_num == 0:
            #     log_avr('guess_single', cnt, t)
    return {
        'cnt': cnt,
        'min_num': min_num,
        'max_num': max_num,
        'total_num': total_num,
        'total_time': total_time
    }

def guess_chunk(bits, one_nums, addr_target, chunk = 10, times = 1):
    min_num = 1 << 256
    max_num = -1
    total_num = 0
    total_time = 0
    for _ in range(0, times):
        t = time.time()
        cnt = 0
        while True:
            if cnt % chunk == 0:
                binSource = generateBinSource(bits, random.randrange(ranStart, ranEnd))
                ranGen = findPermutationsIter(binSource)
            try:
                addr = next(ranGen)
                cnt += 1
                if addr_target == addr:
                    time_end = time.time() - t
                    min_num = min(min_num, cnt)
                    max_num = max(max_num, cnt)
                    total_num += cnt
                    total_time += time_end
                    break
                # if cnt % _log_avr_num == 0:
                #     log_avr('guess_chunk', cnt, t)
            except StopIteration:
                print('WARN: Out Permutations')

            
    return {
        'cnt': cnt,
        'min_num': min_num,
        'max_num': max_num,
        'total_num': total_num,
        'total_time': total_time
    }

def processComp(gss):
    avr_num = round(gss['total_num'] / times, 2)
    min_num = round(gss['min_num'], 2)
    max_num = round(gss['max_num'], 2)
    avr_time = round(gss['total_time'] / times, 2)

    expt = sum([arrangement(bits, one_nums) for one_nums in range(ranStart, ranEnd)])
    minP = round(min_num/expt * 100, 3)
    maxP = round(max_num/expt * 100, 3) 
    print( \
f'{expt}  \t{avr_num}   \t{min_num}   \t{minP}%  \t{maxP}%  \t{max_num}  \t{avr_time}')


confidence_rate = 0.17
bits = 16 # 64 -> 32,33  ->  21~44
one_nums = 9 # 16 -> 13,13.25 -> 5 ~ 11
times = 100
target = generateBinSource(bits, bits - one_nums)

mid = round(bits / 2)
confidence = round(bits * confidence_rate) # round(bits * 0.34)
ranStart = mid - confidence
ranEnd = mid + confidence
print(f'confidence={confidence}, one_num={one_nums}, ranStart={ranStart}, ranEnd={ranEnd}')

print(f'expect   \tavr_num   \tmin_num   \tminP   \tmaxP   \tmax_num   \tavr_time')
processComp(guess_single(bits, one_nums, target, times))
processComp(guess_chunk(bits, one_nums, target, 100, times))
# sgwin = 0
# for idx in range(0, 10000):
#     target = generateBinSource(bits, bits - one_nums)
#     sg = guess_single(bits, one_nums, target, times)
#     sc = guess_chunk(bits, one_nums, target, 100, times)
#     if sg['min_num'] < sc['min_num']:
#         sgwin += 1
# print(f'sgwin={sgwin}')

# total = 0
# cnt = 0
# for idx in range(1, 1000000):
#     n = random.randrange(1, 7)
#     total += n
#     if n == 1:
#         cnt += 1
#     if idx % 100000 == 0:
#         print(f'{idx}: 3np={round(cnt/idx, 4)} cnt={cnt}, p={round(total / idx, 4)}')
#         time.sleep(5)

    