# Data Scraping & Trust Scoring Project

## 📌 Objective

This project implements a **multi-source data scraping pipeline** and a **trust scoring system**.
It collects structured data from:

* Blog websites
* YouTube videos
* PubMed research articles

and evaluates the **reliability of each source** using a custom trust score algorithm.

---

## 📁 Project Structure

```
project/
├── scraper/
│   ├── blog_scraper.py
│   ├── youtube_scraper.py
│   └── pubmed_scraper.py
│
├── scoring/
│   └── trust_score.py
│
├── utils/
│   ├── tagging.py
│   └── chunking.py
│
├── output/
│   ├── blogs.json
│   ├── youtube.json
│   ├── pubmed.json
│   └── scraped_data.json
│
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Tools & Libraries Used

* Python
* Requests
* BeautifulSoup (for blog scraping)
* youtube-transcript-api (for YouTube data)
* Biopython (Entrez API for PubMed)
* langdetect (for language detection)
* JSON (for data storage)

---

## 🕸️ Scraping Approach

### 1. Blog Scraping

* Used `requests` and `BeautifulSoup`
* Extracted:

  * Author
  * Published date
  * Article content
* Removed unnecessary HTML elements
* Collected paragraph text

---

### 2. YouTube Scraping

* Used `youtube-transcript-api`
* Extracted:

  * Video transcript
* Converted transcript into text format

---

### 3. PubMed Scraping

* Used `Biopython Entrez API`
* Extracted:

  * Article title
  * Authors
  * Abstract
  * Publication year

---

## 🏷️ Topic Tagging

* Implemented keyword-based tagging
* Tags generated based on presence of keywords such as:

  * AI
  * Machine Learning
  * Healthcare
  * Data Scraping

---

## ✂️ Content Chunking

* Long content is split into smaller chunks
* Helps in:

  * Better processing
  * Improved readability

---

## 📊 Trust Score Design

Trust score is calculated using:

```
Trust Score = f(
  author_credibility,
  citation_count,
  domain_authority,
  recency,
  medical_disclaimer_presence
)
```

### Factors:

* **Author Credibility** → Known vs unknown authors
* **Citation Count** → (Simulated) references count
* **Domain Authority** → Blog vs PubMed reliability
* **Recency** → Newer content gets higher score
* **Medical Disclaimer** → Important for medical content

### Output:

* Score range: **0 to 1**

---

## ⚠️ Edge Case Handling

* Missing author → "Unknown"
* Missing publish date → "Unknown"
* Transcript unavailable → handled using try-except
* Non-English content → detected using `langdetect`
* Long content → handled using chunking

---

## 🔐 Abuse Prevention Logic

* Fake authors → low credibility score
* SEO spam blogs → lower domain authority
* Outdated content → penalized via recency score
* Missing medical disclaimer → lower trust score

---

## ▶️ How to Run the Project

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run the project

```
python main.py
```

---

## 📂 Output

The results are stored in:

* `output/blogs.json` → 3 blog sources
* `output/youtube.json` → 2 YouTube sources
* `output/pubmed.json` → 1 PubMed article
* `output/scraped_data.json` → combined data (6 sources)

---

## 🚧 Limitations

* Some websites block scraping
* YouTube transcripts may not be available for all videos
* Blog metadata extraction depends on HTML structure
* Citation count is simulated (not real)

---

## ✅ Conclusion

This project successfully demonstrates:

* Multi-source data scraping
* Data structuring into JSON format
* Trust score evaluation system

It provides a foundation for building scalable data pipelines and content evaluation systems.

---
