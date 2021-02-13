import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import pickle
import pdb
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

#Creating Private Key of 1024 bits and Public Key
def enc_rsakeys():
    length=1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey, publickey


#function for encryption which takes public key, plain text as arguments. This function returns a base64 encoded string of ciphertext.
def enc_encrypt(rsa_publickey,plain_text):
    encryptor = PKCS1_OAEP.new(rsa_publickey)
    encrypted = encryptor.encrypt(plain_text)
    return encrypted
    # cipher_text=rsa_publickey.encrypt(plain_text,32)[0]
    # b64cipher=base64.b64encode(cipher_text)
    # return b64cipher


#For decryption, we create a function that takes ciphertext and private key as arguments.
def enc_decrypt(rsa_privatekey,b64cipher):
    decryptor = PKCS1_OAEP.new(rsa_privatekey)
    decrypted = decryptor.decrypt(b64cipher)
    return decrypted
    # decoded_ciphertext = base64.b64decode(b64cipher)
    # plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
    # return plaintext


#Function sign takes two arguments, private key and data. This function returns base64 string of digital signature.
def enc_sign(privatekey,data):
    h = SHA256.new(data)
    return pkcs1_15.new(privatekey).sign(h)


#Function verify takes two arguments, public key and digital signature in base64 and returns a boolean True if signature matches the data, False if not matches data.
def enc_verify(publickey,data,sign):
    h = SHA256.new(data)
    try:
        pkcs1_15.new(publickey).verify(h, sign)
        return True
    except (ValueError, TypeError):
        return False

# sk,pk = rsakeys()
# e = encrypt(pk, b'sadman')
# print(e)
# print(decrypt(sk, e))
# msg = b'dafs'
# locked = sign(sk,msg)
# print(locked)
# print(verify(pk, b'sadman', locked))