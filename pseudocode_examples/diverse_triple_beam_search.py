def diverse_triple_search(q, t_list, b, l, γ):
    """
    Performs diverse triple beam search, used in our proposed NaiveGE or SyncGE.

    Parameters:
        q: query
        b: beam size
        t_list: initial triples  
        l: maximum length
        γ: hyperparameter for diversity
    """
    # Initialize beam for first step
    B_0 = []

    # Score individual triples
    for t in t_list:
        s = score(q, [t])
        B_0.add((s, [t]))
    
    B_0 = top(B_0, b)  # Keep top b scoring triples
    
    # Iterative beam search
    for i in range(1, l):
        B = []
        
        for (s, T) in B_{i-1}:
            V = []  # Candidates from current path
            
            # Explore neighboring triples
            for t in get_neighbours(T[-1]):
                # Skip if triple already used
                if exists(t, B_{i-1}):
                    continue
                
                # Score new path with concatenated triple
                new_path = T + [t]
                s_new = s + score(q, new_path)
                V.add((s_new, new_path))
            
            sort(V, descending=True)
            
            # Apply diversity penalty
            for n in range(len(V)):
                s_new, path = V[n]
                penalty = exp(-min(n, γ)/γ)
                B.add((s_new * penalty, path))
        
        B_i = top(B, b)  # Keep top b paths
    
    return B_i