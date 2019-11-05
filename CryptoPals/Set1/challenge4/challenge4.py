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
        #text = text.upper()
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams:
              score += ngrams(text[i:i+self.L])
            else:
              score += self.floor
        #print(text,score)
        return score

    def xorDecrypt(self,sourcehex,key):
        dest = bytearray.fromhex('') # just makes an empty bytearray
        source = bytearray.fromhex(sourcehex)
        for b in source:
            dest.append(b^key)
        try:
            dest = dest.decode()
        except:
            dest = None
        return dest

ng = NgramScore('../challenge3/english_quadgrams.txt')
fd = open('./4.txt','r')
results = []
for line in fd:
    line = line.strip()
    for key in range(255):
        result = ng.xorDecrypt(line,key)
        if result:
            result = result.strip()
            score = ng.score(result.upper())
            results.append({"pt":result,"score":score})
retval = {"pt":"z","score":-900}
for j in results:
    if j["score"] > retval["score"]:
        retval = j
for count in range(10):
    print(results[count])
print("Suggested Answer: ",retval)
