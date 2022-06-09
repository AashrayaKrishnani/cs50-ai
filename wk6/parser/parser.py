import re
import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP
NP -> N | Adj NP | Det NP | NP PP | N NP
VP -> V | V NP | V PP | Adv VP | VP Adv
PP -> P | P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence)

    # Removing if no alphabetical character is there.
    for word in words:
        if re.search(r"[a-zA-Z]+", word) is None:
            words.remove(word)
    
    # Return lower case words.
    return [ str(word).lower() for word in words]

        


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    trees_to_traverse = list(tree.subtrees(lambda t: t.label()=='NP'))

    chunk = []

    while len(trees_to_traverse) > 0:
        crnt_tree = trees_to_traverse.pop()
        
        sub_trees = list(crnt_tree.subtrees(lambda t: t.label()=='NP' and t!=crnt_tree))

        # If no NP subtrees
        if (sub_trees is None or len(sub_trees)==0):
            if crnt_tree not in chunk:
                chunk.append(crnt_tree)
        # If There are more NP sub trees
        else:
            trees_to_traverse.extend(sub_trees)

    return chunk


if __name__ == "__main__":
    main()
