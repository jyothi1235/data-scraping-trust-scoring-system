from Bio import Entrez
from langdetect import detect

from utils.chunking import chunk_text
from utils.tagging import generate_tags
from scoring.trust_score import calculate_trust_score, recency_score

Entrez.email = "your_email@gmail.com"
def scrape_pubmed(pubmed_id):
    handle = Entrez.efetch(
        db="pubmed",
        id=pubmed_id,
        rettype="xml",
        retmode="xml"
    )
    records = Entrez.read(handle)

    article = records["PubmedArticle"][0]["MedlineCitation"]["Article"]

    title = str(article.get("ArticleTitle", "Unknown Title"))

    abstract = "No abstract available"
    if "Abstract" in article:
        abstract = " ".join(article["Abstract"]["AbstractText"])

    authors = []
    if "AuthorList" in article:
        for author in article["AuthorList"]:
            first_name = author.get("ForeName", "")
            last_name = author.get("LastName", "")
            full_name = f"{first_name} {last_name}".strip()
            authors.append(full_name)

    year = "Unknown"
    try:
        year = article["Journal"]["JournalIssue"]["PubDate"]["Year"]
    except:
        year = "Unknown"

    full_content = title + ". " + abstract

    if abstract != "No abstract available":
        language = detect(abstract)
    else:
        language = "unknown"

    topic_tags = generate_tags(full_content)

    trust_score = calculate_trust_score(
        author_credibility=0.9,
        citation_count=0.8,
        domain_authority=1.0,
        recency=recency_score(year),
        medical_disclaimer_presence=0.8
    )

    return {
        "source_url": f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/",
        "source_type": "pubmed",
        "author": authors,
        "published_date": year,
        "language": language,
        "region": "Unknown",
        "topic_tags": topic_tags,
        "trust_score": trust_score,
        "content_chunks": chunk_text(full_content)
    }