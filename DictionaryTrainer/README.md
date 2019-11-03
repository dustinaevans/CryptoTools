# DictionaryTrainer
Trains a dictionary against a text file

## Intent
The intent of this project is to create a dictionary for cryptographic purposes that contains many words a measure of their popularity
in modern language. This dictionary was created for my own purposes, which is to say that I did not generalize the dictionary for any other use.

## My purpose
I am using this dictionary with the PatternFinder that is included in this repo. PatternFinder takes any word and generates a pattern form it.

```
Apple -> 12234
racecar -> 1234321
Racecar -> 1234321

Note1:
The case of the letter makes no difference.
If anyone sees a reason that the case is significant, please let me know in the issues.
```

Then, checks a dictionary for any word that matches that pattern. (This is where the weights come in.)
PatternFinder prints out all possible matches of that word and without any weighting, there is no possible way to know which word actually matches.

Ciphertext Example:
```
LZDPX -> 12345
boats -> 12345
tries -> 12345
flies -> 12345
```

You see, all of the above words (and many, many more) match the ciphertext pattern.
The purpose of this dictionary is to give the most common words that fit the pattern.

## Format
If you choose to create your own dictionary, it should be in a JSON format as follows:

```
{
  "word": {
    "totalTests": 500,
    "matches": 100,
    "weight": .2
  }
}

where <word> is a string, totalTests is an integer, matches is an integer and weight is a precision value (.12345678)
```

## Operation
The dictionary trainer will loop over the dictionary and update the totalTests value with each comparison.
When it finds a match in the text, it will update the matches value, divide matches with totalTests and update the weight.
The weight is a measure of the absolute popularity of the word as it relates to all text.

## Usage
To use the dictionary, a pattern matcher would be useful. (See ../PatternFinder)
However, if you choose to make use of the dictionary in your own way, find your matches and sort by weight.
This will give you a great starting point for finding the word that you are looking for.

## Contribution
Contributions are welcome. You can either contribute to the code or you can train the dictionary of any modern text that you find.
In either case, please fork the repo and create a new branch. Please include the text that you trained on in your branch.
When your contributions are added, create a pull request.
I will merge the request and if the changes are acceptable, I will then merge the branch into master.

## Notes
11/3/2019 3:00 PM CST
This is currently partially broken. For some reason, the trainer will not match any dictionary words to text words. I really don't understand the reason for this yet but I'm sure it is something simple.
