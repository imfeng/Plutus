import sys
import os
from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey
from binascii import hexlify
import time
import multiprocessing
import random

from hex2bin import getRanNumByWeight, pool_weight_high, pool_weight_low
# from numba import cuda
# print(cuda.gpus)
total_bytes = 8
targetW = '16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN' # '16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN' # 64addr
permutation_oneNums = 19
# print(f'')
boomFile = 'C:/Users/hermit/Documents/bitcoin/plutus/boom.txt'
start_p = int('80', 16)
end_p = int('FF', 16) + 1
bytes_num = total_bytes - 1
# chunk = (end_p - start_p) * 100
chunk = 100000


def init():
    setup('mainnet')

def pri2addr(secret_exponent, target, _boomFile = boomFile):
    priv = PrivateKey(secret_exponent = int(secret_exponent, 16))
    pub = priv.get_public_key()
    address = pub.get_address().to_string()
    if address == target:
        print('boom: ' + address)
        with open(_boomFile, 'a') as file:
            file.write('hex private key: ' + str(secret_exponent) + '\n' + 'WIF private key: ' + str(priv.to_wif(compressed=True)) + '\n' + 'public key: ' + str(pub.to_hex(compressed=True)) + '\n' + 'address: ' + str(address) + '\n\n')
            file.close()
        return True
    return False

def priDec2addr(int_secret, target, _boomFile = boomFile):
    priv = PrivateKey(secret_exponent = int_secret)
    pub = priv.get_public_key()
    address = pub.get_address().to_string()
    if address == target:
        print('boom: ' + address)
        with open(_boomFile, 'a') as file:
            file.write(f'strategy:{strategy}\n')
            file.write('dec private key: ' + str(int_secret) + '\n' + 'WIF private key: ' + str(priv.to_wif(compressed=True)) + '\n' + 'public key: ' + str(pub.to_hex(compressed=True)) + '\n' + 'address: ' + str(address) + '\n\n')
            file.close()
        return True
    return False

def tester():
    init()
    if not pri2addr('03', '1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb', boomFile.replace('.txt', '_t.txt')):
        print('pri2addr: test failed!')
    if not pri2addr('07', '19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA', boomFile.replace('.txt', '_t.txt')):
        print('pri2addr: test failed!')
    if not priDec2addr(3, '1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb', boomFile.replace('.txt', '_t.txt')):
        print('priDec2addr: test failed!')
    if not priDec2addr(7, '19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA', boomFile.replace('.txt', '_t.txt')):
        print('priDec2addr: test failed!')

def starter_random(cpuId):
    isStop = False
    start_time = time.time()
    cur_time = start_time
    cnt = 0
    while not isStop:
        ran = hexlify(os.urandom(bytes_num)).decode('utf-8')
        for idx in range(start_p, end_p):
            cnt += 1
            if pri2addr(str(hex(idx)) + ran, targetW):
                isStop = True
                break
        if cnt % chunk == 0:
            print(f"{cpuId}: total={cnt}, time={round(time.time() - start_time, 2)}, avr={round(chunk / (time.time() - cur_time), 2)}")
            cur_time = time.time()

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

def generateBinSource(bits, startI):
    # startI = bits - one_nums
    # return str.join('', ['0' if idx < startI else '1' for idx in range(bits)])
    # startI = bits - one_nums
    l = ['0' if idx < startI else '1' for idx in range(bits)]
    random.shuffle(l)
    return str.join('', l)


def starter_permutation(cpuId, one_nums, ran_one = False):
    isStop = False
    start_time = time.time()
    cur_time = start_time
    cnt = 0
    bits = total_bytes * 8 - 1
    start_bin_pri = generateBinSource(total_bytes * 8 - 1, bits - one_nums)
    permuGen = findPermutations(start_bin_pri)
    while not isStop:
        try:
            cnt += 1
            perStr = next(permuGen)
            if priDec2addr(int('1' + perStr, 2), targetW):
                isStop = True
                print(f"BOOM! {cpuId}: total={cnt}, time={round(time.time() - start_time, 2)}, avr={round(1 / ((time.time() - cur_time) / chunk), 2)}")
                return True

            if cnt % chunk == 0:
                if ran_one:
                    one_nums = random.randrange(21, 37)
                    cpuId = f'R{one_nums}'
                start_bin_pri = generateBinSource(total_bytes * 8 - 1, bits - one_nums)
                permuGen = findPermutations(start_bin_pri)
                print(f"{cpuId}: total={cnt}, time={round(time.time() - start_time, 2)}, avr={round(1 / ((time.time() - cur_time) / chunk), 2)},\t") # s_bin={start_bin_pri}
                cur_time = time.time()

        except StopIteration:
            print(f'{cpuId}: ALL DONE,one_nums={one_nums} total={cnt}, time={round(time.time() - start_time, 2)}')
            if not ran_one:
                isStop = True
                break

    return False

