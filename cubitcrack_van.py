# cubitcrack.py
import os
import time
import random
from address_v2 import generateBinSource


clBitCrackPath = 'C:/Users/hermit/Documents/bitcoin/VanitySearch-1.15.4_bitcrack/VanitySearch-1.15.4_bitcrack_th512gr.exe'
bits = 64
one_num_min = 21
one_num_max = 34
addr = '16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN' # '16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN'
seed = random.randrange(0, 10000)
outFile = f'C:/Users/hermit/Documents/bitcoin/boom2_van.txt'
times = pow(10, 7) * 2
maxKey = int(generateBinSource(bits, bits), 2)

def getBatFile():
    seed = random.randrange(0, 10000)
    batFile = f'C:/Users/hermit/Documents/bitcoin/plutus/temp-{seed}.bat'
    if os.path.isfile(batFile):
        return getBatFile()
    return batFile

batFile = getBatFile()

def toArg(stride_iter = 1):
    onenum = random.randrange(round(one_num_min / 3), one_num_max)
    keyspace = int('1' + generateBinSource(bits - 1, onenum), 2)
    result = ''
    strides = random.sample(range(0x01, 0x0f), stride_iter)
    # print(strides)
    for stride in strides:
        offsetStr = stride * times
        if offsetStr + keyspace > maxKey:
            offsetStr = hex(maxKey)
        else:
            offsetStr = f'+{hex(offsetStr)}'
        # offsetStr = maxKey
        result += f'"{clBitCrackPath}" -gpu -t 1 -g 12 --keyspace {hex(keyspace)}:{hex(maxKey)} -o "{outFile}" -stop {addr}\n'
    return result
# print(f'{clBitCrackPath} {addr} -c -u -o out64.txt')

cnt = 1
s_time = time.time()
while True:
    print(f'INFO: bits={bits} round={cnt}, seed={seed} time={time.time() - s_time}')
    with open(batFile, 'w') as file:
        file.truncate()
        file.write(f'{toArg(5)}\n')

    os.system(batFile)
    cnt += 1

print('done')

# clBitCrack.exe -c -u -o out256-000.txt --keyspace %random%%random%%random%%random%:+10000000 16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN