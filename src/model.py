# src/model.py
"""
Hybrid matching:
  1. Exact / alias lookup (fast path)
  2. Levenshtein fuzzy match on tokens (typo tolerance)
  3. GloVe average-vector cosine similarity (synonyms + paraphrases)
  4. Threshold-based decision
"""
import numpy as np
import gensim.downloader as api
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher

from answer_key import ANSWER_KEY
from preprocess import tokenize, normalize

# ---- Load GloVe (cached after first run) ----
print("[model] Loading GloVe (glove-wiki-gigaword-100)...")
GLOVE = api.load("glove-wiki-gigaword-100")
VECTOR_SIZE = GLOVE.vector_size
print(f"[model] GloVe loaded. Vector size = {VECTOR_SIZE}")

# ---- Thresholds (calibrated after testing) ----
HIGH_THRESHOLD = 0.68    # confident correct
LOW_THRESHOLD  = 0.70    # partial / suggest
FUZZY_THRESHOLD = 0.80   # Levenshtein ratio for typo match
# below LOW_THRESHOLD = unrecognized


# ---------- Build alias index for exact/fuzzy matching ----------
ALIAS_INDEX = []  # list of (alias_string, item_id, canonical)
for item in ANSWER_KEY:
    ALIAS_INDEX.append((item["canonical"], item["id"], item["canonical"]))
    for alias in item["aliases"]:
        ALIAS_INDEX.append((alias, item["id"], item["canonical"]))


def _levenshtein_ratio(a: str, b: str) -> float:
    """Similarity ratio 0..1 using SequenceMatcher."""
    return SequenceMatcher(None, a, b).ratio()


def _exact_or_alias_match(query: str):
    """Check if the query equals (or is very close to) any alias/canonical."""
    q = normalize(query)
    if not q:
        return None

    best = None
    best_score = 0.0
    for alias, item_id, canonical in ALIAS_INDEX:
        alias_norm = normalize(alias)
        if q == alias_norm:
            return (item_id, canonical, 1.0)
        ratio = _levenshtein_ratio(q, alias_norm)
        if ratio > best_score:
            best_score = ratio
            best = (item_id, canonical, ratio)

    if best and best_score >= FUZZY_THRESHOLD:
        return best
    return None


# ---------- GloVe vector computation ----------
def _avg_vector(tokens: list) -> np.ndarray:
    vectors = [GLOVE[w] for w in tokens if w in GLOVE]
    if not vectors:
        return np.zeros(VECTOR_SIZE, dtype=np.float32)
    return np.mean(vectors, axis=0).astype(np.float32)


def _item_vector(item: dict) -> np.ndarray:
    text = item["canonical"] + " " + " ".join(item["aliases"])
    return _avg_vector(tokenize(text, remove_stopwords=True))


ITEM_VECTORS = np.stack([_item_vector(it) for it in ANSWER_KEY])
print(f"[model] Precomputed {ITEM_VECTORS.shape[0]} item vectors.")


def similarity_matrix(query: str) -> np.ndarray:
    """(11,1) column vector — the "Matrix" of similarity scores."""
    q_tokens = tokenize(query, remove_stopwords=True)
    q_vec = _avg_vector(q_tokens).reshape(1, -1)
    if not np.any(q_vec):
        return np.zeros((len(ANSWER_KEY), 1), dtype=np.float32)
    return cosine_similarity(q_vec, ITEM_VECTORS).T


# ---------- Main classify function ----------
def classify(query: str) -> dict:
    if not query or not query.strip():
        return {
            "status": "empty",
            "matched_id": None, "matched": None, "score": 0.0,
            "reply": "Please type a question about PC hardware parts.",
            "matrix": [0.0] * len(ANSWER_KEY),
        }

    # --- Stage 1: exact / alias / fuzzy (typo) match ---
    hit = _exact_or_alias_match(query)
    if hit:
        item_id, canonical, score = hit
        matched_item = next(it for it in ANSWER_KEY if it["id"] == item_id)
        return {
            "status": "correct",
            "matched_id": item_id,
            "matched": canonical,
            "score": round(score, 4),
            "reply": (
                f"✅ **{canonical}** (confidence: {score:.2f})\n\n"
                f"{matched_item.get('description', '')}"
            ),
            "matrix": [round(score if it["id"] == item_id else 0.0, 4) for it in ANSWER_KEY],
        }

    # --- Stage 2: GloVe cosine similarity ---
    scores = similarity_matrix(query).flatten()
    best_idx = int(np.argmax(scores))
    best_score = float(scores[best_idx])
    item = ANSWER_KEY[best_idx]

    if best_score >= HIGH_THRESHOLD:
        status = "correct"
        reply = (
            f"✅ **{item['canonical']}** (confidence: {best_score:.2f})\n\n"
            f"{item.get('description', '')}"
        )
    elif best_score >= LOW_THRESHOLD:
        status = "partial"
        reply = (
            f"🤔 Did you mean **{item['canonical']}**? (confidence: {best_score:.2f})\n\n"
            f"{item.get('description', '')}"
        )
    else:
        status = "unrecognized"
        reply = "❌ Sorry, that doesn't match any of the 11 hardware items in the answer key."

    return {
        "status": status,
        "matched_id": item["id"] if status != "unrecognized" else None,
        "matched": item["canonical"] if status != "unrecognized" else None,
        "score": best_score,
        "reply": reply,
        "matrix": [round(float(s), 4) for s in scores],
    }