def starter_shuffle(cpuId, one_nums):
    init()
    isStop = False
    start_time = time.time()
    cur_time = start_time
    cnt = 0
    bits = total_bytes * 8 - 1
    startI = bits - one_nums

    while not isStop:
        # l1_time_s = time.time()
        # random.shuffle(l)
        # rdn = str.join('', l)

        rdn = getRanNumByWeight(pool_weight_low, bits) # str.join('', l)
        # rdn = generateBinSource(bits, startI) # str.join('', l)
        # l1_sum += time.time() - l1_time_s
        # 2.1416917443275453e-05s

        # l2_time_s = time.time()
        if priDec2addr(int('1' + rdn, 2), targetW):
            isStop = True
            break
        # l2_sum += time.time() - l2_time_s
        # 0.0006027315184473992s

        if cnt % chunk == 0:
            print(f"{strategy}: total={cnt}, time={round(time.time() - start_time, 2)}, avr={round(1 / ((time.time() - cur_time) / chunk), 2)}")
            cur_time = time.time()

        cnt += 1

def starter_shuffle_addrs(cpuId, one_nums):
    filepath = 'D:/bitcoin/address.tsv'
    stime = time.time()
    addr_list = set()
    with open(filepath, 'r') as file:
        line = file.readline()
        while True:
            line = file.readline()
            if not line:
                break
            addr_list.add(line.split("\t")[0])
    print(f'loadAddress {filepath}: {time.time() - stime}s')
    
    isStop = False
    start_time = time.time()
    cur_time = start_time
    cnt = 0
    bits = 256 - 1
    startI = bits - one_nums
    l = ['0' if idx < startI else '1' for idx in range(bits)]
    while not isStop:
        random.shuffle(l)
        int_secret = int('1' + str.join('', l), 2)
        priv = PrivateKey(secret_exponent = int_secret)
        pub = priv.get_public_key()
        address = pub.get_address().to_string()
        address_old = pub.get_address(compressed=False).to_string()
        if address in addr_list or address_old in addr_list:
            print('boom: ' + int_secret)
            with open(boomFile, 'a') as file:
                file.write('dec private key: ' + str(hex(int_secret)) + '\n' + 'WIF private key: ' + str(priv.to_wif(compressed=True)) + '\n' + 'public key: ' + str(pub.to_hex(compressed=True)) + '\n' + 'address: ' + str(address) + '\n\n')
                file.close()
            break

        if cnt != 0 and cnt % chunk == 0:
            print(f"starter_shuffle_addrs {cpuId}: total={cnt}, time={round(time.time() - start_time, 2)}, avr={round(1 / ((time.time() - cur_time) / chunk), 2)}")
            cur_time = time.time()
        cnt += 1

strategy = 'starter_shuffle + pool_weight_low'
if __name__ == "__main__":
    cmd_cpuId = '0' if sys.argv[1] is None else sys.argv[1]
    cmd_type = 'random' if sys.argv[2] is None else sys.argv[2]
    permutation_oneNums = int(cmd_type)
    print(f'cmd_cpuId={cmd_cpuId}, cmd_type={cmd_type}')
    print(f'total_bytes={total_bytes},\ntargetW={targetW}\npermutation_oneNums={permutation_oneNums}')
    tester()

    # starter_permutation(permutation_oneNums, permutation_oneNums, True)
    starter_shuffle(permutation_oneNums, permutation_oneNums)

    # for idx in range(57, 60):
    #     if starter_permutation(idx, idx):
    #         break
    # if cmd_type == 'random':
    # starter_random(cmd_cpuId)
    # starter_shuffle_addrs(cmd_cpuId, permutation_oneNums)
        # priDec2addr(int('111111001101110100000110011000110010010001110111110100001001101001011011000100000111001000100011100110000010110011100011101101100100011001111011010011110000011111001011010011011100111101101101001000100111000011011110011111101111011110101001000000011100', 2), '17R5GPpTiaFQknekab6BVf7Nb2qyP9dR2y')
    # priv = PrivateKey(secret_exponent = int('0FCDD06632477D09A5B107223982CE3B6467B4F07CB4DCF6D2270DE7EF7A901C', 16))
    # pub = priv.get_public_key()
    # address = pub.get_address(compressed=False).to_string()
    # print(address)


    # for idx in range(10000000):
    #     s = hexlify(os.urandom(bytes_num)).decode('utf-8')
    #     if len(s) < 14:
    #         print('gg')
    # for idx in range(5):
    #     numb = random.randrange(19, 34)
    #     multiprocessing.Process(target=starter_shuffle, args=(numb, numb)).start()
