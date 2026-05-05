import requests
from bs4 import BeautifulSoup
from langdetect import detect

from utils.chunking import chunk_text
from utils.tagging import generate_tags
from scoring.trust_score import calculate_trust_score


def scrape_blog(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    title = "Unknown Title"
    title_tag = soup.find("h1")
    if title_tag:
        title = title_tag.get_text(strip=True)

    author = "Unknown"
    author_tag = soup.find(attrs={"name": "author"})
    if author_tag:
        author = author_tag.get("content", "Unknown")

    published_date = "Unknown"
    time_tag = soup.find("time")
    if time_tag:
        published_date = time_tag.get_text(strip=True)

    description = "No description available"
    desc_tag = soup.find(attrs={"name": "description"})
    if desc_tag:
        description = desc_tag.get("content", "No description available")

    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text(strip=True) for p in paragraphs])

    full_text = title + " " + description + " " + content

    language = detect(full_text) if full_text.strip() else "unknown"
    topic_tags = generate_tags(full_text)

    disclaimer_present = 1.0 if "disclaimer" in full_text.lower() else 0.4

    trust_score = calculate_trust_score(
        author_credibility=0.8 if author != "Unknown" else 0.5,
        citation_count=0.3,
        domain_authority=0.6,
        recency=0.7,
        medical_disclaimer_presence=disclaimer_present
    )

    return {
        "source_url": url,
        "source_type": "blog",
        "title": title,
        "description": description,
        "author": author,
        "published_date": published_date,
        "language": language,
        "region": "Unknown",
        "topic_tags": topic_tags,
        "trust_score": trust_score,
        "content_chunks": chunk_text(content)
    }