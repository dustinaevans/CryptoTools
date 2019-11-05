# CryptoPals
Solutions to the challenges located at https://cryptopals.com/

## Challenge
Single byte XOR. This is generally trivial, you simply loop over the values 0-255 (0x00 - 0xFF) and XOR the first byte of the provided string until you get a readable char. However, I have completed the first 5 challenges before and how you solve this challenge will determine your success in solving challenge 6.

## Problem
The problem that I am going to focus on is the scoring mechanism. The last time I solved this challenge, I thought my scoring mechanism was sufficient but later it turned out that this was false. The way that I scored the result strings the first time was based on the valid chars and their frequency of use in the English language. In the interest of learning from my mistakes, let's review my old scoring algorithm.

```
These apply to both uppercase and lowercase
Scoring:
E : 20
T : 19
A : 18
O : 17
I : 16
_ : 15 (This is a space not an underscore)
S : 14
H : 13
R : 12
D : 11
L : 10
U : 9

All other letters score a 1 (includes punctuation)
Non-printable chars score a -10
```
- start score at zero
- iterate over the string
- for each letter found, add the table value of that char to the score

This really is a simple and effective solution for THIS challenge but it wasn't sufficient in challenge 6 because a string with a large number of high-scoring chars would score higher than the actual plaintext. Eg. EEEEE (100) would score higher than apple (50).

Let's begin revamping this scoring algorithm.

Start with what we know. This is repeating key XOR. More importantly, it is single-byte repeating key XOR. This means that all of the characters in the string are encrypted using the same key. So, let's examine the text to see if we can find any information about the original plaintext.

```
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
```
Now, I'm going to split the string into bytes because this is clearly all hex.

```
1b 37 37 33 31 36 3f 78 15 1b 7f 2b 78 34 31 33 3d 78 39 78 28 37 2d 36 3c 78 37 3e 78 3a 39 3b 37 36
```

The first thing that catches my eye is that 37 repeats several times. The real catch is that it repeats twice in a row and this indicates a double.

```
A quick note about letter groupings in cryptography:
- A monogram is simply a single letter
- A bigram is a group of 2 letters that is valid in the relevant language
  - Example: ie is a valid digram but jk is not because it is never found in any word
- A double is a bigram that has the same letter in both positions and is valid
  - Example: ss, nn, ee, etc.
- A trigram is a group of 3 letters that is valid
  - Example: ing, est
- A Quadgram is a group of 4 letters
  - Example: tion, ions
- A Quintgram is a group of 5 letters
  - Example: ation, tions, tiona
```

The double is important because they are not all that common (compared to other groupings) and there are a limited number of them in English. The most common doubles are, in this order, ss, ee, tt, ff, ll, mm, oo. Therefore, our double of 37 37 is likely to be one of these. So let's try those out by hand. The ASCII value for s is 115 or 0x73. The special thing about XOR is that it doesn't matter what order the values are in (A^B == B^A). So, if we XOR 0x37 with 0x73 we should get the key because of the following:

```
A^B=C
B^A=C
A^C=B
B^C=A
```

`0x73 ^ 0x37 = 0x44`

0x44 is ASCII D. This looks promising because we got a valid character as the alleged key. So let's XOR another byte with 0x44 and see if we get another valid character.

`0x44 ^ 0x1B = 0x5F`

0x5F is ASCII _ so this may not be so promising after all, but let's try one more.

`0x44 ^ 0x78 = 0x3C`

0x3C is ASCII < so D really isn't a good candidate for the key because it is unlikely that a sentence has several < in it.

Now we continue this process of trying all of the doubles until we get reasonable characters out. This will be the first part of the python script, I will just create a function to XOR the entire string with a chosen value and print the result to see if we get good results. Note that I will probably have to try out uppercase and lowercase letters to find the key.

This approach wasn't as fast as just bruteforcing the entire keyspace but it is much more efficient because I only needed 4 guesses to get the key. This approach is known as a plaintext attack. A plaintext attack depends on you either guessing or knowing part of the plaintext that made the ciphertext you are working on. In this case, we were able to guess that the ciphertext of hex 3737 was the plaintext oo. When we XOR 0x37 with the ASCII hex value for o which is 0x6F, we get 0x58 which is ASCII X (note the caps). Therefore, the key for this is XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX or X * 34. This is a very simple problem but we are only half done. Now we need to analyze the plaintext and find a way to get that result via some scoring method and pretending that we don't know the key.

