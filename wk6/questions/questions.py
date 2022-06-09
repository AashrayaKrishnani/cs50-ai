import math
import os
import string
import nltk
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    files = dict()

    for dir in os.listdir(directory):
        
        with open(os.path.join(directory, dir)) as f:
            data = f.readlines()

        text = ''
        for string in data:
            text += str(string)

        files[dir] = text

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document)

    # words lowercased
    words = [word.lower() for word in words]

    # Words to remove.
    toRemove=set()

    # Filtering.
    for word in words:
        if word in nltk.corpus.stopwords.words('english') or word in string.punctuation:
            toRemove.add(word)

    for word in toRemove:
        try:
            while True:
                words.remove(word)
        except ValueError:
            pass
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    total_docs = len(documents.keys())
    all_words = set()
    for doc in documents.keys():
        words = set(documents[doc])
        all_words = all_words.union(words)

    # Initializing dict with initial count = 0
    words = dict()
    for word in all_words:
        words[word] = 0

    # Updating count of each word
    for doc in documents.keys():
        crnt_words = set(documents[doc])
        for word in crnt_words:
            words[word] += 1

    # Finally Calculating idf values.
    for word in all_words:
        words[word] = math.log2(total_docs/words[word])

    return words


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    # Dict to store Score
    scores = dict()
    for file in files.keys():
        scores[file]=0

    for q in query:
        # If word is in some document.
        if q in idfs.keys():
            # Iterating throught files
            for file in files.keys():
                # If File has this word.
                if q in files[file]:
                    # Calculate frequency.
                    f = files[file].count(q)
                    # Update Score.
                    scores[file] += f*idfs[q]
                else: 
                    pass

        else: 
            pass

    answer = list(scores.keys())
    answer.sort(key=lambda f: scores[f], reverse=True)

    return answer[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    # Dict to store Score
    scores = dict()
    for sentence in sentences.keys():
        scores[sentence]=0

    # Calculating Score based on idfs
    for q in query:
        # If word is in some sentence.
        if q in idfs.keys():
            # Iterating throught sentences
            for sentence in sentences.keys():
                # If Sentence has this word.
                if q in sentences[sentence]:
                    # Update Score.
                    scores[sentence] += idfs[q]
                else: 
                    pass
        else: 
            pass

    answer = list(scores.keys())
    answer.sort(key=lambda f: scores[f], reverse=True)

   # Function to calculate query term density.
    def query_term_density(query, sentence):
        common = 0
        for word in tokenize(sentence):
            if word in query:
                common+=1

        return common/len(sentence)

    # Manually sorting equal score values based on query-term density
    for k in range(n):
        modified = False
        for i in range(len(answer)-1):
            # If Equal Scores.
            if scores[answer[i]] == scores[answer[i+1]]:
                # If in Incorrect Order -> Swap.
                if query_term_density(query, answer[i]) < query_term_density(query, answer[i+1]):
                    tmp = answer[i+1]
                    answer[i+1] = answer[i]
                    answer[i] = tmp
                    modified=True
        if not modified:
            break

    return answer[:n]


if __name__ == "__main__":
    main()
