import requests
from bs4 import BeautifulSoup
from langdetect import detect
from utils.chunking import chunk_text
from utils.tagging import generate_tags
from scoring.trust_score import calculate_trust_score

def scrape_blog(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    author = "Unknown"          # add this first
    published_date = "Unknown"  # add this first

    author_tag = soup.find(attrs={"name": "author"})
    if author_tag:
        author = author_tag.get("content", "Unknown")

    time_tag = soup.find("time")
    if time_tag:
        published_date = time_tag.get_text(strip=True)

    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text(strip=True) for p in paragraphs])

    language = detect(content) if content else "unknown"
    topic_tags = generate_tags(content)

    trust_score = calculate_trust_score(
        author_credibility=0.8 if author != "Unknown" else 0.5,
        citation_count=0.3,
        domain_authority=0.6,
        recency=0.7,
        medical_disclaimer_presence=0.5
    )

    return {
        "source_url": url,
        "source_type": "blog",
        "author": author,
        "published_date": published_date,
        "language": language,
        "region": "Unknown",
        "topic_tags": topic_tags,
        "trust_score": trust_score,
        "content_chunks": chunk_text(content)
    }