# 🌟 GitHub Trending Tracker (CLI Tool)

A **Command-Line Tool** that scrapes **GitHub Trending**, stores repository data, and analyzes **stars growth, consistency, and ranking trends** over time.  
Perfect for tracking which projects are consistently popular and spotting fast-rising repos.

---

## 🚀 Features

- 📡 **Web Scraping** – Collects trending repositories using **BeautifulSoup + lxml**  
- 💾 **Database Support** – Stores data for daily tracking  
- 📊 **Statistics**:
  - Presence % (days repo appeared in trending)  
  - Average stars (mean, std, min, max)  
  - Average rank  
  - Trend slope (stars growth per day)  
- 📈 **Visualization** – Plots top repositories’ star trends  
- 🖥️ **CLI Based** – No GUI, runs fully in terminal  

---

## 📂 Project Structure

Project/
│── config/ # Config files (e.g., config.yaml)
│── data/ # Raw scraped data
│── output/ # Generated plots & reports
│── src/ # Core source code
│── test/ # Test scripts
│── dbchecker.py # Database check helper
│── main.py # CLI entry point
│── requirements.txt # Dependencies
│── README.md # Documentation


---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/github-trending-tracker.git
cd github-trending-tracker

Create & activate virtual environment (conda way):

conda create -n github_star_repo python=3.11 -y
conda activate github_star_repo
pip install -r requirements.txt

Or using venv:

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt

🛠️ Configuration

Edit config/config.yaml to adjust settings:

scraper:
  trending_url: "https://github.com/trending"
  since: "daily"       # daily | weekly | monthly
  user_agent: "Mozilla/5.0"

database:
  path: "data/repos.db"

output:
  folder: "output"

plot:
  top_n: 10
  figsize: [10, 6]

▶️ Usage

Run the tool:

python main.py

Example Flow:

Checks if today’s data is already in database

Scrapes GitHub Trending if not present

Asks how many days to analyze (default: 7)

Computes summary stats

Generates trend plots in output/

📊 Example Output
CLI Stats:
====== Summary Stats =======
{
  'total_days': 7,
  'total_unique_repos': 42,
  'most_present': [...],
  'consistent_repos': [...],
  'top_by_average_stars': [...]
}

Plots:

📈 Star growth of top trending repositories will be saved in /output/.

🧰 Built With

BeautifulSoup4
 – Web scraping

lxml
 – HTML parsing

pandas
 – Data analysis

numpy
 – Math operations (polyfit for slope)

matplotlib
 – Plotting

tqdm
 – Progress bars

💡 Future Improvements

Add CLI flags (e.g., --days 30 --since weekly)

Export reports to CSV/Excel

Automate with GitHub Actions (daily scrape)

Build a simple web dashboard

📜 License

MIT License – free to use & modify.