import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
from typing import List, Tuple


def _parse_stars_text(text: str) -> int:
    if not text:
        return 0
    t = text.strip().lower().replace(",", "")
    try:
        if "k" in t:
            return int(float(t.replace("k", "").strip()) * 1000)
        return int(float(t))
    except Exception:
        m = re.search(r"[\d\.]+", t)
        if m:
            val = float(m.group(0))
            if "k" in t:
                return int(val * 1000)
            return int(val)
        return 0
    """
      Yeh regex numbers aur decimal extract karta hai (e.g. "stars: 2.3k" → "2.3").

     float(m.group(0)) → extracted number ko float me convert karta hai.

    Phir wahi "k" logic apply hota hai.
    """

class GitHubScraper:
    def __init__(self, url: str, headers: dict = None):
        self.url = url
        self.headers = headers or {"User-Agent": "Mozilla/5.0"}

    def scrape_trending(self) -> List[Tuple[str, int]]:
        resp = requests.get(self.url, headers=self.headers, timeout=15)
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to fetch {self.url}: {resp.status_code}")
        soup = BeautifulSoup(resp.text, "html.parser")
        repo_list = []
        items = soup.find_all("article", class_="Box-row")
        for item in tqdm(items, desc="Scraping repos"):
            a = item.find("h2")
            if a and a.find("a"):
                href = a.find("a").get("href", "").strip()
                repo_name = href.strip("/").lstrip("/")
            else:
                repo_name = item.get_text(strip=True).split()[0]
            # star element: an <a> whose href endswith '/stargazers'
            star_tag = item.find("a", href=re.compile(r"/stargazers$"))
            stars = _parse_stars_text(star_tag.get_text()) if star_tag else 0
            repo_list.append((repo_name, stars))
            print(f"Found repo: {repo_name} with stars: {stars}")
        return repo_list