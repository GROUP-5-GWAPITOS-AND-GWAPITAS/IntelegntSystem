# src/preprocess.py
"""
Text preprocessing: lowercasing, punctuation removal, whitespace
normalization, tokenization, and input validation.
"""
import re
import string

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "of", "in", "on",
    "for", "to", "and", "or", "with", "what", "which", "who", "that",
    "this", "it", "its", "as", "at", "by", "from", "be", "been",
}


def normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    if text is None:
        return ""
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str, remove_stopwords: bool = False) -> list[str]:
    """Normalize + split into tokens; optionally remove stopwords."""
    text = normalize(text)
    if not text:
        return []
    tokens = text.split()
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]
    return tokens


def is_valid_input(text: str) -> bool:
    """Reject empty or whitespace-only input."""
    return bool(normalize(text))