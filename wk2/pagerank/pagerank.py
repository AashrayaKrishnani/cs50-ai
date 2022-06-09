import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    prob = dict()

    allPages = corpus.keys()
    linkedPages = corpus[page]

    # If Page has no links, suppose it to have links to all pages.
    if len(linkedPages)==0:
        linkedPages = allPages

    # Dealing with 'd' probability for Linked Pages.
    factor = damping_factor / len(linkedPages)
    for page in linkedPages:
        prob[page] = factor

    # Dealing with '1-d' probability for all pages
    factor = (1-damping_factor) / len(allPages)
    for page in allPages:
        if page in linkedPages:
            prob[page] += factor
        else:
            prob[page] = factor    

    return prob


    
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = 0
    allPages = list(corpus.keys())

    # Initialising Dictionary.
    prob = dict()
    for page in allPages:
        prob[page] = 0

    # Random first Sample.
    page = allPages[random.randrange(0, len(allPages))]
    prob[page] += 1
    samples += 1

    while samples<n:

        # Prob. Distribution to find which page to choose next.
        model = transition_model(corpus, page, damping_factor)

        # Preparing to choose a page from model based on given prob.
        weights = []
        for i in range(len(allPages)):
            weights.append( model[allPages[i]] )     # The probability for that page.

        # Choosing the page, updating counters.
        page = (random.choices(allPages, weights))[0]
        samples += 1
        prob[page] += 1


    # Now calculating probabilites for each page by dividing occurences/totalSamples
    for page in allPages:
        prob[page] = prob[page]/samples

    return prob
        


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    allPages = corpus.keys()

    # Dictionary of with a page as key, and value being the set of all pages that link TO it.
    linkingPages = dict()
    for p1 in allPages:
        s = set()
        for p2 in allPages:
            if p1 in corpus[p2]:
                s.add(p2)

        linkingPages[p1] = s

    # Initializing dict having each page with probability 1/N
    prob = dict()
    factor = 1/len(allPages)
    for page in allPages:
        prob[page] = factor

    # Recursively Calculating Probabilities
    repeat = True
    while(repeat):
        repeat = False
        
        new_prob = dict()

        for page in allPages:
            
            # Calculating new probablity for this page, based on current data
            val = (1-damping_factor)/len(allPages)

            # Iterating over pages that link TO current page
            for linkingPage in linkingPages[page]:
                linksCount = len(corpus[linkingPage])
                
                val += damping_factor * (prob[linkingPage]/linksCount)

            new_prob[page] = val

            # Maintaining precision of 0.001
            if abs(new_prob[page] - prob[page]) >= 0.001:
                repeat = True

        prob = new_prob

    # Debugging Check
    _sum = 0
    for page in allPages:
        _sum += prob[page] 
    if(abs(_sum - 1) > 0.001):
        # Making their Sum=1
        for page in allPages:
            prob[page] = prob[page]/_sum       # Since check is the Sum.


    return prob

    



if __name__ == "__main__":
    main()
