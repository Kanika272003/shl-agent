def compare_assessments(recommendations):
    if len(recommendations) < 2:
        return "Need at least two assessments to compare."

    first = recommendations[0]
    second = recommendations[1]

    comparison = f"""
Comparison between assessments:

1. {first['name']}
- Type: {first['test_type']}
- Best for evaluating role-specific technical skills

2. {second['name']}
- Type: {second['test_type']}
- Useful for measuring complementary skills

Summary:
{first['name']} focuses more on primary skill evaluation, while {second['name']} helps assess additional capabilities.
"""

    return comparison