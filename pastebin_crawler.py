import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import re

KEYWORDS = ["crypto", "bitcoin", "ethereum", "blockchain", "t.me"]
ARCHIVE_URL = "https://pastebin.com/archive"
RAW_URL_TEMPLATE = "https://pastebin.com/raw/{}"
OUTPUT_FILE = "keyword_matches.jsonl"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_paste_ids():
    response = requests.get(ARCHIVE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    paste_links = soup.select("table.maintable tr td a[href^='/']")
    paste_ids = [link["href"].strip("/") for link in paste_links[:30]]
    return paste_ids

def fetch_paste_content(paste_id):
    raw_url = RAW_URL_TEMPLATE.format(paste_id)
    try:
        response = requests.get(raw_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        print(f"Error fetching {paste_id}: {e}")
    return None

def keyword_found(content):
    found = [kw for kw in KEYWORDS if re.search(rf"\b{re.escape(kw)}\b", content, re.IGNORECASE)]
    return found

def main():
    paste_ids = get_paste_ids()
    print(f"[+] Found {len(paste_ids)} paste IDs")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for paste_id in paste_ids:
            print(f"[>] Checking paste ID: {paste_id}")
            content = fetch_paste_content(paste_id)
            if not content:
                continue
            keywords = keyword_found(content)
            if keywords:
                result = {
                    "source": "pastebin",
                    "context": f"Found crypto-related content in Pastebin paste ID {paste_id}",
                    "paste_id": paste_id,
                    "url": RAW_URL_TEMPLATE.format(paste_id),
                    "discovered_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "keywords_found": keywords,
                    "status": "pending"
                }
                f.write(json.dumps(result) + "\n")
                print(f"[+] Match found in {paste_id}: {keywords}")
            time.sleep(2)

if __name__ == "__main__":
    main()
