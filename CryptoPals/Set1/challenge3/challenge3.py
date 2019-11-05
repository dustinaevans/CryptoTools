from math import log10

class NgramScore(object):
    def __init__(self,ngramfile,sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        for line in open(ngramfile):
            key,count = line.split(sep)
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams:
              score += ngrams(text[i:i+self.L])
            else:
              score += self.floor
        return score


def xorDecrypt(sourcehex,key):
    dest = bytearray.fromhex('') # just makes an empty bytearray
    source = bytearray.fromhex(sourcehex)
    for b in source:
        dest.append(b^key)
    return dest

#source = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
# this is the 0x37 from the source string XOR'd with a guessed plaintext character to give us the key
# key = 0x37^0x6f
#
# # init NgramScore object
# ng = NgramScore('./english_quadgrams.txt')
# # print the ciphertext score
# print(ng.score(source)) # -755.6729089466493
# # print the plaintext score
# print(ng.score(xorDecrypt(source,key).decode())) # -360.3978488822479
# # print the plaintext
# print(xorDecrypt(source,key))
# # print the key
# print(chr(key))

source = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
results = []
ng = NgramScore('./english_quadgrams.txt')
for key in range(256):
    tempdecrypt = None
    score = 0
    try:
        tempdecrypt = xorDecrypt(source,key).decode()
        score = ng.score(tempdecrypt.upper())
    except:
        tempdecrypt = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        score = -900
    results.append({"pt":tempdecrypt,"score":score})
retval = {'pt':'adsf','score':-900}
for i in results:
    if i['score'] > retval['score']:
        retval = i
for i in results:
    print(i)

print(retval)
