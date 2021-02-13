import base64
from hashlib import *
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
import enc, time
import csv
import pickle

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

#--pw will not be input by user, rather be generated by hashing the voterID itself. Makes it unique.

def get_private_key(pw='anmol'): #--by default the password is anmol
    password = str(sha256((pw).encode('utf-8')).hexdigest())
    salt = b"this is a salt and the m0re c0mplex th!s wi11 be, the m0re d!44icult w1!! b3 the K37"
    #--Password Based Key Derivation Function 2 (PBKDF2)
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key


def encrypt(raw, private_key):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, private_key):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

if __name__=='__main__':
    key = get_private_key('sdgssdgs')
    ms = 'anmol'
    lock = encrypt(ms,key)
    print(lock)
    print(decrypt(lock,key))