I saw some articles on at http://practicalcryptography.com/cryptanalysis/, so let's take a look at that. Under text characterization, we see several methods by which we can score a piece of suspected plaintext. It appears that there is already an ngram scoring tool on this website at http://practicalcryptography.com/media/cryptanalysis/files/ngram_score_1.py. We will analyze and use this code. Also included in this repo is the english quadgrams file which you can find at http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/.

```python
'''
EDIT by Dustin Evans: This code has been updated to run on python3

Allows scoring of text using n-gram probabilities
17/07/12
'''
from math import log10

class ngram_score(object):
    def __init__(self,ngramfile,sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        for line in file(ngramfile):
            key,count = line.split(sep)
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.itervalues())
        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in xrange(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams:
              score += ngrams(text[i:i+self.L])
            else:
              score += self.floor          
        return score

```

```text
Example usage from the site:
import ngram_score as ns
fitness = ns.ngram_score('quadgrams.txt')
print fitness.score('HELLOWORLD')
```

If we first look at the quadgrams file (I will explain why we are using quadgrams in a bit), we see that the format is `YOUR 1194475`, which is the quadgram and it's count. To get the quadgrams probability, we first sum all of the counts and divide the count in question by that total, then take the log base 10 of the result. Ultimately, this will give us a negative number and the closer that number is to 0, the more "English-like" the quadgram is, or the more popular the quadgram in the English language.

```text
Side Note:
I think after completing this challenge, I will update my dictionary trainer to use this algorithm so that we can further expand the dictionaries.
```

After we have computed the probabilities and have them loaded in memory, we can score a piece of text. To score, we do the following:
1. Set score equal to zero
2. Set ngrams to the `__getitem__` function
3. Loop over the range 0-5 (in this case `self.L=4` because we are using quadgrams)
4. For each substring `i:i+5`, if the substring is in self.ngrams, increment score by the probability of that ngram
5. Else if the substring is NOT in self.ngrams, increment the score by `log10(0.01/sum)` Where sum is the total of all counts in quadgram file
6. Return the score

The reason that we are using quadgrams is because the larger your letter groupings, the more accurate you can be. Monograms ended up working terribly for me because you could repeat the highest scoring letters to make the overall score higher. In the case of quadgrams, it is statistically much less likely that quadgrams will be repeated in a short text. In a large encrypted text, the result may be skewed because there are more letters to count. However, you could just break the text into small pieces and work with one at a time until you find the key, assuming that the key isn't as large as the text itself.

So now, lets try this code out. Scoring the ciphertext gives us a score of `-755.6729089466493` and the plaintext gives us a score of `-360.3978488822479`. So this worked out quite well. Now we need to write the program to the specifications that the website gave us; we need to pretend like we don't have the key and iterate over all possible keys. So let's write that code.

```python
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
```

I actually ended up having to go through several iterations of this code. First, the codes wasn't compatible with python3. Second, there were cases where the decrypted text had values that were out of ordinal range (not in the ASCII table). This is where the z's and the score of -900 come in. If the program can't turn the values into text, just give it z's and -900. Third, uppercase values were getting a better score than lowercase. When you do this project for yourself, you will find that there are two nearly correct answers for the key; one that gives you the correct case and one that gives you the incorrect case. If you are working on an XOR problem and you get something that looks almost readable, change the case of your key and that may give you the correctly decrypt the ciphertext.

```
Case example:

A key of X yields "Cooking MC's like a pound of bacon"
a key of x yields "cOOKING\x00mc\x07S\x00LIKE\x00A\x00POUND\x00OF\x00BACON"

```

So now we have our scoring mechanism and we will be prepared for challenge 6 when it comes along.


## References
https://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html
http://practicalcryptography.com/cryptanalysis/ **This reference is very good**
http://www.asciitable.com/
http://xor.pw/
