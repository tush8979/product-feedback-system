from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query, texts, top_k=5):
    if not texts:
        return []

    q_emb = model.encode(query, convert_to_tensor=True)
    t_emb = model.encode(texts, convert_to_tensor=True)

    scores = util.cos_sim(q_emb, t_emb)[0]
    top = scores.topk(k=min(top_k, len(texts)))

    return top.indices.tolist()