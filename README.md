# Hacker News Scraper

A command-line tool that scrapes Hacker News front page stories, filters by score, and exports results to CSV.

## Features

- Scrapes up to 5 pages of Hacker News stories (150 stories)
- Extracts title, URL, score, author, and comment count per story
- Filter stories by minimum score
- Sorts results by score (highest first)
- Exports to timestamped CSV file
- Retry logic with respectful rate limiting

## Usage

```bash
# Clone the repo
git clone https://github.com/EXE901/hacker-news-scraper.git
cd hacker-news-scraper

# Install dependencies
pip install -r requirements.txt

# Run
python scraper.py
```

## Example Output

```
Hacker News Scraper
============================================================
How many pages to scrape? (1-5, default 1): 2
Minimum score filter? (0 for all, default 0): 100

Scraping page 1...
Scraping page 2...

============================================================
  Top 10 Stories
============================================================

1. Show HN: I built a tool that does X
   Score: 847 | Author: username | Comments: 312
   https://example.com/article

2. Ask HN: How do you structure large Python projects?
   Score: 623 | Author: username2 | Comments: 189
   https://news.ycombinator.com/item?id=...
```

## CSV Output

Each run saves a timestamped CSV (e.g. `hn_stories_20240415_143022.csv`):

| title | url | score | author | comments |
|-------|-----|-------|--------|----------|
| Story title | https://... | 847 | user | 312 |

## Project Structure

```
web_scraper/
│── scraper.py       # Main scraper logic
│── requirements.txt
│── README.md
```

## Tech Stack

- Python 3.x
- `requests` — HTTP requests with retry logic
- `beautifulsoup4` — HTML parsing
- `csv` — standard library CSV export

## What I Learned

- HTTP requests and response handling
- HTML parsing with BeautifulSoup and CSS selectors
- Data filtering and sorting
- CSV file I/O
- Rate limiting and respectful scraping practices
- Retry logic for robust network handling
