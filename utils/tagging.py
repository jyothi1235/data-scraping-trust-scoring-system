def generate_tags(text):
    keywords=[
        "AI",
        "machine learning",
        "healthcare",
        "medicine",
        "data scraping",
        "deep learning",
        "NLP",
        "Python",
        "research",
        "technology"
    ]
    text_lower=text.lower()
    tags=[]
    for keyword in keywords:
        if keyword.lower() in text_lower:
            tags.append(keyword)
    return tags        