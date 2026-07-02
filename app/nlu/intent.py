import re


COMPARE_PATTERNS = [
    r"\bcompare\b",
    r"\bdifference between\b",
    r"\bvs\.?\b",
    r"\bversus\b",
    r"\bwhich is better\b",
]

REFINE_KEYWORDS = [
    "add",
    "include",
    "remove",
    "drop",
    "delete",
    "exclude",
    "replace",
    "swap",
    "change",
    "update",
]

VAGUE_PATTERNS = [
    r"^need assessment$",
    r"^help me hire$",
    r"^suggest test$",
    r"^can you help\??$",
    r"^recommend assessment$",
]

ROLE_SIGNAL_KEYWORDS = [
    "developer",
    "engineer",
    "manager",
    "analyst",
    "sales",
    "graduate",
    "intern",
    "python",
    "java",
    "sql",
    "aws",
    "backend",
    "frontend",
]

VAGUE_MAX_WORDS = 6


def _matches_any(patterns, text: str) -> bool:
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False


def _contains_any_keyword(keywords, text: str) -> bool:
    for keyword in keywords:
        if keyword in text:
            return True
    return False


def detect_intent(message: str) -> str:
    if message is None:
        return "clarify"

    text = message.strip().lower()

    if not text:
        return "clarify"

    if _matches_any(COMPARE_PATTERNS, text):
        return "compare"

    if _contains_any_keyword(REFINE_KEYWORDS, text):
        return "refine"

    if _matches_any(VAGUE_PATTERNS, text):
        return "clarify"

    if _contains_any_keyword(ROLE_SIGNAL_KEYWORDS, text):
        return "recommend"

    word_count = len(text.split())

    if word_count <= VAGUE_MAX_WORDS:
        return "clarify"

    return "clarify"