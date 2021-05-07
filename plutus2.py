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

DATABASE = r'database/MAR_23_2019/'

def generate_private_key_by_str(passphrase): 
	return sha256(passphrase.encode('utf-8')).hexdigest().upper()

def generate_private_key(): 
	"""
	Generate a random 32-byte hex integer which serves as a randomly 
	generated Bitcoin private key.
	Average Time: 0.0000061659 seconds
	"""
	# addr = binascii.hexlify(os.urandom(32)).decode('utf-8').upper()
	seed = 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks hash'
	# addr = binascii.hexlify(os.urandom(32)).decode('utf-8').upper()
	# passphrase = 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU74sHUHy8S'
	# addr = sha256(seed.encode('utf-8')).hexdigest().upper()
	# addr = 'b190e2d40cfdeee2cee072954a2be89e7ba39364'.upper()
	# print(addr)
	# addr = binascii.hexlify(hexlify(seed.encode())).decode('utf-8').upper()
	# addr = '03'.decode('utf-8').upper()
	addr = binascii.hexlify(bytearray.fromhex('03')).decode('utf-8').upper()
	print(addr)

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
	# return '0104' + pk.publicKey().toString().hex().upper()
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

def process(private_key, public_key, address, database):
	"""
	Accept an address and query the database. If the address is found in the 
	database, then it is assumed to have a balance and the wallet data is 
	written to the hard drive. If the address is not in the database, then it 
	is assumed to be empty and printed to the user.
	Average Time: 0.0000026941 seconds
	"""
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

def main(database):
	"""
	Create the main pipeline by using an infinite loop to repeatedly call the 
	functions, while utilizing multiprocessing from __main__. Because all the 
	functions are relatively fast, it is better to combine them all into 
	one process.
	"""
	# times = 1
	# while True:
	private_key = generate_private_key()			# 0.0000061659 seconds
	public_key = private_key_to_public_key(private_key) 	# 0.0031567731 seconds
	address = public_key_to_address(public_key)		# 0.0000801390 seconds
	print(private_key_to_WIF(public_key))
	process(private_key, public_key, address, database) 	# 0.0000026941 seconds
	time.sleep(0.05)
									# --------------------
									# 0.0032457721 seconds
		# times -= 1

def cus_main(database, source):
	every = 10000
	total = len(database[source])
	print(f'({source}) total files: {total}')
	num = 0
	start_time = time.time()
	for passphrase in database[source]:
		private_key = generate_private_key_by_str(passphrase.strip())
		public_key = private_key_to_public_key(private_key)
		address = public_key_to_address(public_key)
		process(private_key, public_key, address, database)
		num += 1
		if num % every == 0:
			sec = round(time.time() - start_time, 5)
			print(f'({source}) done: num={num} seconds={sec}, avg={round(sec/num, 5)}')
			start_time = time.time()
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
	# for c, p in enumerate(os.listdir(DATABASE)):
	# 	print('\rreading database: ' + str(c + 1) + '/' + str(count), end = ' ')
	# 	with open(DATABASE + p, 'rb') as file:
	# 		if c < half:
	# 			if c < quarter: database[0] = database[0] | pickle.load(file)
	# 			else: database[1] = database[1] | pickle.load(file)
	# 		else:
	# 			if c < half + quarter: database[2] = database[2] | pickle.load(file)
	# 			else: database[3] = database[3] | pickle.load(file)
	# print('DONE')
	main(database)

	# # To verify the database size, remove the # from the line below
	# #print('database size: ' + str(sum(len(i) for i in database))); quit()
	# cus_main(database)
	# for cpu in range(multiprocessing.cpu_count()):
	# 	# multiprocessing.Process(target = main, args = (database, )).start()
	# multiprocessing.Process(target = cus_main, args = (database, 0)).start()
	# multiprocessing.Process(target = cus_main, args = (database, 1)).start()
	# multiprocessing.Process(target = cus_main, args = (database, 2)).start()
	# multiprocessing.Process(target = cus_main, args = (database, 3)).start()

