# starter_shuffle_addrs.py
import sys
import os
from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey
import time
import multiprocessing
import random

cpus = 3
# filepath = 'D:/bitcoin/P2PKH-1'
filepath = 'D:/bitcoin/adrs.txt'
boomFile = 'C:/Users/hermit/Documents/bitcoin/plutus/boom.txt'
chunk = 100000
bits = 256 - 1
targetW = '16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN'

def init():
    setup('mainnet')

def get_int_secret(arr):
    return int('1' + str.join('', arr), 2)

def generateBinSource(bits, startI):
    l = ['0' if idx < startI else '1' for idx in range(bits)]
    random.shuffle(l)
    return str.join('', l)

# permutate
def findPermutations(ele):
    length = len(ele)
    if length == 1:
        yield ele
        return

    for idx in range(0, length):
        char = ele[idx]

        if ele.index(char) != idx:
            continue

        yield from (char + rest for rest in findPermutations(ele[:idx] + ele[idx+1:]))

def getAddress(int_secret):
    priv = PrivateKey(secret_exponent = int_secret)
    pub = priv.get_public_key()
    address = pub.get_address().to_string()
    # address_old = pub.get_address(compressed=False).to_string()
    return address

def starter_shuffle_addrs(one_nums, permute = 0):
    init()
    isStop = False
    start_time = time.time()
    cur_time = start_time
    cnt = 0
    startI = bits - one_nums
    l = ['0' if idx < startI else '1' for idx in range(bits)]
    tmp_cnt_permute = 0
    perGen = findPermutations(str.join('', l))
    while not isStop:
        try:
            ran = next(perGen)
        except StopIteration:
            tmp_cnt_permute = 0
            print(f'ERROR: StopIteration! permute={permute}')
        # if permute > 0:
        #     if tmp_cnt_permute > permute:
        #         tmp_cnt_permute = 0

        #     if tmp_cnt_permute == 0:
        #         random.shuffle(l)
        #         perGen = findPermutations(str.join('', l))
        #         tmp_cnt_permute = 0
            
        #     if tmp_cnt_permute < permute:
        #         tmp_cnt_permute += 1
        #         try:
        #             ran = next(perGen)
        #         except StopIteration:
        #             tmp_cnt_permute = 0
        #             print(f'ERROR: StopIteration! permute={permute}')
        # else:
        #     random.shuffle(l)
        #     ran = str.join('', l)

        cnt += 1
        addrs = getAddress(int('1' + ran, 2))
        
        if address in addr_list or address_old in addr_list:
            prinum = str(hex(int_secret))
            print('boom: ' + prinum)
            with open(boomFile, 'a') as file:
                file.write('total: ' + str(cnt) + '\n' + 'hex private key: ' + prinum + '\n' + 'WIF private key: ' + str(priv.to_wif(compressed=True)) + '\n' + 'public key: ' + str(pub.to_hex(compressed=True)) + '\n' + 'address: ' + str(address) + '\n\n')
                file.close()

        if cnt != 0 and cnt % chunk == 0:
            print(f"starter_shuffle_addrs: one_nums={one_nums}, total={cnt}, time={round(time.time() - start_time, 2)}, avr={round(1 / ((time.time() - cur_time) / chunk), 2)}")
            cur_time = time.time()

def starter_permutation(one_nums):
    init()
    isStop = False
    start_time = time.time()
    cur_time = start_time
    cnt = 0
    start_bin_pri = generateBinSource(bits, bits - one_nums)
    permuGen = findPermutations(start_bin_pri)
    while not isStop:
        try:
            cnt += 1
            rankey = int('1' + next(permuGen), 2)
            addrs = getAddress(rankey)

            # if addrs in addr_list:
            if addrs in addr_list:
                prinum = str(hex(rankey))
                print('boom: ' + prinum)
                with open(boomFile, 'a') as file:
                    file.write(f'total:{str(cnt)}\n\tprikey: {prinum}\n\taddrs: {addrs}\n\n')

            if cnt % chunk == 0:
                print(f"starter_shuffle_addrs: total={cnt}, one_nums={one_nums}, time={round(time.time() - start_time, 2)}, avr={round(1 / ((time.time() - cur_time) / chunk), 2)}")
                one_nums = random.randrange(round(bits/2)-5, round(bits/2)+5)
                start_bin_pri = generateBinSource(bits, bits - one_nums)
                permuGen = findPermutations(start_bin_pri)
                cur_time = time.time()

        except StopIteration:
            print(f'starter_shuffle_addrs: ALL DONE,one_nums={one_nums} total={cnt}, time={round(time.time() - start_time, 2)}')
            isStop = True
            break

    return False

# manager = multiprocessing.Manager()
# shared_dict = manager.dict()
# # addr_list = set()
addr_list = set()
stime = time.time()
with open(filepath, 'r') as file:
    while True:
        line = file.readline().strip()
        if not line:
            break
        addr_list.add(line)
print(f'loadAddress {filepath}: {time.time() - stime}s')

if __name__ == "__main__":
    one_nums = 1 if sys.argv[1] is None else sys.argv[1]
    permutation_oneNums = int(one_nums)
    print(f'permutation_oneNums={permutation_oneNums}')

    starter_permutation(permutation_oneNums)
    # starter_shuffle_addrs(permutation_oneNums, 20000)

    # for idx in range(0, cpus):
        # multiprocessing.Pool.apply_async(target=starter_shuffle_addrs, args=(permutation_oneNums + idx)).start()
        # multiprocessing.Process(target=starter_shuffle_addrs, args=(permutation_oneNums + idx, addr_list)).start()
    # a = multiprocessing.Process(target=test, args=(shared_dict, 1))
    # b = multiprocessing.Process(target=test, args=(shared_dict, 2))
    # a.start()
    # b.start()
    # a.join()
    # b.join()
    # print(shared_dict)

