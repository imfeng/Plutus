# hex2bin.py
import binascii
import random
import time
import collections

def hex2bin():
        
    bits = 64
    with open('btc32_pri.txt', 'r') as rfile:
        with open('btc32_pri_b.txt', 'w') as wf:
            while True:
                line = rfile.readline().strip()
                if not line:
                    break
                wf.write(f'{int(line, 16):0>64b}\n')

hex2bin()

def onetByIndex():
    cntlist = [0 for idx in range(0, 64)]
    with open('btc32_pri_b.txt', 'r') as rfile:
        while True:
            line = rfile.readline().strip()
            if not line:
                break
            for idx, num in enumerate(line):
                if num == '1':
                    cntlist[idx] += 1
    return cntlist
def calcPercent(cntlist):
    plist = [-1 for idx in range(0, 64)]
    for idx, cnt in enumerate(cntlist):
        if idx == 0:
            continue
        plist[idx] = f'{round(round(cnt / idx, 4) * 100, 2)}%'
    return plist
            

# cntlist = onetByIndex()
# plist = calcPercent(cntlist)
# print(cntlist)
# print(plist)
# print(n.zfill(3))


def times_linear(pool_dict, cnt):
    pool = pool_dict.copy()
    sum_weight = sum(pool)
    rst = []
    for _ in range(cnt):
        n = random.randint(1, sum_weight)
        for binIdx, weight in enumerate(pool):
            if n <= weight:
                rst.append(binIdx)
                sum_weight -= weight
                del pool[binIdx]
                break
            else:
                n -= weight
    return rst
def times_linear_one(pool_dict):
    pool = pool_dict.copy()
    sum_weight = sum(pool)
    rst = []
    n = random.randint(1, sum_weight)
    for binIdx, weight in enumerate(pool):
        if n <= weight:
            return binIdx
        else:
            n -= weight
    return 0
# print(times_linear(pool_dict, 2))

pool_weight_high = [5000,5000,5000,5000,5000,5000,5714,7500,7778,4000,2727,7500,4615,5714,5333,1875,6471,7222,5263,6500,6667,5909,3043,6250,4400,5385,5926,4643,4828,5667,5484,5313,3939,5588,5143,5000,5676,6053,5385,5500,5366,4286,4186,4773,5778,4783,5106,4375,4490,5800,4902,5962,5283,4444,4545,3750,5439,3966,5254,4833,6066,4677,4921,]
pool_weight_low = [5000,5000,5000,5000,5000,5000,4286,2500,2222,6000,7273,2500,5385,4286,4667,8125,3529,2778,4737,3500,3333,4091,6957,3750,5600,4615,4074,5357,5172,4333,4516,4688,6061,4412,4857,5000,4324,3947,4615,4500,4634,5714,5814,5227,4222,5217,4894,5625,5510,4200,5098,4038,4717,5556,5455,6250,4561,6034,4746,5167,3934,5323,5079,]
maxP = 10000
# pool_dict = [50, 50, 30, 40]

# bits = 63

# amt = 0
# num_min = 1 << 256
# num_max = -1

# times = 100000
# cntlist = [0 for i in range(0, bits)]

# for _ in range(0, times):
#     rlist = [0 for i in range(0, bits)]
#     for idx, n in enumerate(rlist):
#         zOr1 = times_linear_one([maxP-pool_weight_high[idx], pool_weight_high[idx]])
#         rlist[idx] = zOr1
#     cnt = rlist.count(1)
#     cntlist[cnt-1] += 1
#     amt += cnt
#     num_min = min(num_min, cnt)
#     num_max = max(num_max, cnt)
# print(f'avr={amt / times}, min={num_min}, max={num_max}')
# print(cntlist)


def getRanNumByWeight(pool_weight, bits):
    rlist = ['0' for i in range(0, bits)]
    for idx in range(0, bits):
        zOr1 = times_linear_one([maxP-pool_weight_high[idx], pool_weight_high[idx]])
        rlist[idx] = str(zOr1)        
    return ''.join(rlist)
