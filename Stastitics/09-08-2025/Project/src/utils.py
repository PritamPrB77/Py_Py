import os
import yaml
from datetime import datetime,timedelta

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    # parse the YAML file and return the configuration as a dictionary
    
def ensure_folder_exists(folder_path: str):
    os.makedirs(folder_path, exist_ok=True)

# def get_today_date() -> str:
#     return datetime.now().strftime("%Y-%m-%d")

def get_today_date() -> str:
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

#Agar timedelta(days=2) karte ho → 2 din pehle ki date return hogi.

# Agar timedelta(days=7) karte ho → 1 week pehle ki date milegi.

# Agar timedelta(days=-1) karte ho → subtract ke bajaye kal ki date (tomorrow) return hogi.

# Agar timedelta(days=0) karte ho → koi change nahi hoga, aaj ki date return hogi.