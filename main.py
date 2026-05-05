import json
import os

from scraper.blog_scraper import scrape_blog
from scraper.youtube_scraper import scrape_youtube
from scraper.pubmed_scraper import scrape_pubmed


blog_urls = [
    "https://www.ibm.com/think/topics/artificial-intelligence",
    "https://www.oracle.com/artificial-intelligence/what-is-ai/",
    "https://www.geeksforgeeks.org/web-scraping/"
]

youtube_urls = [
    "https://www.youtube.com/watch?v=aircAruvnKk",
    "https://www.youtube.com/watch?v=rfscVS0vtbw"
]

pubmed_ids = [
    "37061324"
]


os.makedirs("output", exist_ok=True)

all_data = []
blogs_data = []
youtube_data = []
pubmed_data = []


for url in blog_urls:
    try:
        data = scrape_blog(url)
        blogs_data.append(data)
        all_data.append(data)
    except Exception as e:
        print("Blog error:", url, e)


for url in youtube_urls:
    try:
        data = scrape_youtube(url)
        youtube_data.append(data)
        all_data.append(data)
    except Exception as e:
        print("YouTube error:", url, e)


for pid in pubmed_ids:
    try:
        data = scrape_pubmed(pid)
        pubmed_data.append(data)
        all_data.append(data)
    except Exception as e:
        print("PubMed error:", pid, e)


with open("output/blogs.json", "w", encoding="utf-8") as file:
    json.dump(blogs_data, file, indent=4, ensure_ascii=False)

with open("output/youtube.json", "w", encoding="utf-8") as file:
    json.dump(youtube_data, file, indent=4, ensure_ascii=False)

with open("output/pubmed.json", "w", encoding="utf-8") as file:
    json.dump(pubmed_data, file, indent=4, ensure_ascii=False)

with open("output/scraped_data.json", "w", encoding="utf-8") as file:
    json.dump(all_data, file, indent=4, ensure_ascii=False)


print("Project completed successfully.")
print("Blogs scraped:", len(blogs_data))
print("YouTube videos scraped:", len(youtube_data))
print("PubMed articles scraped:", len(pubmed_data))
print("Total sources:", len(all_data))
print("Check output folder.")