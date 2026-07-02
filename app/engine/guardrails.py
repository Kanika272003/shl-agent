import re
from typing import Optional, Tuple


INJECTION_PATTERNS = [
    r"ignore (all|any|the)? ?previous instructions",
    r"ignore (all|any|the)? ?prior instructions",
    r"ignore all above",
    r"ignore everything",
    r"disregard (all|any|the)? ?previous instructions",
    r"forget (all|any|the)? ?(previous|prior) instructions",
    r"forget your rules",
    r"act as (an?|another) (ai|assistant|model|chatbot)",
    r"pretend (you are|to be)",
    r"you are now",
    r"reveal (your|the) system prompt",
    r"show (me )?(your|the) system prompt",
    r"show hidden prompt",
    r"internal instructions",
    r"confidential prompt",
    r"what is your system prompt",
    r"print (your|the) instructions",
    r"repeat (your|the) instructions",
    r"jailbreak",
    r"dan mode",
    r"developer mode",
    r"disable guardrails",
    r"system override",
    r"bypass (your|all)? ?(restrictions|rules|guardrails|filters)",
    r"override (your|all)? ?(restrictions|rules|guardrails|filters)",
]

LEGAL_PATTERNS = [
    r"legal requirement",
    r"legal obligation",
    r"is it legal",
    r"lawsuit",
    r"sue",
    r"lawyer",
    r"attorney",
    r"litigation",
    r"regulatory compliance",
]

NON_SHL_PATTERNS = [
    r"\bhackerrank\b",
    r"\bcodesignal\b",
    r"\bleetcode\b",
    r"\bpymetrics\b",
    r"\bharver\b",
    r"non[- ]shl",
    r"outside (the )?shl catalog",
    r"other than shl",
    r"recommend.*outside.*catalog",
    r"custom assessment",
    r"create new assessment",
]

OFF_TOPIC_PATTERNS = [
    r"\bweather\b",
    r"\brecipe\b",
    r"\bjoke\b",
    r"\bpoem\b",
    r"\bsong\b",
    r"\bstory\b",
    r"\bmovie\b",
    r"\bcrypto\b",
    r"\bbitcoin\b",
    r"\bhoroscope\b",
    r"\btranslate\b",
    r"\bsports\b",
]

HIRING_ADVICE_PATTERNS = [
    r"how (should|do) i (fire|terminate|lay off)",
    r"salary negotiation",
    r"how much should i pay",
    r"offer letter",
    r"background check",
]

REFUSAL_INJECTION = (
    "I can't follow instructions that override my configuration. "
    "I can help you select SHL assessments."
)

REFUSAL_LEGAL = (
    "I can't provide legal or compliance advice. "
    "Please consult your legal team."
)

REFUSAL_NON_SHL = (
    "I can only recommend assessments from the SHL catalog."
)

REFUSAL_OFF_TOPIC = (
    "I only help with SHL assessment recommendations for hiring."
)

REFUSAL_HIRING_ADVICE = (
    "I can't provide HR or compensation advice. "
    "I can help select SHL assessments."
)


def _matches_any(patterns, text: str) -> bool:
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False


def check_guardrails(message: str) -> Tuple[bool, Optional[str]]:
    if message is None:
        return True, None

    text = message.strip().lower()

    if not text:
        return True, None

    if _matches_any(INJECTION_PATTERNS, text):
        return False, REFUSAL_INJECTION

    if _matches_any(LEGAL_PATTERNS, text):
        return False, REFUSAL_LEGAL

    if _matches_any(NON_SHL_PATTERNS, text):
        return False, REFUSAL_NON_SHL

    if _matches_any(HIRING_ADVICE_PATTERNS, text):
        return False, REFUSAL_HIRING_ADVICE

    if _matches_any(OFF_TOPIC_PATTERNS, text):
        return False, REFUSAL_OFF_TOPIC

    return True, None