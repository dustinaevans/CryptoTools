# CryptoPals
Solutions to the challenges located at https://cryptopals.com/

## Challenge
So this challenge is all about actually detecting that single-char XOR has been used to encrypt a string.

## Problem
There are 327 strings in the file that included with the challenge. Our goal is not so much decrypting the string rather than detecting that it was encrypted specifically with single-byte XOR. However, I think that decrypting and detecting the encryption would be one and the same, in this case. So, we are just going to bruteforce all of the strings in the file, record the decrypted text and score and print out the highest scoring result. This challenge will be going straight to the solution portion.

## Solution
1. Load the file
3. Init an empty list to store results in
2. Iterate over all of the strings
3. Iterate over 256 values and decrypt with each
4. Score the resulting plaintext
5. Store the plaintext and its score in results
6. Iterate over results to find the highest scoring value
7. Print highest scoring value

```python
# Including the same code that was used in challenge3:

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
```

This prints the text "{'pt': 'Now that the party is jumping', 'score': -248.86250710373162}"

This one was really trivial, let's move on to the next challenge.
