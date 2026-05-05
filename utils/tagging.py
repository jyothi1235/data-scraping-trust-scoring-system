def generate_tags(text):
    if not text:
        return []

    keywords = [
        "AI", "artificial intelligence", "machine learning",
        "deep learning", "healthcare", "medicine", "data scraping",
        "web scraping", "Python", "NLP", "research", "technology"
    ]

    text_lower = text.lower()
    tags = []

    for keyword in keywords:
        if keyword.lower() in text_lower:
            tags.append(keyword)

    return tags[:6]