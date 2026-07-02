def refine_recommendations(message: str, recommendations: list):
    message = message.lower()

    if not recommendations:
        return recommendations

    def contains(rec, keyword):
        return (
            keyword in rec["name"].lower()
            or keyword in rec["test_type"].lower()
        )

    # Remove SQL assessments
    if "sql" in message and ("remove" in message or "exclude" in message):
        recommendations = [
            rec for rec in recommendations
            if not contains(rec, "sql")
        ]

    # Remove numerical assessments
    if "numerical" in message and (
        "remove" in message or "exclude" in message
    ):
        recommendations = [
            rec for rec in recommendations
            if not contains(rec, "numerical")
        ]

    # Remove aptitude assessments
    if "aptitude" in message and (
        "remove" in message or "exclude" in message
    ):
        recommendations = [
            rec for rec in recommendations
            if not contains(rec, "aptitude")
        ]

    # Remove ability assessments
    if "ability" in message and (
        "remove" in message or "exclude" in message
    ):
        recommendations = [
            rec for rec in recommendations
            if not contains(rec, "ability")
        ]

    # Only personality assessments
    if "personality" in message:
        recommendations = [
            rec for rec in recommendations
            if contains(rec, "personality")
        ]

    # Only technical / coding assessments
    if "technical" in message or "coding" in message:
        recommendations = [
            rec for rec in recommendations
            if (
                contains(rec, "knowledge")
                or contains(rec, "skills")
                or contains(rec, "python")
                or contains(rec, "developer")
            )
        ]

    return recommendations