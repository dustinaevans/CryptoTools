import json


test1 = "apple"
pattern1 = "12234"

class DictLookup:

    def __init__(self,dictionary):
        self.initDict(dictionary)
        pass

    def update(self, ct):
        self.ct = ct

    def findPattern(self,pattern):
        pass

    def initDict(self,dictionary):
        fd = open(dictionary,'r')
        self.dictionary = json.loads(fd.read())

    def initEmptyPattern(self,maskstr):
        testpattern = []
        for i in maskstr:
            testpattern.append("A")
        return testpattern

    def getUniqChars(self,teststr):
        uniq = []
        count = 0
        for i in teststr:
            if i in uniq:
                pass
            else:
                uniq.append(i)
        return uniq

    def word2Pattern(self,word):
        empty = self.initEmptyPattern(word)
        emptystr = ""
        uniq = self.getUniqChars(word)
        count = 0
        for i in word:
            if i in uniq:
                empty[count]=str(uniq.index(i)+1)
            count+=1
        for i in empty:
            emptystr+=i
        return emptystr

    def testWordAndPattern(self,word,pattern):
        test1 = word
        test2 = pattern
        if test1 == test2:
            return True
        return False

    # Abstract testing of two different words
    def test2Words(self,word1,word2):
        if len(word1) != len(word2):
            return False
        test1 = self.word2Pattern(word1)
        test2 = self.word2Pattern(word2)
        if test1 == test2:
            return True
        return False

    def findCTWord(self, word):
        ctword = word.lower()
        for i in self.dictionary:
            i = i.lower()
            if self.test2Words(i,word):
                print("Possible word for %s is %s"%(word,i))

CT = "LOFYSDJ LZDPX' MDPPOVZOAI LSXR OA YSJJGNDDA OX SFMESJJZ FSWMSOA ROPR ROAU GV MYD LSXR OX LGUDJDU SVMDP' NOJJOSL XYSMADP'X VSFD HEM WSOAMDU NYOMD"

dl = DictLookup('./words_dictionary.json')

dl.findCTWord("SFMESJJZ")


# Notes
# Need to add some kind of weight to the words in the dictionary
# Possiblility of spidering reddit and updating weights based on the thread entries
# Count total number of words tested and divide individual word hits by total to get weights
