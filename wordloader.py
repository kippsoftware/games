"""WordLoader filters a dictionary and returns the words

kippsoftware

The dictionary format is a text file with one word per line.

The easiest way to snag a dictionary is on the command line.  You can
sed, awk, grep, and sort if you want to.

% /usr/local/bin/aspell dump master > words.txt

"""

import os

class WordLoader :
    def __init__(self, size) :
        self.size = size

    # filter out wrong-sized words, words with apostrophes, and proper nouns
    def filter(self, word) :
        return len(word) == self.size and "'" not in word and word == word.lower()

    # parse and return the filtered words from the given dictionary
    # filename - where to read the words
    def loadWords(self, filename) :
        words = [ word.strip() for word in open(filename).readlines() ]
        words = list(sorted(filter(self.filter, words)))
        return words

if __name__ == "__main__" :
    w = WordLoader(5)
    words = w.loadWords("words.txt")
    print(len(words), "%d-letter words found" % w.size)
