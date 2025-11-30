import re
from collections import Counter

_SENTENCE_ENDS = re.compile(r'[.!?]+')

def tokenize_sentences(text):
    sentences = [s.strip() for s in _SENTENCE_ENDS.split(text) if s.strip()]
    return sentences

def tokenize_words(text):
    words = re.findall(r"\b[\w']+\b", text.lower())
    return words

def basic_metrics(text):
    words = tokenize_words(text)
    sentences = tokenize_sentences(text)
    chars = len(text)
    unique_words = len(set(words))
    word_count = len(words)
    sentence_count = max(1, len(sentences))
    avg_sentence_len = word_count / sentence_count if sentence_count else word_count
    lexical_density = unique_words / word_count if word_count else 0
    # simple complexity proxy
    complexity = avg_sentence_len * (1 + (1 - lexical_density))
    return {
        "chars": chars,
        "words": word_count,
        "unique_words": unique_words,
        "sentences": sentence_count,
        "avg_sentence_length": round(avg_sentence_len, 2),
        "lexical_density": round(lexical_density, 3),
        "complexity_score": round(complexity, 3)
    }

def highlight_issues(text):
    """Return very simple grammar-ish hints (heuristic)."""
    sentences = tokenize_sentences(text)
    hints = []
    for i, s in enumerate(sentences[:8], 1):
        if len(s.split()) > 35:
            hints.append(f"Sentence {i}: very long ({len(s.split())} words) — consider splitting.")
        if re.search(r'\bi\b', s):
            # heuristic: lowercase "i" may indicate nonstandard writing
            hints.append(f"Sentence {i}: lowercase 'i' found — check capitalization.")
    return hints
