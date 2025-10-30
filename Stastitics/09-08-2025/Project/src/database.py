import sqlite3
import os
from typing import List, Tuple
from datetime import datetime, timedelta


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        parent = os.path.dirname(os.path.abspath(db_path))
        # print(f"Ensuring database directory exists: {parent}",os.path.exists(parent))
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        self._create_table()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        return conn
    
    def _create_table(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trending_repos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                repo_name TEXT NOT NULL,
                stars INTEGER DEFAULT 0,
                UNIQUE(date, repo_name)
            )
        """)
        conn.commit()
        conn.close()
        """
        Iska matlab hai: (date, repo_name) ka combination hamesha unique hona chahiye.

        date same ho sakti hai for multiple repos, aur repo_name same ho sakta hai multiple dates par, but dono ek saath same nahi ho sakte.
        """

    def date_exists(self, date: str) -> bool:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM trending_repos WHERE date = ? LIMIT 1", (date,))
        exists = cur.fetchone() is not None
        conn.close()
        return exists
    
    def insert_repos(self, date: str, repos: List[Tuple[str, int]]):
        conn = self._connect()
        cur = conn.cursor()
        cur.executemany(
            "INSERT OR REPLACE INTO trending_repos (date, repo_name, stars) VALUES (?, ?, ?)",
            [(date, name, int(stars)) for name, stars in repos]
        )
        conn.commit()
        conn.close()

    def fetch_last_n_days(self, days: int) -> List[Tuple[str, str, int]]:
        conn = self._connect()
        cur = conn.cursor()
        if days <= 0:
            cur.execute("SELECT date, repo_name, stars FROM trending_repos ORDER BY date ASC, stars DESC")
            rows = cur.fetchall()
            conn.close()
            return rows
        
        today = datetime.now().date()
        start_date = (today - timedelta(days=days - 1)).strftime("%Y-%m-%d")
        cur.execute(
            "SELECT date, repo_name, stars FROM trending_repos WHERE date >= ? ORDER BY date ASC, stars DESC",
            (start_date,)
        )
        rows = cur.fetchall()
        conn.close()
        return rows