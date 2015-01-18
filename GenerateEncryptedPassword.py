import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
import bcrypt

salt = '$2a$12$NQLS2R3QdTRYjVbInDbawe'
key = '7xkVpjUvEHsjEcS0Irrxoa2NkeyKfuq'

print "salt : " + salt
print "key : " + key

hash = bcrypt.hashpw(key, salt)


BLOCK_SIZE = 32
PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
#DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

# create a cipher object using the hash
cipher = AES.new(hash[0:32])

aPassword = raw_input("Input your password to encrypt :")

# encode a string
encoded = EncodeAES(cipher, aPassword)
print 'Encrypted password:', encoded

# decode the encoded string
#decoded = DecodeAES(cipher, encoded)
#print 'Decrypted password:', decoded

