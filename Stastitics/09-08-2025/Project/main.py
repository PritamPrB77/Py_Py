import sys
import os
import pprint


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
print(f"Project root: {PROJECT_ROOT}")
from src.database import DatabaseManager
from src.utils import load_config, ensure_folder_exists, get_today_date
from src.scraper import GitHubScraper
from src.stats import summarize_stats, top_repo_names_from_summary
from src.plotting import plot_top_repos

def main():
    cfg = load_config(os.path.join(PROJECT_ROOT, "config", "config.yaml"))
    print(cfg)
    data_folder = os.path.join(PROJECT_ROOT, "data")
    output_folder = os.path.join(PROJECT_ROOT, cfg["output"]["folder"])
    db_path = os.path.join(PROJECT_ROOT, cfg["database"]["path"])
    print(data_folder, output_folder, db_path)
    print("Ensuring folders exist...")
    ensure_folder_exists(data_folder)
    ensure_folder_exists(output_folder)

    db = DatabaseManager(db_path)
    today = get_today_date()
    print(f"Today's date: {today}")
    if db.date_exists(today):
        print(f"Data for today already exist. Skipping scrape and insert for data : {today}")
    else:
        url = cfg["scraper"]["trending_url"]
        if cfg["scraper"].get("since"):
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}since={cfg['scraper']['since']}"
        headers = {"User-Agent": cfg["scraper"].get("user_agent", "Mozilla/5.0")}
          # e:g-https://example.com/search?q=python
          #https://example.com/search?q=python&page=2
# .get(key, default) ek dictionary method hai jo:

# Agar key dict me present hai → uska value return karega.

# Agar key present nahi hai → default value return karega.
        print("Starting scrape:", url)
        scraper = GitHubScraper(url, headers=headers)
        try:
            repos = scraper.scrape_trending()
            db.insert_repos(today, repos)
            print(f"Inserted/Updated {len(repos)} repos for {today}")
        except Exception as e:
            print(f"Exception occured while scraping data from github, Error : {e}")

    try:
        days = int(input("Enter number of days to analyze (e.g., 7): ").strip())
    except Exception:
        print("Invalid input, defaulting to 7 days.")
        days = 7  

    rows = db.fetch_last_n_days(days)
    if not rows:
        print("No data found for the selected period. Exiting.")
        return
    else:
        stats = summarize_stats(rows, top_n=cfg["plot"]["top_n"], min_presence_pct=0.3)

    print("\n====== Summary Stats =======")
    pprint.pprint(stats)

    top_names = top_repo_names_from_summary(stats, fallback_top_n=cfg["plot"]["top_n"])
    print("top names =",top_names)
    if not top_names:
        print("No repos found to plot.")
    else:
        plot_top_repos(rows, output_folder, top_repos=top_names, figsize=tuple(cfg["plot"]["figsize"]))
    
    
if __name__ == '__main__':

    main()
