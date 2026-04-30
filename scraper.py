import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; HackerNewsScraper/1.0)"
}


def fetch_page(url, retries=3, delay=2):
    """Fetch a page with retry logic and error handling."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    return None


def parse_stories(html):
    """Parse Hacker News stories from HTML and return a list of dicts."""
    soup = BeautifulSoup(html, "html.parser")
    stories = []

    rows = soup.select("tr.athing")

    for row in rows:
        # Title and URL
        title_tag = row.select_one("span.titleline > a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        url = title_tag.get("href", "")

        # Skip internal links
        if url.startswith("item?"):
            url = f"https://news.ycombinator.com/{url}"

        # Score and metadata from the next sibling row
        subtext_row = row.find_next_sibling("tr")
        score = 0
        comments = 0
        author = "unknown"

        if subtext_row:
            score_tag = subtext_row.select_one("span.score")
            if score_tag:
                score = int(score_tag.get_text().replace(" points", "").replace(" point", ""))

            author_tag = subtext_row.select_one("a.hnuser")
            if author_tag:
                author = author_tag.get_text(strip=True)

            comment_tags = subtext_row.select("a")
            for tag in comment_tags:
                text = tag.get_text(strip=True)
                if "comment" in text:
                    try:
                        comments = int(text.split()[0])
                    except ValueError:
                        comments = 0

        stories.append({
            "title": title,
            "url": url,
            "score": score,
            "author": author,
            "comments": comments,
        })

    return stories


def save_to_csv(stories, filename=None):
    """Save stories to a CSV file."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hn_stories_{timestamp}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url", "score", "author", "comments"])
        writer.writeheader()
        writer.writerows(stories)

    return filename


def scrape(pages=1, min_score=0, save_csv=True):
    """
    Scrape Hacker News front page stories.

    Args:
        pages (int): Number of pages to scrape (each page has 30 stories)
        min_score (int): Only include stories with at least this score
        save_csv (bool): Whether to save results to CSV

    Returns:
        list: List of story dicts
    """
    all_stories = []

    for page in range(1, pages + 1):
        url = f"https://news.ycombinator.com/news?p={page}"
        print(f"Scraping page {page}...")

        html = fetch_page(url)
        if not html:
            print(f"Failed to fetch page {page}, skipping.")
            continue

        stories = parse_stories(html)
        all_stories.extend(stories)

        if page < pages:
            time.sleep(1)  # be respectful to the server

    # Filter by minimum score
    if min_score > 0:
        all_stories = [s for s in all_stories if s["score"] >= min_score]

    # Sort by score descending
    all_stories.sort(key=lambda x: x["score"], reverse=True)

    return all_stories


def display_stories(stories, limit=10):
    """Print stories to the console in a readable format."""
    print(f"\n{'='*60}")
    print(f"  Top {min(limit, len(stories))} Stories")
    print(f"{'='*60}\n")

    for i, story in enumerate(stories[:limit], 1):
        print(f"{i}. {story['title']}")
        print(f"   Score: {story['score']} | Author: {story['author']} | Comments: {story['comments']}")
        print(f"   {story['url']}")
        print()


def main():
    print("Hacker News Scraper")
    print("=" * 60)

    try:
        pages = int(input("How many pages to scrape? (1-5, default 1): ").strip() or "1")
        pages = max(1, min(5, pages))  # clamp between 1 and 5

        min_score = int(input("Minimum score filter? (0 for all, default 0): ").strip() or "0")

    except ValueError:
        print("Invalid input, using defaults.")
        pages, min_score = 1, 0

    stories = scrape(pages=pages, min_score=min_score)

    if not stories:
        print("No stories found.")
        return

    display_stories(stories, limit=10)

    save = input("Save results to CSV? (y/n, default y): ").strip().lower()
    if save != "n":
        filename = save_to_csv(stories)
        print(f"Saved {len(stories)} stories to {filename}")

    print(f"\nTotal stories scraped: {len(stories)}")


if __name__ == "__main__":
    main()
