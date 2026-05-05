from datetime import datetime

def recency_score(year):
    if not year or year == "Unknown":
        return 0.5

    try:
        year = int(year)
        age = datetime.now().year - year

        if age <= 1:
            return 1.0
        elif age <= 3:
            return 0.8
        elif age <= 5:
            return 0.6
        else:
            return 0.3
    except:
        return 0.5


def calculate_trust_score(
    author_credibility,
    citation_count,
    domain_authority,
    recency,
    medical_disclaimer_presence
):
    score = (
        author_credibility * 0.25 +
        citation_count * 0.20 +
        domain_authority * 0.25 +
        recency * 0.20 +
        medical_disclaimer_presence * 0.10
    )

    return round(min(max(score, 0), 1), 2)