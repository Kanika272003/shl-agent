def refine_recommendations(message: str, recommendations: list):
    message = message.lower()

    if not recommendations:
        return recommendations

    # Remove SQL-related tests
    if "remove sql" in message:
        recommendations = [
            rec for rec in recommendations
            if "sql" not in rec["name"].lower()
        ]

    # Remove numerical assessments
    if "remove numerical" in message or "numerical" in message:
        recommendations = [
            rec for rec in recommendations
            if "numerical" not in rec["name"].lower()
            and "numerical" not in rec["test_type"].lower()
        ]

    # Keep only personality assessments
    if "personality" in message:
        recommendations = [
            rec for rec in recommendations
            if "personality" in rec["test_type"].lower()
        ]

    return recommendations