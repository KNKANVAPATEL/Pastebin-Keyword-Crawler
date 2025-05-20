# Pastebin Keyword Crawler

## Objective
This tool scrapes Pastebin's latest 30 public pastes and looks for keywords related to cryptocurrency and Telegram links.

## Keywords Detected
- "crypto"
- "bitcoin"
- "ethereum"
- "blockchain"
- "t.me"

## Output Format
Each match is stored in `keyword_matches.jsonl` in the following format:

```json
{
  "source": "pastebin",
  "context": "Found crypto-related content in Pastebin paste ID abc123",
  "paste_id": "abc123",
  "url": "https://pastebin.com/raw/abc123",
  "discovered_at": "2025-05-12T10:00:00Z",
  "keywords_found": ["crypto", "bitcoin"],
  "status": "pending"
}
```

## Setup Instructions

```bash
pip install -r requirements.txt
python pastebin_crawler.py
```

## Requirements
- requests
- beautifulsoup4
