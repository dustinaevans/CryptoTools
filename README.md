# CryptoTools
Various cryptography tools that I have created

## Purpose
When I create tools for cryptologic research, I put them in this repo so that others can use and develop them.

## Motivation
I fully intend to further the public understanding of cryptology and nurture the learning of people that are new to the science.
I am by no means advanced in the field, but research must be done in order to gain understanding.

## PatternFinder
1. Transforms a word to a pattern and then finds that pattern in a text file.

```
tries -> 12345

match 12345 -> flies
match 12345 -> bread
match 12345 -> grunt
```

2. Takes in a pattern and matches that pattern in a text file.

```
12345

match 12345 -> files
match 12345 -> tries
match 12345 -> bread
```

Note that these matches do not provide an guarantee that the word found IS the word you are looking for.

## DictionaryTrainer
Trains a dictionary against a text file
See the readme.md in DictionaryTrainer for additional information.
