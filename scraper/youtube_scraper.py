from youtube_transcript_api  import YouTubeTranscriptApi
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
def scrape_youtube(url):
    video_id=get_video_id(url)
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
    except:
        transcript = "Transcript unavailable"

    if transcript != "Transcript unavailable":
        language = detect(transcript)
    else:
        language = "unknown"
    topic_tags = generate_tags(transcript)

    trust_score = calculate_trust_score(
        author_credibility=0.6,
        citation_count=0.3,
        domain_authority=0.7,
        recency=0.7,
        medical_disclaimer_presence=0.4
    )

    return {
        "source_url": url,
        "source_type": "youtube",
        "author": "YouTube Channel",
        "published_date": "Unknown",
        "language": language,
        "region": "Unknown",
        "topic_tags": topic_tags,
        "trust_score": trust_score,
        "content_chunks": chunk_text(transcript)
    }

