def syncge(query):
    """
    SyncGE pipeline implementation.
    
    Parameters:
        query: Input query  
    """
    
    # Base retrieval for current query (i.e bm25)
    base_passages = base_retriever(current_query)
    
    # Read passages and extract proximal triples via LLM
    proximal_triples = reader(base_passages, query)
    
    # Link proximal triples to their closest real triples in index
    triples = tripleLink(proximal_triples)

    # Graph expansion using proximal triples
    expanded_passages = graph_expasion(triples, query)

    # Combine base and expanded passages, and save them
    combined_passages = rrf(base_passages + expanded_passages)

    return combined_passages