import json
import blessings
import time

"""
(Mandatory) dictionaryFile: String
(Mandatory) trainingText: String
(Optional)  debug: Bool
trainer = DictionaryTrainer(dictionaryFile,trainingText,debug)
trainer.train()

TODO: Create a function that saves the dictionary as JSON
"""
class DictionaryTrainer:

    def __init__(self,dictionary,trainingText,debug: bool=False):
        self.__matches = 0
        self.__trainingTextName = trainingText
        self.__dictionaryName = dictionary
        self.__debug = debug
        self.__loadDictionary(dictionary)
        self.__loadTrainingText(trainingText)

    """
    Private

    log(msg) -> void

    print msg to stdout
    """
    def __log(self,msg):
        if self.__debug:
            print(msg)

    """
    Private

    loadDictionary(dictionary) -> void

    loads the dictionary into self.dictionary
    if json, loads as dict
    if not json, loads as text file
    """
    def __loadDictionary(self,dictionary):
        fd = open(dictionary,'r')
        jsontest = fd.readline()
        fd.seek(0)
        if "{" in jsontest:
            self.__dictionary = json.loads(fd.read())
        else:
            self.__dictionary = fd

    """
    Private

    loadTrainingText(text) -> void

    creates file descriptor for training text in self.trainingText
    """
    def __loadTrainingText(self,text):
        self.__trainingText = open(text,'r')

    """
    Private

    stripNonLetters(word) -> string

    Creates a copy of the word that only contains alphabet letters
    """
    def __stripNonLetters(self,word):
        validchars = "abcdefghijklmnopqrstuvwxyz'ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        tempword = ""
        for i in word:
            i = i.lower()
            if i in validchars:
                tempword+=i
        tempword = tempword.strip()
        tempword = tempword.lower()
        tempword = tempword.replace(" ","")
        tempword = tempword.replace("\t","")
        return tempword

    """
    Private

    findDictWordInText(word) -> void

    Tests whether the word is in self.trainingText
    If word exists, log("Match")

    TODO: Update the dictionary with the count for each word found

    NOTE: Doesn't match anything??
    """
    def __findDictWordInText(self,word):
        self.__trainingText.seek(0)
        word = word.lower()
        self.__menu("Training dictionary word: %s"%word)
        for line in self.__trainingText:
            """Testing for empty line. If strip returns a string, continue"""
            line = line.strip()
            if line:
                self.__log("Testing against: %s"%line)
                if " " in line:
                    self.__log("Splitting line")
                    line = line.split(" ")
                    templine = []
                    for i in line:
                        templine.append(self.__stripNonLetters(i))
                    line = templine
                else:
                    line = self.__stripNonLetters(line)
                if type(line) is list:
                    self.__log("Line is list")
                    for i in line:
                        self.__log("Testing %s against %s"%(word,i))
                        if i == word:
                            self.__matches += 1
                            #self.__menu("Match: %s - %s"%(word,i)) # Point to update dictionary counts
                        else:
                            pass
                            #self.__menu("List %s != %s"%(i,word))
                else:
                    if line == word:
                        self.__matches += 1
                        #self.__menu("Match: %s - %s"%(word,line)) # Point to update dictionary counts
                    else:
                        pass
                        #self.__menu("NonList %s != %s"%(line,word))
                self.__log("Line is now: %s"%line)
                self.__log("\n\n")
        time.sleep(.2)


    def __menu(self,output: str=None):
            if not self.__debug:
                term = blessings.Terminal()
                with term.fullscreen():
                    term.move(0, 0)
                    print("Dictionary Training tool")
                    print("Written by: Dustin Evans")
                    print("Training your Dictionary %s against file %s"%(self.__dictionaryName,self.__trainingTextName))
                    if output:
                        print(output)
                    else:
                        pass
                    print("\n Matches: %s"%self.__matches)
    """
    Public

    train() -> void

    Begins the training process
    """
    def train(self):
        line = self.__dictionary.readline()
        while line:
            self.__findDictWordInText(line)
            line = self.__dictionary.readline()


trainer = DictionaryTrainer('/usr/share/dict/words','./the_lightning_thief.txt',False)
trainer.train()
