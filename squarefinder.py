"""SquareFinder 

kippsoftware

Initialized with a word list of a given size, SquareFinder indexes the
words with a Patricia Trie, then returns all the crossword-like grids
of words in the dictionary.

The Wordle dictionary I have only gives you 162, so you'll want to add
some plurals.

"""

import sys, os
import patricia

class SquareNode :
    # keep the state at each coordinate in the solution grid
    def __init__(self) :
        self.letter = ""
        self.allowed = {}

class SquareFinder :
    # index the words
    def __init__(self, words, size) :
        self.words = words
        self.size = size
        self.tree = patricia.Tree().insertWords(words)

    # calculate the legal letters going across at the last grid position
    def across(self) :
        word = ""
        y = (len(self.grid) - 1) // self.size * self.size
        for pos in range(y, len(self.grid)) :
            word = word + self.grid[pos].letter
        allowed = self.tree.getChildren(word)
        return allowed

    # calculate the legal letters going down at the last grid position
    def down(self) :
        word = ""
        x = (len(self.grid) - 1) % self.size
        for pos in range(x, len(self.grid), self.size) :
            word = word + self.grid[pos].letter
        return self.tree.getChildren(word)

    # yield each square solution
    # e.g., for square in self.findSquares()
    def findSquares(self) :
        self.grid = []
        self.grid.append(SquareNode())
        self.grid[-1].allowed = self.across() & self.down()
        self.count = 0
        while len(self.grid) :
            if not len(self.grid[-1].allowed) :
                self.grid.pop()
            else :
                self.grid[-1].letter = sorted(self.grid[-1].allowed)[0]
                self.grid[-1].allowed.remove(self.grid[-1].letter)
                if len(self.grid) == self.size * self.size :
                    if self.solved() :
                        self.count += 1
                        yield str(self)
                else :
                    self.grid.append(SquareNode())
                    self.grid[-1].allowed = self.across() & self.down()

    # cull duplicates
    def solved(self) :
        words = set()
        word = ""
        # collect the words going across
        for y in range(self.size) :
            for x in range(self.size) :
                word = word + self.grid[y * self.size + x].letter
            words.add(word)
            word = ""
        # collect the words going down
        for x in range(self.size) :
            for y in range(self.size) :
                word = word + self.grid[y * self.size + x].letter
            words.add(word)
            word = ""
        # check for duplicates
        return len(words) == self.size + self.size

    # return AtomicML string
    def __str__(self, indent="") :
        out = [ indent + "square %d" % self.count ]
        row = indent + "  "
        count = 0
        for square in self.grid :
            row = row + square.letter
            if (count + 1) % self.size == 0 :
              out.append(row)
              row = indent + "  "
            count += 1
        out.append(row)
        return "\n".join(out)

if __name__ == "__main__" :
    from wordloader import WordLoader
    size = 5
    filename = "five-letter.txt"
    # filename = "wordle-words.txt"
    words = WordLoader(size).loadWords(filename)
    sf = SquareFinder(words, size)
    for square in sf.findSquares() :
        print(square)
