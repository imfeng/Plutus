# cubitcrack.py
import os
import time
import random
from address_v2 import generateBinSource


clBitCrackPath = 'C:/Users/hermit/Documents/bitcoin/cuBitCrack.exe'
bits = 64
one_num_min = 21
one_num_max = 31
addr = '16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN' # 64 '16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN'
seed = random.randrange(0, 10000)
outFile = f'C:/Users/hermit/Documents/bitcoin/boom64.txt'
times = pow(10, 8) * 2
maxKey = int(generateBinSource(bits, bits), 2)

def passImpossible(hexstr):
    temp = None
    cnt = 0
    zerocnt = 0
    for st in hexstr[:-6]:
        if st == temp:
            cnt += 1
        if st == '0':
            zerocnt += 1
        temp = st
    return cnt > 6 or zerocnt > 6
    # return False
    # return True

def getBatFile():
    seed = random.randrange(0, 10000)
    batFile = f'C:/Users/hermit/Documents/bitcoin/plutus/temp-{seed}.bat'
    if os.path.isfile(batFile):
        return getBatFile()
    return batFile

def saveWork(start, end):
    saveFile = f'C:/Users/hermit/Documents/bitcoin/work_bit64.bat'
    with open(saveFile, 'a') as file:
        file.write(f'{start}-{end}\n')    

batFile = getBatFile()

def getKeySpace(bits, onenum):
    cnt = 0
    while True:
        cnt += 1
        keyspace = hex(int('1' + generateBinSource(bits - 1, onenum), 2))
        if cnt > 100:
            print(keyspace)
        if not passImpossible(keyspace[2:]):
            break
    return keyspace

def toArgBitCrack(stride_iter = 1):
    num16 = 8
    mask = (pow(2, num16 * 4) - 1) << num16 * 4
    onenum = random.randrange(one_num_min, one_num_max)
    keyspace = hex(int(getKeySpace(bits, onenum), 16) & mask)
    result = ''
    # strides = random.sample(range(0x01, 0x0f), stride_iter)
    offsetStr = (pow(16, num16) - 1) + int(keyspace, 16)
    if offsetStr > maxKey:
        offsetStr = hex(maxKey)
    else:
        offsetStr = hex(offsetStr)
    # offsetStr = maxKey
    saveWork(keyspace, offsetStr)
    result += f'{clBitCrackPath} {addr} --keyspace {keyspace}:{offsetStr} -o {outFile} -b 64\n' #  --stride {hex(stride)}
    return result
# print(f'{clBitCrackPath} {addr} -c -u -o out64.txt')

mask = (pow(2, 120) - 1) << 60
def toArgKangaroo(bits = 120, pub = '02ceb6cbbcdbdf5ef7150682150f4ce2c6f4807b349827dcdbdd1f2efa885a2630', maxKey = '0xffffffffffffffffffffffffffffff'):
    onenum = random.randrange(one_num_min + 11, one_num_max + 11)
    print(f'INFO: bits={bits}, round={cnt}, onenum={onenum}, seed={seed} time={time.time() - s_time}')

    keyspace = hex(int(getKeySpace(bits, onenum), 16) & mask)
    result = ''
    offsetStr = (pow(16, 15) - 1) + int(keyspace, 16)
    if offsetStr > int(maxKey, 16):
        offsetStr = maxKeyz
    else:
        offsetStr = hex(offsetStr)
    with open(f'C:/Users/hermit/Documents/bitcoin/in120-{seed}.txt', 'w') as file:
        file.write(keyspace[2:])
        file.write('\n')
        file.write(offsetStr[2:])
        file.write('\n')
        file.write(pub)
        # file.write('60f4d11574f5ddee49961d9609ac6') # 60f4d11574f5deee49961d9609ac6
        # file.write('\n')
        # file.write('60f4d11574f5dfee49961d9609ac6')
        # file.write('\n')
        # file.write('0248d313b0398d4923cdca73b8cfa6532b91b96703902fc8b32fd438a3b7cd7f55')
    result = f'"C:/Users/hermit/Documents/bitcoin/Kangaroo.exe" -gpu -t 0 -m 1 -o "C:/Users/hermit/Documents/bitcoin/boom_120.txt" "C:/Users/hermit/Documents/bitcoin/in120-{seed}.txt"\n' 
    return result

cnt = 1
s_time = time.time()
while True:
    with open(batFile, 'w') as file:
        file.truncate()
        # file.write(f'{toArgKangaroo()}\n')
        file.write(f'{toArgBitCrack(1)}\n')

    os.system(batFile)
    cnt += 1

print('done')

# clBitCrack.exe -c -u -o out256-000.txt --keyspace %random%%random%%random%%random%:+10000000 16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN