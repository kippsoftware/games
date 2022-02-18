"""Patricia Trie for indexing words

kippsoftware

Each node has its own letter and a map<letter,node> of its children's
letters.

"""

class Node :
    # instantiate an empty node
    # letter - one letter
    def __init__(self, letter) :
        self.letter = letter
        self.children = { }
    # insert a word into the tree
    # word - string of letters
    def insert(self, word) :
        if not len(word) :
            return
        letter = word[0]
        if not letter in self.children :
            self.children[letter] = Node(letter)
        self.children[letter].insert(word[1:])
    # return True if the word is in the tree
    # word - string of letters
    def hasWord(self, word) :
        if not len(word) :
            return True
        letter = word[0]
        if letter in self.children :
            return self.children[letter].hasWord(word[1:])
        return False
    # return set of child letters
    # word - string of letters
    def getChildren(self, word) :
        if not len(word) :
            return self.children.keys()
        letter = word[0]
        if letter in self.children :
            return self.children[letter].getChildren(word[1:])
        return {}
    # return AtomicML string
    def __str__(self, indent = "") :
        out = [ indent + self.letter ]
        for item in sorted(self.children) :
            out.append(self.children[item].__str__(indent + "  "))
        return "\n".join(out)

class Tree :
    # initialize with empty root
    def __init__(self) :
        self.root = Node("*")
    # insert words into the tree
    # words - list of words
    def insertWords(self, words) :
        for word in words :
            self.insertWord(word)
        return self
    # insert one word into the tree
    # word - string of letters
    def insertWord(self, word) :
        self.root.insert(word)
        return self
    # return True if the word is in the tree
    # word - string of letters
    def hasWord(self, word) :
        return self.root.hasWord(word)
    # return set of child letters
    # word - string of letters
    def getChildren(self, word) :
        return self.root.getChildren(word)
    # return AtomicML string
    def __str__(self, indent="") :
        return self.root.__str__(indent)

if __name__ == '__main__' :
    WORDS = """\
APPLE
APPLY
AROSE
THEIR
THERE
UNTIL"""
    tree = Tree().insertWords(WORDS.split("\n"))
    print(tree)
    print("tree has APPLE", tree.hasWord("APPLE"))
    print("tree has UNTIL", tree.hasWord("UNTIL"))
    print("tree has ACORN", tree.hasWord("ACORN"))
    print("children of A", tree.getChildren("A"))
