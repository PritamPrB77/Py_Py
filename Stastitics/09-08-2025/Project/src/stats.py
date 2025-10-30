import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
from datetime import datetime

def rows_to_df(rows: List[Tuple[str, str, int]]) -> pd.DataFrame:
    df = pd.DataFrame(rows, columns=["date", "repo_name", "stars"])
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["date", "stars"], ascending=[True, False]).reset_index(drop=True)
    return df

def compute_presence(df: pd.DataFrame) -> pd.DataFrame:
    total_days = df["date"].nunique()
    presence = df.groupby("repo_name")["date"].nunique().rename("days_present").reset_index()
    presence["presence_pct"] = presence["days_present"] / max(1, total_days)
    return presence.sort_values(["days_present", "presence_pct"], ascending=False)

def compute_avg_stars(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby("repo_name")["stars"].agg(["mean", "std", "max", "min"]).reset_index()
    agg = agg.rename(columns={"mean": "avg_stars", "std": "std_stars"})
    agg["avg_stars"] = agg["avg_stars"].fillna(0)
    agg["std_stars"] = agg["std_stars"].fillna(0)
    return agg

def compute_avg_rank(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()
    tmp["rank"] = tmp.groupby("date")["stars"].rank(ascending=False, method="min")
    avg_rank = tmp.groupby("repo_name")["rank"].mean().reset_index().rename(columns={"rank": "avg_rank"})
    return avg_rank

def compute_trend_slope(df: pd.DataFrame) -> pd.DataFrame:
    slopes = []
    for repo, group in df.groupby("repo_name"):
        g = group.sort_values("date")
        if len(g) < 2:
            slopes.append({"repo_name": repo, "slope": 0.0})
            continue
        x = g["date"].map(datetime.toordinal).astype(float).values
        y = g["stars"].astype(float).values
        # fit line y = m x + c
        m, c = np.polyfit(x, y, 1)
        slopes.append({"repo_name": repo, "slope": float(m)})
    return pd.DataFrame(slopes)
"""
🔹 Example

Suppose data:

date	repo_name	stars
2025-08-01	repoA	100
2025-08-02	repoA	120
2025-08-03	repoA	150

👉 polyfit finds line slope ≈ +25/day.
So slope for repoA = 25.


"""
def summarize_stats(rows: List[Tuple[str, str, int]], top_n: int = 10, min_presence_pct: float = 0.5) -> Dict:

    df = rows_to_df(rows)
    if df.empty:
        return {
            "total_days": 0,
            "total_unique_repos": 0,
            "most_present": [],
            "consistent_repos": [],
            "top_by_average_stars": []
        }

    presence = compute_presence(df)
    avg = compute_avg_stars(df)
    avg_rank = compute_avg_rank(df)
    slope = compute_trend_slope(df)

    merged = presence.merge(avg, on="repo_name").merge(avg_rank, on="repo_name").merge(slope, on="repo_name")

    # order by days_present desc, avg_rank asc
    most_present = merged.sort_values(["days_present", "avg_rank"], ascending=[False, True]).head(top_n)
    consistent = merged[merged["presence_pct"] >= min_presence_pct].sort_values(["presence_pct", "avg_rank"], ascending=[False, True]).head(top_n)
    top_by_avg = merged.sort_values("avg_stars", ascending=False).head(top_n)

    summary = {
        "total_days": int(df["date"].nunique()),
        "total_unique_repos": int(df["repo_name"].nunique()),
        "most_present": most_present.to_dict(orient="records"),
        "consistent_repos": consistent.to_dict(orient="records"),
        "top_by_average_stars": top_by_avg.to_dict(orient="records"),
    }

    return summary

def top_repo_names_from_summary(summary: Dict, fallback_top_n: int = 10) -> List[str]:
    for key in ("consistent_repos", "most_present", "top_by_average_stars"):
        items = summary.get(key) or []
        if items:
            return [r["repo_name"] for r in items][:fallback_top_n]
    return []