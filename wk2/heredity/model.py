probs = {
    1: {
        'T': 0.5,
        'F': 0.5
    },
    2: {
        'T': 1,
        'F': 0
    },
    0: {
        'T': 0,
        'F': 1
    },
}

mut = {
    'T': 0.01,
    'F': 0.99
}


def get_gene_prob(geneReq, mother_gene_count, father_gene_count):
    if(geneReq == 0):
        return (probs[mother_gene_count]['T']*mut['T']*probs[father_gene_count]['T']*mut['T']
                + (probs[mother_gene_count]['F']*mut['F']*probs[father_gene_count]['T']*mut['T'])
                + (probs[mother_gene_count]['T']*mut['T']*probs[father_gene_count]['F']*mut['F'])
                + (probs[mother_gene_count]['F']*mut['F']*probs[father_gene_count]['F']*mut['F']))

    elif geneReq == 1:
        return (  # Probability to get that single gene from mother
            (probs[mother_gene_count]['T']*mut['F']*probs[father_gene_count]['T']*mut['T']
             + (probs[mother_gene_count]['F']*mut['T']*probs[father_gene_count]['T']*mut['T'])
             + (probs[mother_gene_count]['T']*mut['F']*probs[father_gene_count]['F']*mut['F'])
             + (probs[mother_gene_count]['F']*mut['T']*probs[father_gene_count]['F']*mut['F']))
            +
            # Probability to get that single gene from father
            (probs[mother_gene_count]['T']*mut['T']*probs[father_gene_count]['T']*mut['F']
             + (probs[mother_gene_count]['T']*mut['T']*probs[father_gene_count]['F']*mut['T'])
             + (probs[mother_gene_count]['F']*mut['F']*probs[father_gene_count]['T']*mut['F'])
             + (probs[mother_gene_count]['F']*mut['F']*probs[father_gene_count]['F']*mut['T'])))
    else:  # GeneReq==2 
        return (probs[mother_gene_count]['T']*mut['F']*probs[father_gene_count]['T']*mut['F']
                + (probs[mother_gene_count]['F']*mut['T']*probs[father_gene_count]['T']*mut['F'])
                + (probs[mother_gene_count]['T']*mut['F']*probs[father_gene_count]['F']*mut['T'])
                + (probs[mother_gene_count]['F']*mut['T']*probs[father_gene_count]['F']*mut['T']))
