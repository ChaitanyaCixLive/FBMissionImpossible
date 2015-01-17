import base64
import ConfigParser
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
import bcrypt

class LutherStickell(object):

	_instance = None
    	def __new__(cls, *args, **kwargs):
        	if not cls._instance:
            		cls._instance = super(LutherStickell, cls).__new__(cls, *args, **kwargs)
        	return cls._instance


	def __init__(self):

		self.myConfig = ConfigParser.ConfigParser()
		self.myConfig.read("./LutherStickell.ini")

	def GetMeDBName(self):

		return self.myConfig.get("MovieConfig", "Database")

	def GetMeDBUserName(self):

		return self.myConfig.get("MovieConfig", "DBUser")

	def GetMeDBUserPassword(self):

		return self.myConfig.get("MovieConfig", "DBPass")

	def GetMeFacebookAppURL(self):

		return self.myConfig.get("FB", "AppURL")

	def GetMeFacebookUserId(self):

		return self.myConfig.get("FB", "User")

	def SsssssshGetFacebookPassword(self):

		salt = self.myConfig.get("FB", "Salt")
		key = self.myConfig.get("FB", "Key")
		hashed = bcrypt.hashpw(key, salt)
		
		cipher = AES.new(hashed[0:32])
		
		BLOCK_SIZE = 32
		PADDING = '{'

		pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

		DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
		
		return DecodeAES(cipher, self.myConfig.get("FB", "Pass"))
		


