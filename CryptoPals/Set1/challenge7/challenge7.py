from Crypto.Cipher import AES
from base64 import b64decode

key = b"YELLOW SUBMARINE"

fd = open('7.txt','rb')
ct = fd.read()
ct = b64decode(ct)
cipher = AES.new(key, AES.MODE_ECB)
pt = cipher.decrypt(ct).decode()
print(pt)
