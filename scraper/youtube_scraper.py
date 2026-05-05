import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from langdetect import detect

from utils.chunking import chunk_text
from utils.tagging import generate_tags
from scoring.trust_score import calculate_trust_score


def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    return url


def get_youtube_metadata(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = "Unknown Title"
        title_tag = soup.find("meta", property="og:title")
        if title_tag:
            title = title_tag.get("content", "Unknown Title")

        description = "No description available"
        desc_tag = soup.find("meta", property="og:description")
        if desc_tag:
            description = desc_tag.get("content", "No description available")

        channel = "Unknown Channel"
        channel_tag = soup.find("link", itemprop="name")
        if channel_tag:
            channel = channel_tag.get("content", "Unknown Channel")

        return title, description, channel

    except:
        return "Unknown Title", "No description available", "Unknown Channel"


def scrape_youtube(url):
    video_id = get_video_id(url)

    title, description, channel = get_youtube_metadata(url)

    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
    except:
        transcript = "Transcript unavailable"

    full_text = title + " " + description + " " + transcript

    language = detect(full_text) if full_text.strip() else "unknown"
    topic_tags = generate_tags(full_text)

    trust_score = calculate_trust_score(
        author_credibility=0.7 if channel != "Unknown Channel" else 0.5,
        citation_count=0.3,
        domain_authority=0.7,
        recency=0.7,
        medical_disclaimer_presence=0.4
    )

    return {
        "source_url": url,
        "source_type": "youtube",
        "title": title,
        "description": description,
        "author": channel,
        "published_date": "Unknown",
        "language": language,
        "region": "Unknown",
        "topic_tags": topic_tags,
        "trust_score": trust_score,
        "content_chunks": chunk_text(transcript)
    }