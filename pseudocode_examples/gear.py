class GistMemory:
    """
    Manages the accumulation and storage of proximal triples
    across multiple retrieval steps.
    """
    def __init__(self):
        self.proximal_triples = []
    
    def add_triples(self, new_triples):
        """Append new proximal triples to memory"""
        self.proximal_triples.extend(new_triples)
    
    def get_all_triples(self):
        """Return all accumulated triples"""
        return self.proximal_triples

def gear(query, max_steps=4):
    """
    GeAR pipeline implementation with multi-step retrieval capabilities.
    
    Parameters:
        query: Original input query  
        max_steps: Maximum number of retrieval steps
    """
    # Initialize variables
    gist_memory = GistMemory()
    current_query = query
    step = 1
    retrieved_passages = []
    
    while step <= max_steps:
        # Base retrieval for current query (i.e bm25)
        base_passages = base_retriever(current_query)
        
        # Read passages and extract proximal triples via LLM
        if step == 1:
            proximal_triples = reader(base_passages, query)
        else:
            proximal_triples = reader(base_passages, query, gist_memory.get_all_triples())
        
        # Link proximal triples to their closest real triples in index
        triples = tripleLink(proximal_triples)

        # Graph expansion using proximal triples
        expanded_passages = graph_expasion(triples, query)

        # Combine base and expanded passages, and save them
        combined_passages = rrf(base_passages + expanded_passages)
        retrieved_passages.append(combined_passages)
        
        # Read passages and extract proximal triples via LLM 
        proximal_triples = gist_memory_constructor(expanded_passages)

        # Add to gist memory
        gist_memory.add_triples(proximal_triples)

        # Check if we have enough evidence to answer query
        is_answerable, reasoning = reason(gist_memory.get_all_triples(), query)
        
        if is_answerable:
            break
        else:
            # Rewrite query for next step
            current_query = rewrite(query, gist_memory.get_all_triples(), reasoning)
            step += 1
    
    # Link final gist memory triples to passages
    gist_passages = []
    for triple in gist_memory.get_all_triples():
        linked_passages = passageLink(triple)
        gist_passages.append(linked_passages)
    
    # Final passage ranking combining all retrieved passages
    final_passages = rrf(gist_passages + retrieved_passages)

    return final_passages