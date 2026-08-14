"""Deterministic publication decision; AI output cannot bypass these gates."""

CRITICAL_FLAGS = {"title-only", "prompt-injection", "suspicious-url", "unsupported-claim"}


def decide(evidence_sufficient: bool, risk_flags: list[str], theme_score: float, threshold: float = 0.65) -> tuple[str, list[str]]:
    flags = set(risk_flags)
    reasons = []
    if flags & {"prompt-injection", "suspicious-url"}:
        return "quarantined", sorted(flags & {"prompt-injection", "suspicious-url"})
    if not evidence_sufficient:
        reasons.append("evidence insufficient for summary")
    if flags & CRITICAL_FLAGS:
        reasons.extend(sorted(flags & CRITICAL_FLAGS))
    if theme_score < threshold:
        reasons.append("primary theme score below threshold")
    return ("withheld", reasons) if reasons else ("published", ["passed automatic publication controls"])
