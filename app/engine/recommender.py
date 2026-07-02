import math
import re
from typing import Any, Dict, List

from app.catalog.loader import load_catalog

catalog = load_catalog()

WEIGHT_NAME = 5
WEIGHT_KEYS = 3
WEIGHT_DESCRIPTION = 1

PHRASE_BONUS_NAME = 6
PHRASE_BONUS_DESCRIPTION = 2

MIN_SCORE = 1.5

STOPWORDS = {
    "a", "an", "the", "and", "or", "for", "of", "to", "in", "on", "with",
    "is", "are", "we", "need", "needs", "looking", "hire", "hiring",
    "assessment", "assessments", "test", "tests", "role", "candidate",
    "candidates", "please", "want", "would", "like", "can", "you",
    "recommend", "suggest", "who", "that", "will",
}

SYNONYMS = {
    "back-end": "backend",
    "back end": "backend",
    "front-end": "frontend",
    "front end": "frontend",
    "engineer": "developer",
    "engineers": "developer",
    "dev": "developer",
    "devs": "developer",
    "py": "python",
    "js": "javascript",
    "db": "database",
    "databases": "database",
    "amazon web services": "aws",
    "behavioural": "personality",
    "behavioral": "personality",
    "behaviour": "personality",
    "behavior": "personality",
    "reasoning": "cognitive",
    "aptitude": "cognitive",
    "scenario": "situational",
    "scenarios": "situational",
    "judgement": "situational",
    "judgment": "situational",
}


def _clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    for variant, canonical in SYNONYMS.items():
        pattern = r"\b" + re.escape(variant) + r"\b"
        text = re.sub(pattern, canonical, text)

    return text


def _get_words(text: str) -> List[str]:
    words = text.split()
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def _entry_text(entry: Dict[str, Any], field: str) -> str:
    value = entry.get(field, "")
    if isinstance(value, list):
        return " ".join(str(v) for v in value)
    return str(value or "")


def _entry_all_text_clean(entry: Dict[str, Any]) -> str:
    combined = " ".join([
        _entry_text(entry, "name"),
        _entry_text(entry, "keys"),
        _entry_text(entry, "description"),
    ])
    return _clean_text(combined)


def _build_rarity_table(catalog_entries: List[Dict[str, Any]]) -> Dict[str, float]:
    total_entries = len(catalog_entries)
    doc_frequency = {}

    for entry in catalog_entries:
        words_in_entry = set(_get_words(_entry_all_text_clean(entry)))

        for word in words_in_entry:
            doc_frequency[word] = doc_frequency.get(word, 0) + 1

    rarity_table = {}

    for word, df in doc_frequency.items():
        rarity_table[word] = math.log((total_entries + 1) / (df + 1)) + 1

    return rarity_table


RARITY = _build_rarity_table(catalog)
DEFAULT_RARITY = 1.0


def _rarity_of(word: str) -> float:
    return RARITY.get(word, DEFAULT_RARITY)


def _score_field(query_words: List[str], field_text: str, weight: int) -> float:
    if not field_text:
        return 0.0

    field_words = set(field_text.split())
    score = 0.0

    for word in set(query_words):
        if word in field_words:
            score += weight * _rarity_of(word)

    return score


def _phrase_bonus(query_clean: str, field_text: str, bonus: int) -> float:
    if len(query_clean.split()) < 2:
        return 0.0

    if query_clean in field_text:
        return bonus

    return 0.0


def _score_entry(query_clean: str, query_words: List[str], entry: Dict[str, Any]) -> float:
    name_text = _clean_text(_entry_text(entry, "name"))
    keys_text = _clean_text(_entry_text(entry, "keys"))
    description_text = _clean_text(_entry_text(entry, "description"))

    score = 0.0
    score += _score_field(query_words, name_text, WEIGHT_NAME)
    score += _score_field(query_words, keys_text, WEIGHT_KEYS)
    score += _score_field(query_words, description_text, WEIGHT_DESCRIPTION)

    score += _phrase_bonus(query_clean, name_text, PHRASE_BONUS_NAME)
    score += _phrase_bonus(query_clean, description_text, PHRASE_BONUS_DESCRIPTION)

    return score


def recommend_assessments(query: str, top_k: int = 10):
    if not query or not query.strip():
        return []

    query_clean = _clean_text(query)
    query_words = _get_words(query_clean)

    if not query_words:
        return []

    scored = []

    for entry in catalog:
        score = _score_entry(query_clean, query_words, entry)

        if score >= MIN_SCORE:
            scored.append((score, entry))

    scored.sort(
        key=lambda pair: (
            -pair[0],
            _entry_text(pair[1], "name").lower()
        )
    )

    recommendations = []

    for _, entry in scored[:top_k]:
        recommendations.append(
            {
                "name": entry.get("name", ""),
                "url": entry.get("link", ""),
                "test_type": ", ".join(entry.get("keys", [])),
            }
        )

    return recommendations