from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes as randBytes
from Crypto.Util.Padding import pad,unpad

key = randBytes(16)

def parseKV(KV):
    obj = {}
    kvlist = KV.split("&")
    for i in kvlist:
        kvmagic = i.split("=")
        obj[kvmagic[0]]=kvmagic[1]
    return obj

def profile_for(email):
    badchars = "&="
    for i in badchars:
        if i in email:
            return 0
    hashobj = MD5.new()
    hashobj.update(email.encode())
    uid = hashobj.hexdigest()
    role = 'user'
    return "email=%s&uid=%s&role=%s"%(email,uid,role)

def sendProfile(email):
    cipher = AES.new(key,AES.MODE_ECB)
    profile = profile_for(email)
    profile = profile.encode()
    if profile == 0:
        return 0
    profile = pad(profile,AES.block_size)
    return cipher.encrypt(profile).hex()

def recvProfile(profile):
    profile = bytearray.fromhex(profile)
    cipher = AES.new(key,AES.MODE_ECB)
    profile = cipher.decrypt(profile)
    profile = unpad(profile,AES.block_size).decode()
    profile = parseKV(profile)
    print(profile)

for i in range(13):
    profile = sendProfile("A"*i)
    print(profile)
    print([profile[i:i+32] for i in range(0, len(profile), 32)],i)
    recvProfile(profile)
# print(sendProfile("dustine@turnkeysol.com"))
