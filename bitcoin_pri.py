# bitcoin_pri.py
from ecdsa import SigningKey, VerifyingKey, SECP256k1, ellipticcurve, numbertheory
from binascii import unhexlify, hexlify

def get_public_key(secret_exponent):
    """Returns the corresponding PublicKey"""
    key = SigningKey.from_secret_exponent(secret_exponent, curve=SECP256k1)

    verifying_key = hexlify(key.get_verifying_key().to_string())
    return PublicKey( '04' + verifying_key.decode('utf-8') )

def get_address(self, compressed=True):
    """Returns the corresponding P2PKH Address (default compressed)"""

    hash160 = self._to_hash160(compressed)
    addr_string_hex = hexlify(hash160).decode('utf-8')
    return P2pkhAddress(hash160=addr_string_hex)
    
def _to_hash160(self, compressed=True):
    """Returns the RIPEMD( SHA256( ) ) of the public key in bytes"""

    pubkey = unhexlify( self.to_hex(compressed) )
    hashsha256 = hashlib.sha256(pubkey).digest()
    hashripemd160 = hashlib.new('ripemd160')
    hashripemd160.update(hashsha256)
    hash160 = hashripemd160.digest()
    return hash160
print(get_public_key(1))